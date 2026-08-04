import numpy as np

from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import preprocess_input

from app.ai.load_model import get_model

IMAGE_SIZE = (224,224)


def predict_image(image_path):

    model = get_model()

    img = image.load_img(
        image_path,
        target_size=IMAGE_SIZE
    )

    img = image.img_to_array(img)

    img = np.expand_dims(img, axis=0)

    img = preprocess_input(img)

    prediction = model.predict(
        img,
        verbose=0
    )

    return prediction[0]