"""
prepare_dataset.py
Chuẩn bị HAM10000: đọc metadata, ghép ảnh, chia train/valid/test.

Đã sửa 2 vấn đề so với bản gốc:
1. Lỗi thụt lề khiến copy_images() không bao giờ được gọi.
2. Data leakage: split theo lesion_id (không phải image_id) để đảm bảo
   các ảnh của CÙNG một tổn thương không bị chia vào cả train và test.
"""

import os
import shutil

import pandas as pd
from sklearn.model_selection import train_test_split


BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DATASET_DIR = os.path.join(BASE_DIR, "dataset", "HAM10000")

IMAGE_DIR1 = os.path.join(DATASET_DIR, "images", "HAM10000_images_part_1")
IMAGE_DIR2 = os.path.join(DATASET_DIR, "images", "HAM10000_images_part_2")

METADATA = os.path.join(DATASET_DIR, "metadata", "HAM10000_metadata.csv")

TRAIN_DIR = os.path.join(DATASET_DIR, "train")
VALID_DIR = os.path.join(DATASET_DIR, "valid")
TEST_DIR = os.path.join(DATASET_DIR, "test")

RANDOM_STATE = 42


def get_image_path(image_id):
    """Tìm đường dẫn ảnh, kiểm tra tồn tại ở cả 2 thư mục."""
    path1 = os.path.join(IMAGE_DIR1, image_id + ".jpg")
    if os.path.exists(path1):
        return path1

    path2 = os.path.join(IMAGE_DIR2, image_id + ".jpg")
    if os.path.exists(path2):
        return path2

    return None  # Không tìm thấy -> sẽ bị loại bỏ, không crash chương trình


def split_by_lesion(metadata):
    """
    Chia train/valid/test theo lesion_id (KHÔNG theo image_id).

    Lý do: HAM10000 có nhiều ảnh chụp cùng 1 tổn thương (cùng lesion_id).
    Nếu chia theo image_id, ảnh của cùng 1 tổn thương có thể rơi vào cả
    train và test -> model "nhớ" tổn thương đó từ lúc train -> đánh giá
    trên test bị SAI (accuracy cao giả tạo, không phản ánh thực tế).

    Cách làm: lấy nhãn đại diện cho mỗi lesion_id (nhãn dx thường giống
    nhau trong cùng 1 lesion), stratify theo đó, rồi map ngược lại toàn
    bộ ảnh thuộc các lesion_id đã được gán vào từng tập.
    """
    lesion_df = metadata.drop_duplicates(subset="lesion_id")[["lesion_id", "dx"]]

    train_lesions, test_lesions = train_test_split(
        lesion_df,
        test_size=0.15,
        random_state=RANDOM_STATE,
        stratify=lesion_df["dx"]
    )
    train_lesions, valid_lesions = train_test_split(
        train_lesions,
        test_size=0.15,
        random_state=RANDOM_STATE,
        stratify=train_lesions["dx"]
    )

    train_ids = set(train_lesions["lesion_id"])
    valid_ids = set(valid_lesions["lesion_id"])
    test_ids = set(test_lesions["lesion_id"])

    train_df = metadata[metadata["lesion_id"].isin(train_ids)].reset_index(drop=True)
    valid_df = metadata[metadata["lesion_id"].isin(valid_ids)].reset_index(drop=True)
    test_df = metadata[metadata["lesion_id"].isin(test_ids)].reset_index(drop=True)

    return train_df, valid_df, test_df


def make_class_folders(classes):
    for folder in [TRAIN_DIR, VALID_DIR, TEST_DIR]:
        os.makedirs(folder, exist_ok=True)
        for cls in classes:
            os.makedirs(os.path.join(folder, cls), exist_ok=True)


def copy_images(df, destination):
    """Copy ảnh vào thư mục theo lớp. Bỏ qua và cảnh báo nếu ảnh không tồn tại."""
    missing = 0
    for _, row in df.iterrows():
        if row["path"] is None:
            missing += 1
            continue

        dest_path = os.path.join(destination, row["dx"], row["image_id"] + ".jpg")
        shutil.copy(row["path"], dest_path)

    if missing > 0:
        print(f"  ⚠ Cảnh báo: {missing} ảnh không tìm thấy, đã bỏ qua ({destination})")


def main():
    metadata = pd.read_csv(METADATA)
    print(metadata.head())
    print("Tổng số ảnh trong metadata:", metadata.shape[0])
    print("Số lesion_id duy nhất:", metadata["lesion_id"].nunique())

    metadata["path"] = metadata["image_id"].apply(get_image_path)

    n_missing = metadata["path"].isna().sum()
    if n_missing > 0:
        print(f"⚠ Có {n_missing} ảnh không tìm thấy trong 2 thư mục ảnh.")

    print(metadata[["image_id", "lesion_id", "path"]].head())

    train_df, valid_df, test_df = split_by_lesion(metadata)

    classes = sorted(metadata["dx"].unique())
    make_class_folders(classes)

    copy_images(train_df, TRAIN_DIR)
    copy_images(valid_df, VALID_DIR)
    copy_images(test_df, TEST_DIR)

    print("=" * 50)
    print("Dataset prepared successfully!")
    print("=" * 50)
    print("Train      :", len(train_df))
    print("Validation :", len(valid_df))
    print("Test       :", len(test_df))
    print()
    print("Phân bố lớp - Train:")
    print(train_df["dx"].value_counts())
    print("\nPhân bố lớp - Valid:")
    print(valid_df["dx"].value_counts())
    print("\nPhân bố lớp - Test:")
    print(test_df["dx"].value_counts())

    # Kiểm tra chéo: đảm bảo không có lesion_id nào lọt vào 2 tập cùng lúc
    overlap_train_test = set(train_df["lesion_id"]) & set(test_df["lesion_id"])
    overlap_train_valid = set(train_df["lesion_id"]) & set(valid_df["lesion_id"])
    assert len(overlap_train_test) == 0, "LỖI: có lesion_id trùng giữa train và test!"
    assert len(overlap_train_valid) == 0, "LỖI: có lesion_id trùng giữa train và valid!"
    print("\n✅ Đã kiểm tra: không có lesion_id nào bị trùng giữa các tập.")


if __name__ == "__main__":
    main()