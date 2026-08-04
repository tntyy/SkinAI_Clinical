import cv2
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

from tensorflow.keras.models import load_model
from tensorflow.keras.applications.resnet50 import preprocess_input

# ===================================================
# CONFIG
# ===================================================

IMAGE_PATH = "test.jpg"
MODEL_PATH = "model/skin_model.keras"

IMG_SIZE = 224

CLASS_NAMES = [
    "akiec",
    "bcc",
    "bkl",
    "df",
    "mel",
    "nv",
    "vasc"
]

# ===================================================
# LOAD MODEL
# ===================================================

model = load_model(MODEL_PATH)

# Backbone ResNet50
base_model = model.get_layer("resnet50")

# ===================================================
# LOAD IMAGE
# ===================================================

image = cv2.imread(IMAGE_PATH)

image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

img = cv2.resize(image_rgb, (IMG_SIZE, IMG_SIZE))

x = np.expand_dims(img, axis=0)

x = preprocess_input(x)

# ===================================================
# PREDICT
# ===================================================

pred = model.predict(x, verbose=0)

pred_index = np.argmax(pred[0])

print("Prediction:", CLASS_NAMES[pred_index])
print("Confidence:", pred[0][pred_index])

# ===================================================
# FORWARD PASS
# ===================================================

with tf.GradientTape() as tape:

    # đi qua backbone trước
    conv_output = base_model(x)

    tape.watch(conv_output)

    # đi qua head của model
    y = model.layers[2](conv_output)
    y = model.layers[3](y)
    y = model.layers[4](y)
    y = model.layers[5](y)
    y = model.layers[6](y)
    preds = model.layers[7](y)

    loss = preds[:, pred_index]

# ===================================================
# Gradient
# ===================================================

grads = tape.gradient(loss, conv_output)

pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))

conv_output = conv_output[0]

heatmap = tf.reduce_sum(conv_output * pooled_grads, axis=-1)

heatmap = tf.maximum(heatmap, 0)

heatmap /= tf.reduce_max(heatmap)

heatmap = heatmap.numpy()

# ===================================================
# Resize
# ===================================================

heatmap = cv2.resize(
    heatmap,
    (image.shape[1], image.shape[0])
)

heatmap = np.uint8(255 * heatmap)

heatmap = cv2.applyColorMap(
    heatmap,
    cv2.COLORMAP_JET
)

overlay = cv2.addWeighted(
    image,
    0.6,
    heatmap,
    0.4,
    0
)

overlay = cv2.cvtColor(
    overlay,
    cv2.COLOR_BGR2RGB
)

# ===================================================
# SHOW
# ===================================================

plt.figure(figsize=(10,5))

plt.subplot(1,2,1)
plt.imshow(image_rgb)
plt.title("Original")
plt.axis("off")

plt.subplot(1,2,2)
plt.imshow(overlay)
plt.title("GradCAM")
plt.axis("off")

plt.show()