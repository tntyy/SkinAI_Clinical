from app.database.db import db

from app.models.ai_prediction import (
    AIPrediction
)

from app.models.ai_prediction_detail import (
    AIPredictionDetail
)

from app.models.ai_heatmap import (
    AIHeatmap
)

from app.models.disease import (
    Disease
)


class PredictionResult:

    def __init__(
        self,
        detail,
        disease
    ):

        self.detail = detail

        self.rank = detail.rank

        self.predicted_class = (
            detail.predicted_class
        )

        self.confidence = (
            detail.confidence
        )

        self.disease = disease


class AIRepository:

    # ======================================================
    # SAVE PREDICTION
    # ======================================================

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

        db.session.add(
            prediction
        )

        db.session.commit()

        return prediction

    # ======================================================
    # SAVE DETAIL
    # ======================================================

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

        db.session.add(
            detail
        )

        db.session.commit()

        return detail

    # ======================================================
    # SAVE HEATMAP
    # ======================================================

    @staticmethod
    def save_heatmap(
        prediction_id,
        heatmap_path,
        overlay_path
    ):

        row = AIHeatmap(

            prediction_id=prediction_id,

            heatmap_path=heatmap_path,

            overlay_path=overlay_path

        )

        db.session.add(
            row
        )

        db.session.commit()

        return row

    # ======================================================
    # GET PREDICTION BY IMAGE
    # ======================================================

    @staticmethod
    def get_prediction_by_image(
        image_id
    ):

        return (

            AIPrediction.query

            .filter_by(
                image_id=image_id
            )

            .order_by(
                AIPrediction
                .prediction_id
                .desc()
            )

            .first()

        )

    # ======================================================
    # GET PREDICTION DETAILS
    # ======================================================

    @staticmethod
    def get_prediction_details(
        prediction_id
    ):

        results = (

            db.session.query(

                AIPredictionDetail,

                Disease

            )

            .outerjoin(

                Disease,

                Disease.disease_code
                ==
                AIPredictionDetail.predicted_class

            )

            .filter(

                AIPredictionDetail
                .prediction_id
                ==
                prediction_id

            )

            .order_by(

                AIPredictionDetail.rank

            )

            .all()

        )

        data = []

        for detail, disease in results:

            data.append({

                "rank":
                    detail.rank,

                "predicted_class":
                    detail.predicted_class,

                "confidence":
                    detail.confidence,

                "disease":
                    disease

            })

        print(
            "✅ AI DETAILS:",
            data
        )

        return data

    # ======================================================
    # GET HEATMAP
    # ======================================================

    @staticmethod
    def get_heatmap(
        prediction_id
    ):

        heatmap = (

            AIHeatmap.query

            .filter_by(
                prediction_id=prediction_id
            )

            .first()

        )

        if heatmap:

            print(
                "✅ HEATMAP FOUND:",
                heatmap.heatmap_path
            )

            print(
                "✅ OVERLAY FOUND:",
                heatmap.overlay_path
            )

        else:

            print(
                "❌ NO HEATMAP:",
                prediction_id
            )

        return heatmap

    # ======================================================
    # GET LATEST PREDICTION
    # ======================================================

    @staticmethod
    def get_latest_prediction(
        image_id
    ):

        return (

            AIPrediction.query

            .filter_by(
                image_id=image_id
            )

            .order_by(
                AIPrediction
                .prediction_id
                .desc()
            )

            .first()

        )