"""
train_model.py
Train ResNet50 trên HAM10000 với xử lý mất cân bằng lớp (class imbalance).
Giải quyết vấn đề: model chỉ đoán về lớp 'nv' (lớp đông nhất).

Chiến lược áp dụng:
1. Stratified split (giữ tỷ lệ lớp đều ở train/val/test)
2. Class weights tính tự động theo tần suất nghịch đảo
3. Augmentation mạnh hơn cho lớp hiếm (qua oversampling có augment)
4. Train 2 giai đoạn: freeze backbone -> fine-tune
5. Theo dõi Macro F1 thay vì Accuracy để chọn best model
"""

import os
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras import layers, models, callbacks, optimizers
from sklearn.model_selection import train_test_split
from sklearn.utils.class_weight import compute_class_weight
from sklearn.metrics import f1_score
import json

# ============================================
# CONFIG
# ============================================
IMG_SIZE = 224
BATCH_SIZE = 32
SEED = 42
NUM_CLASSES = 7
CLASS_NAMES = ['akiec', 'bcc', 'bkl', 'df', 'mel', 'nv', 'vasc']

METADATA_PATH = 'dataset/HAM10000/metadata/HAM10000_metadata.csv'
IMAGES_DIR = [
    'dataset/HAM10000/images/HAM10000_images_part_1',
    'dataset/HAM10000/images/HAM10000_images_part_2'
]
MODEL_DIR = 'model'
BEST_MODEL_PATH = os.path.join(MODEL_DIR, 'best_model.keras')
FINAL_MODEL_PATH = os.path.join(MODEL_DIR, 'skin_model.keras')

os.makedirs(MODEL_DIR, exist_ok=True)


# ============================================
# BƯỚC 1: CHUẨN BỊ DỮ LIỆU (STRATIFIED SPLIT)
# ============================================
def build_dataframe():
    """Đọc metadata, ghép đường dẫn ảnh, mã hóa nhãn."""
    df = pd.read_csv(METADATA_PATH)

    def find_image_path(image_id):
        for folder in IMAGES_DIR:
            path = os.path.join(folder, f"{image_id}.jpg")
            if os.path.exists(path):
                return path
        return None

    df['image_path'] = df['image_id'].apply(find_image_path)
    df = df.dropna(subset=['image_path']).reset_index(drop=True)

    label_to_idx = {name: i for i, name in enumerate(CLASS_NAMES)}
    df['label'] = df['dx'].map(label_to_idx)

    print("Phân bố lớp trong toàn bộ dữ liệu:")
    print(df['dx'].value_counts())
    print(f"\nTỷ lệ lớp lớn nhất / nhỏ nhất: "
          f"{df['dx'].value_counts().max() / df['dx'].value_counts().min():.1f}x")

    return df


def stratified_split(df):
    """
    Chia train/val/test theo tỷ lệ 70/15/15, GIỮ NGUYÊN tỷ lệ lớp
    ở mỗi tập bằng stratify=df['label'].
    Quan trọng: nếu không stratify, val/test có thể ngẫu nhiên có rất ít
    ảnh của lớp hiếm -> đánh giá sai lệch.
    """
    train_df, temp_df = train_test_split(
        df, test_size=0.30, stratify=df['label'], random_state=SEED
    )
    val_df, test_df = train_test_split(
        temp_df, test_size=0.50, stratify=temp_df['label'], random_state=SEED
    )

    print(f"\nTrain: {len(train_df)} | Val: {len(val_df)} | Test: {len(test_df)}")
    return train_df.reset_index(drop=True), val_df.reset_index(drop=True), test_df.reset_index(drop=True)


# ============================================
# BƯỚC 2: TÍNH CLASS WEIGHTS (chìa khóa xử lý mất cân bằng)
# ============================================
def get_class_weights(train_df):
    """
    Tính trọng số nghịch đảo tần suất lớp.
    Lớp hiếm (vd: df, vasc) sẽ có weight cao hơn nhiều lần
    -> loss bị phạt nặng hơn khi model đoán sai các lớp này
    -> buộc model phải học đặc trưng thật thay vì đoán bừa lớp đông.
    """
    labels = train_df['label'].values
    weights = compute_class_weight(
        class_weight='balanced',
        classes=np.arange(NUM_CLASSES),
        y=labels
    )
    class_weight_dict = {i: w for i, w in enumerate(weights)}

    print("\nClass weights (lớp hiếm sẽ có số cao hơn):")
    for i, name in enumerate(CLASS_NAMES):
        print(f"  {name}: {class_weight_dict[i]:.2f}")

    return class_weight_dict


