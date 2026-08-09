from app.database.db import db

from app.models.ai_prediction import AIPrediction
from app.models.ai_prediction_detail import AIPredictionDetail
from app.models.ai_heatmap import AIHeatmap
from app.models.disease import Disease


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

        db.session.add(prediction)

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

        db.session.add(detail)

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

        db.session.add(row)

        db.session.commit()

        return row

    # ======================================================
    # GET HEATMAP
    # ======================================================

    @staticmethod
    def get_heatmap(prediction_id):

        return (
            AIHeatmap.query
            .filter_by(
                prediction_id=prediction_id
            )
            .order_by(
                AIHeatmap.heatmap_id.desc()
            )
            .first()
        )

    # ======================================================
    # GET PREDICTION BY IMAGE
    # ======================================================

    @staticmethod
    def get_prediction_by_image(image_id):

        return (
            AIPrediction.query
            .filter_by(
                image_id=image_id
            )
            .order_by(
                AIPrediction.prediction_id.desc()
            )
            .first()
        )

    # ======================================================
    # GET PREDICTION DETAILS
    # ======================================================

    @staticmethod
    def get_prediction_details(prediction_id):

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
                AIPredictionDetail.prediction_id
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
    # GET PREDICTION FOR CHAT
    # ======================================================

    @classmethod
    def get_prediction_for_chat(
        cls,
        prediction_id
    ):

        prediction = (
            AIPrediction.query
            .filter_by(
                prediction_id=prediction_id
            )
            .first()
        )

        if prediction is None:
            return None

        results = cls.get_prediction_details(
            prediction.prediction_id
        )

        if not results:
            return None

        heatmap = cls.get_heatmap(
            prediction.prediction_id
        )

        top_result = results[0]

        predicted_class = (
            top_result.get("predicted_class")
        )

        confidence = float(
            top_result.get("confidence") or 0
        )

        disease = (
            top_result.get("disease")
        )

        return {

            "prediction_id":
                prediction.prediction_id,

            "prediction":
                predicted_class,

            "predicted_class":
                predicted_class,

            "confidence":
                confidence,

            "disease":
                (
                    disease.disease_name_vi
                    if disease
                    else predicted_class
                ),

            "disease_name":
                (
                    disease.disease_name
                    if disease
                    else None
                ),

            "disease_name_vi":
                (
                    disease.disease_name_vi
                    if disease
                    else None
                ),

            "disease_code":
                (
                    disease.disease_code
                    if disease
                    else predicted_class
                ),

            "icd10":
                (
                    disease.icd10_code
                    if disease
                    else None
                ),

            "icd10_code":
                (
                    disease.icd10_code
                    if disease
                    else None
                ),

            "risk":
                (
                    disease.risk_level
                    if disease
                    else None
                ),

            "risk_level":
                (
                    disease.risk_level
                    if disease
                    else None
                ),

            "overview":
                (
                    disease.overview
                    if disease
                    else None
                ),

            "symptoms":
                (
                    disease.symptoms
                    if disease
                    else None
                ),

            "treatment":
                (
                    disease.treatment
                    if disease
                    else None
                ),

            "prevention":
                (
                    disease.prevention
                    if disease
                    else None
                ),

            "follow_up":
                (
                    disease.follow_up
                    if disease
                    else None
                ),

            "heatmap":
                bool(heatmap),

            "heatmap_path":
                (
                    heatmap.heatmap_path
                    if heatmap
                    else None
                ),

            "overlay_path":
                (
                    heatmap.overlay_path
                    if heatmap
                    else None
                )
        }

    # ======================================================
    # GET LATEST PREDICTION FOR CHAT
    # ======================================================

    @classmethod
    def get_latest_prediction_for_chat(cls):

        prediction = (
            AIPrediction.query
            .order_by(
                AIPrediction.prediction_id.desc()
            )
            .first()
        )

        if prediction is None:
            return None

        results = cls.get_prediction_details(
            prediction.prediction_id
        )

        if not results:
            return None

        top_result = results[0]

        predicted_class = (
            top_result.get(
                "predicted_class"
            )
        )

        confidence = float(
            top_result.get(
                "confidence"
            ) or 0
        )

        disease = top_result.get(
            "disease"
        )

        heatmap = cls.get_heatmap(
            prediction.prediction_id
        )

        return {

            "prediction_id":
                prediction.prediction_id,

            "prediction":
                predicted_class,

            "predicted_class":
                predicted_class,

            "confidence":
                confidence,

            "disease":
                (
                    disease.disease_name_vi
                    if disease
                    else predicted_class
                ),

            "disease_name":
                (
                    disease.disease_name
                    if disease
                    else None
                ),

            "disease_name_vi":
                (
                    disease.disease_name_vi
                    if disease
                    else None
                ),

            "disease_code":
                (
                    disease.disease_code
                    if disease
                    else predicted_class
                ),

            "icd10":
                (
                    disease.icd10_code
                    if disease
                    else None
                ),

            "icd10_code":
                (
                    disease.icd10_code
                    if disease
                    else None
                ),

            "risk":
                (
                    disease.risk_level
                    if disease
                    else None
                ),

            "risk_level":
                (
                    disease.risk_level
                    if disease
                    else None
                ),

            "overview":
                (
                    disease.overview
                    if disease
                    else None
                ),

            "symptoms":
                (
                    disease.symptoms
                    if disease
                    else None
                ),

            "treatment":
                (
                    disease.treatment
                    if disease
                    else None
                ),

            "prevention":
                (
                    disease.prevention
                    if disease
                    else None
                ),

            "follow_up":
                (
                    disease.follow_up
                    if disease
                    else None
                ),

            "heatmap":
                bool(heatmap),

            "heatmap_path":
                (
                    heatmap.heatmap_path
                    if heatmap
                    else None
                ),

            "overlay_path":
                (
                    heatmap.overlay_path
                    if heatmap
                    else None
                ),

            "results":
                results
        }
