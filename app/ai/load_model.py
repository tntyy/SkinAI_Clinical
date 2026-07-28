from tensorflow.keras.models import load_model

import os

MODEL = None


def get_model():

    global MODEL

    if MODEL is None:

        model_path = os.path.join(
            "model",
            "skin_model.keras"
        )

        MODEL = load_model(model_path)

    return MODEL