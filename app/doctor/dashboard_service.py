from app.database.db import db

from app.models.patient import Patient
from app.models.examination import Examination
from app.models.ai_prediction import AIPrediction
from app.models.doctor_report import DoctorReport
from app.models.ai_prediction_detail import AIPredictionDetail


class DashboardService:

    @staticmethod
    def get_dashboard():

        patient_count = Patient.query.count()

        exam_count = Examination.query.count()

        ai_count = AIPrediction.query.count()

        report_count = DoctorReport.query.count()

        recent_predictions = (
            AIPrediction.query
            .order_by(AIPrediction.created_at.desc())
            .limit(5)
            .all()
        )

        disease_stats = (
            db.session.query(
                AIPredictionDetail.predicted_class,
                db.func.count(AIPredictionDetail.detail_id)
            )
            .group_by(
                AIPredictionDetail.predicted_class
            )
            .all()
        )

        return {

            "patient_count": patient_count,

            "exam_count": exam_count,

            "ai_count": ai_count,

            "report_count": report_count,

            "recent_predictions": recent_predictions,

            "disease_stats": disease_stats

        }