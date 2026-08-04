import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import preprocess_input

IMG_SIZE = (224, 224)


def generate_gradcam(model, image_path):

    img = image.load_img(
        image_path,
        target_size=IMG_SIZE
    )

    img = image.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = preprocess_input(img)

    # Backbone ResNet50
    base_model = model.layers[1]

    # Layer cuối của ResNet50
    last_conv_layer = base_model.get_layer("conv5_block3_out")

    grad_model = tf.keras.models.Model(
        inputs=base_model.input,
        outputs=[
            last_conv_layer.output,
            base_model.output
        ]
    )

    classifier_input = tf.keras.Input(shape=base_model.output.shape[1:])

    x = classifier_input

    for layer in model.layers[2:]:
        x = layer(x)

    classifier_model = tf.keras.Model(
        classifier_input,
        x
    )

    with tf.GradientTape() as tape:

        conv_output, features = grad_model(img)

        tape.watch(conv_output)

        predictions = classifier_model(features)

        class_index = tf.argmax(predictions[0])

        loss = predictions[:, class_index]

    grads = tape.gradient(
        loss,
        conv_output
    )

    pooled_grads = tf.reduce_mean(
        grads,
        axis=(0, 1, 2)
    )

    conv_output = conv_output[0]

    heatmap = tf.reduce_sum(
        conv_output * pooled_grads,
        axis=-1
    )

    heatmap = tf.maximum(
        heatmap,
        0
    )

    heatmap /= (
        tf.reduce_max(heatmap) + 1e-8
    )

    return heatmap.numpy()