# ============================================
# BƯỚC 3: DATA PIPELINE VỚI AUGMENTATION MẠNH HƠN CHO LỚP HIẾM
# ============================================
def oversample_minority(train_df, target_ratio=0.4):
    """
    Oversample các lớp hiếm bằng cách lặp lại record (ảnh sẽ được augment
    ngẫu nhiên khác nhau mỗi epoch nên KHÔNG bị duplicate y hệt).
    target_ratio: lớp hiếm sẽ được nhân lên tới tối thiểu target_ratio
    của lớp đông nhất.
    """
    counts = train_df['label'].value_counts()
    max_count = counts.max()
    target_count = int(max_count * target_ratio)

    dfs = [train_df]
    for label, count in counts.items():
        if count < target_count:
            subset = train_df[train_df['label'] == label]
            n_repeat = (target_count // count)
            for _ in range(n_repeat - 1):
                dfs.append(subset)

    balanced_df = pd.concat(dfs, ignore_index=True)
    balanced_df = balanced_df.sample(frac=1, random_state=SEED).reset_index(drop=True)

    print(f"\nSau oversampling: {len(balanced_df)} ảnh (từ {len(train_df)})")
    print(balanced_df['dx'].value_counts())
    return balanced_df


def load_and_preprocess(image_path, label, training=False):
    image = tf.io.read_file(image_path)
    image = tf.image.decode_jpeg(image, channels=3)
    image = tf.image.resize(image, [IMG_SIZE, IMG_SIZE])

    if training:
        image = tf.image.random_flip_left_right(image)
        image = tf.image.random_flip_up_down(image)
        image = tf.image.random_brightness(image, max_delta=0.15)
        image = tf.image.random_contrast(image, lower=0.85, upper=1.15)
        image = tf.image.random_saturation(image, lower=0.85, upper=1.15)
        # Xoay ngẫu nhiên nhẹ - tổn thương da không có hướng cố định
        angle = tf.random.uniform([], -0.2, 0.2)
        image = tf.image.rot90(image, k=tf.random.uniform([], 0, 4, dtype=tf.int32))

    image = preprocess_input(image)
    label = tf.one_hot(label, NUM_CLASSES)
    return image, label


def make_dataset(df, training=False, batch_size=BATCH_SIZE):
    paths = df['image_path'].values
    labels = df['label'].values

    ds = tf.data.Dataset.from_tensor_slices((paths, labels))
    if training:
        ds = ds.shuffle(buffer_size=len(df), seed=SEED)

    ds = ds.map(
        lambda p, l: load_and_preprocess(p, l, training=training),
        num_parallel_calls=tf.data.AUTOTUNE
    )
    ds = ds.batch(batch_size).prefetch(tf.data.AUTOTUNE)
    return ds


# ============================================
# BƯỚC 4: XÂY DỰNG MODEL RESNET50
# ============================================
def build_model():
    base_model = ResNet50(
        weights='imagenet',
        include_top=False,
        input_shape=(IMG_SIZE, IMG_SIZE, 3)
    )
    base_model.trainable = False  # Giai đoạn 1: freeze toàn bộ backbone

    inputs = layers.Input(shape=(IMG_SIZE, IMG_SIZE, 3))
    x = base_model(inputs, training=False)
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.Dropout(0.4)(x)
    x = layers.Dense(256, activation='relu')(x)
    x = layers.BatchNormalization()(x)
    x = layers.Dropout(0.3)(x)
    outputs = layers.Dense(NUM_CLASSES, activation='softmax')(x)

    model = models.Model(inputs, outputs)
    return model, base_model


# ============================================
# METRIC TÙY CHỈNH: MACRO F1 (quan trọng hơn Accuracy rất nhiều)
# ============================================
class MacroF1Callback(callbacks.Callback):
    """
    Tính Macro F1 trên tập validation sau mỗi epoch.
    Macro F1 = trung bình F1 của TỪNG lớp (không quan tâm lớp đông/hiếm)
    -> Nếu model chỉ đoán "nv", Macro F1 sẽ rất THẤP dù Accuracy cao
    -> Đây là con số thật để đánh giá model có học đều các lớp hay không.
    """
    def __init__(self, val_ds, val_labels):
        super().__init__()
        self.val_ds = val_ds
        self.val_labels = val_labels
        self.best_f1 = 0

    def on_epoch_end(self, epoch, logs=None):
        preds = self.model.predict(self.val_ds, verbose=0)
        pred_labels = np.argmax(preds, axis=1)
        macro_f1 = f1_score(self.val_labels, pred_labels, average='macro')
        logs['val_macro_f1'] = macro_f1
        print(f" - val_macro_f1: {macro_f1:.4f}")

        if macro_f1 > self.best_f1:
            self.best_f1 = macro_f1


# ============================================
# MAIN TRAINING PIPELINE
# ============================================
def main():
    # --- Bước 1: Data ---
    df = build_dataframe()
    train_df, val_df, test_df = stratified_split(df)

    # Lưu lại split để dùng cho evaluate.py (đảm bảo cùng 1 test set)
    train_df.to_csv('dataset/HAM10000/metadata/train_split.csv', index=False)
    val_df.to_csv('dataset/HAM10000/metadata/val_split.csv', index=False)
    test_df.to_csv('dataset/HAM10000/metadata/test_split.csv', index=False)

    # Oversample nhẹ lớp hiếm TRƯỚC khi tính class_weight
    train_df_balanced = oversample_minority(train_df, target_ratio=0.35)

    class_weight_dict = get_class_weights(train_df_balanced)

    train_ds = make_dataset(train_df_balanced, training=True)
    val_ds = make_dataset(val_df, training=False)
    val_labels = val_df['label'].values

    # --- Bước 2: Model ---
    model, base_model = build_model()

    # ============================================
    # GIAI ĐOẠN 1: Train chỉ phần head (backbone freeze)
    # ============================================
    print("\n" + "=" * 50)
    print("GIAI ĐOẠN 1: Train head (backbone frozen)")
    print("=" * 50)

    model.compile(
        optimizer=optimizers.Adam(learning_rate=1e-3),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )

    callbacks_stage1 = [
        MacroF1Callback(val_ds, val_labels),
        callbacks.EarlyStopping(
            monitor='val_macro_f1', mode='max', patience=5,
            restore_best_weights=True, verbose=1
        ),
        callbacks.ReduceLROnPlateau(
            monitor='val_macro_f1', mode='max', factor=0.5,
            patience=3, min_lr=1e-6, verbose=1
        ),
    ]

    model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=15,
        class_weight=class_weight_dict,
        callbacks=callbacks_stage1,
        verbose=1
    )

    # ============================================D
    # GIAI ĐOẠN 2: Fine-tune - mở khóa vài block cuối ResNet50
    # ============================================
    print("\n" + "=" * 50)
    print("GIAI ĐOẠN 2: Fine-tune (unfreeze block cuối)")
    print("=" * 50)

    base_model.trainable = True
    # Chỉ mở khóa từ layer thứ 143 trở đi (conv5 block của ResNet50)
    # Giữ nguyên các layer đầu để không phá vỡ đặc trưng tổng quát đã học từ ImageNet
    for layer in base_model.layers[:143]:
        layer.trainable = False

    model.compile(
        optimizer=optimizers.Adam(learning_rate=1e-5),  # LR rất nhỏ khi fine-tune
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )

    checkpoint = callbacks.ModelCheckpoint(
        BEST_MODEL_PATH,
        monitor='val_macro_f1', mode='max',
        save_best_only=True, verbose=1
    )

    callbacks_stage2 = [
        MacroF1Callback(val_ds, val_labels),
        checkpoint,
        callbacks.EarlyStopping(
            monitor='val_macro_f1', mode='max', patience=7,
            restore_best_weights=True, verbose=1
        ),
        callbacks.ReduceLROnPlateau(
            monitor='val_macro_f1', mode='max', factor=0.5,
            patience=3, min_lr=1e-7, verbose=1
        ),
    ]

    history = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=30,
        class_weight=class_weight_dict,
        callbacks=callbacks_stage2,
        verbose=1
    )

    # --- Lưu model cuối cùng ---
    model.save(FINAL_MODEL_PATH)
    print(f"\n✅ Đã lưu model tại: {FINAL_MODEL_PATH}")
    print(f"✅ Best model (theo Macro F1) tại: {BEST_MODEL_PATH}")

    # Lưu lịch sử train để vẽ biểu đồ sau này
    with open(os.path.join(MODEL_DIR, 'training_history.json'), 'w') as f:
        json.dump(history.history, f, indent=2)


if __name__ == '__main__':
    main()