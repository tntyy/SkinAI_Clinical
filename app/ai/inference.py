import time
import numpy as np

from app.ai.predict import predict_image
from app.ai.repositories import AIRepository
from app.models.disease import Disease
from app.ai.gradcam_service import create_heatmap

CLASSES = [
    "akiec",
    "bcc",
    "bkl",
    "df",
    "mel",
    "nv",
    "vasc"
]


def run_prediction(image_path, lesion_image_id):

    start = time.time()

    prediction = predict_image(image_path)

    inference_time = time.time() - start

    top3 = np.argsort(prediction)[::-1][:3]

    prediction_row = AIRepository.save_prediction(

        lesion_image_id=lesion_image_id,

        model_name="ResNet50",

        version="1.0",

        inference_time=inference_time

    )

    heatmap_path, overlay_path = create_heatmap(
        image_path
    )

    AIRepository.save_heatmap(

        prediction_row.prediction_id,

        heatmap_path,

        overlay_path

    )

    results=[]

    for rank, idx in enumerate(top3, start=1):

        disease = Disease.query.filter_by(
            disease_code=CLASSES[idx]
        ).first()

        AIRepository.save_detail(

            prediction_id=prediction_row.prediction_id,

            lesion_type=CLASSES[idx],

            probability=float(prediction[idx]),

            ranking=rank

        )

        results.append({

            "rank":rank,

            "class":CLASSES[idx],

            "confidence":float(prediction[idx]),

            "disease" : disease

        })

    return {

        "results": results,

        "heatmap_path": heatmap_path,

        "overlay_path": overlay_path

    }