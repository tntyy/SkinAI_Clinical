import numpy as np

from app.ai.predict import predict_image


def run_prediction(image_path):

    prediction = predict_image(image_path)

    top3 = np.argsort(prediction)[::-1][:3]

    classes = [

        "akiec",

        "bcc",

        "bkl",

        "df",

        "mel",

        "nv",

        "vasc"

    ]

    results = []

    for rank, idx in enumerate(top3, start=1):

        results.append({

            "rank": rank,

            "class": classes[idx],

            "confidence": float(prediction[idx])

        })

    return results