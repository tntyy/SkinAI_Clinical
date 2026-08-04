from app.database.db import db

from app.models.ai_prediction import AIPrediction
from app.models.ai_prediction_detail import AIPredictionDetail
from app.models.ai_heatmap import AIHeatmap

class AIRepository:

    @staticmethod
    def save_prediction(
            lesion_image_id,
            model_name,
            version,
            inference_time
    ):
        prediction = AIPrediction(

            image_id=lesion_image_id,

            model_name=model_name,

            model_version=version,

            inference_time=inference_time

        )

        db.session.add(prediction)
        db.session.commit()

        return prediction

    @staticmethod
    def save_detail(
            prediction_id,
            lesion_type,
            probability,
            ranking
    ):
        detail = AIPredictionDetail(

            prediction_id=prediction_id,

            rank=ranking,

            predicted_class=lesion_type,

            confidence=probability

        )

        db.session.add(detail)
        db.session.commit()

        return detail

    @staticmethod
    def save_heatmap(
            prediction_id,
            heatmap_path,
            overlay_path):
        row = AIHeatmap(

            prediction_id=prediction_id,

            heatmap_path=heatmap_path,

            overlay_path=overlay_path

        )

        db.session.add(row)

        db.session.commit()

        return row