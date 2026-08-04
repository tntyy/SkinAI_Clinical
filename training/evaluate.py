import os
import numpy as np
import pandas as pd
import tensorflow as tf

from tensorflow.keras.models import load_model
from tensorflow.keras.applications.resnet50 import preprocess_input

from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)

IMG_SIZE = 224
BATCH_SIZE = 32

MODEL_PATH = "model/best_model.keras"

TEST_CSV = "dataset/HAM10000/metadata/test_split.csv"

CLASS_NAMES = [
    "akiec",
    "bcc",
    "bkl",
    "df",
    "mel",
    "nv",
    "vasc"
]


def load_image(path):

    image = tf.io.read_file(path)

    image = tf.image.decode_jpeg(
        image,
        channels=3
    )

    image = tf.image.resize(
        image,
        (IMG_SIZE, IMG_SIZE)
    )

    image = preprocess_input(image)

    return image


df = pd.read_csv(TEST_CSV)

images = np.array([
    load_image(x).numpy()
    for x in df["image_path"]
])

labels = df["label"].values

model = load_model(MODEL_PATH)

pred = model.predict(images)

pred_labels = np.argmax(pred, axis=1)

print("=" * 60)

print("Accuracy :", accuracy_score(labels, pred_labels))

print("Precision:", precision_score(
    labels,
    pred_labels,
    average="macro"
))

print("Recall   :", recall_score(
    labels,
    pred_labels,
    average="macro"
))

print("Macro F1 :", f1_score(
    labels,
    pred_labels,
    average="macro"
))

print("=" * 60)

print(classification_report(
    labels,
    pred_labels,
    target_names=CLASS_NAMES
))

print("=" * 60)

print(confusion_matrix(
    labels,
    pred_labels
))