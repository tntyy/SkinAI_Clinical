from tensorflow.keras.models import load_model
import os

MODEL = None

def get_model():
    global MODEL

    if MODEL is None:

        model_path = os.path.join(
            "model",
            "best_model.keras"
        )

        MODEL = load_model(model_path)

        print("\n========== MODEL ==========")

        for i, layer in enumerate(MODEL.layers):
            print(i, layer.name, type(layer).__name__)

        print("===========================\n")

    return MODEL