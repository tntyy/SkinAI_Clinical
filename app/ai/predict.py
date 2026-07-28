import numpy as np

from tensorflow.keras.preprocessing import image

from app.ai.load_model import get_model

IMAGE_SIZE = (224, 224)

CLASS_NAMES = [

    "akiec",

    "bcc",

    "bkl",

    "df",

    "mel",

    "nv",

    "vasc"

]


def predict_image(image_path):

    model = get_model()

    img = image.load_img(

        image_path,

        target_size=IMAGE_SIZE

    )

    img = image.img_to_array(img)

    img = img / 255.0

    img = np.expand_dims(

        img,

        axis=0

    )

    prediction = model.predict(img)

    return prediction[0]