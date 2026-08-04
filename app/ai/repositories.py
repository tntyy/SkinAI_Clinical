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

    @staticmethod
    def get_prediction_by_image(image_id):
        return (
            AIPrediction.query
            .filter_by(image_id=image_id)
            .order_by(AIPrediction.prediction_id.desc())
            .first()
        )

    @staticmethod
    def get_prediction_details(prediction_id):
        return (
            AIPredictionDetail.query
            .filter_by(prediction_id=prediction_id)
            .order_by(AIPredictionDetail.rank)
            .all()
        )

    @staticmethod
    def get_heatmap(prediction_id):
        return AIHeatmap.query.filter_by(
            prediction_id=prediction_id
        ).first()