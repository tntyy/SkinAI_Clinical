from app.database.db import db

from app.models.patient import Patient
from app.models.examination import Examination
from app.models.ai_prediction import AIPrediction
from app.models.doctor_report import DoctorReport
from app.models.ai_prediction_detail import AIPredictionDetail
from flask_login import current_user
from app.models.lesion_image import LesionImage

class DashboardService:

    @staticmethod
    def get_dashboard():
        doctor_id = current_user.doctor_profile.doctor_id

        patient_count = Patient.query.filter_by(
            created_by_doctor=doctor_id
        ).count()

        exam_count = Examination.query.filter_by(
            doctor_id=doctor_id
        ).count()

        ai_count = (
            AIPrediction.query
            .join(LesionImage, AIPrediction.image_id == LesionImage.image_id)
            .join(Examination, LesionImage.exam_id == Examination.exam_id)
            .filter(Examination.doctor_id == doctor_id)
            .count()
        )

        report_count = DoctorReport.query.filter_by(
            doctor_id=doctor_id
        ).count()

        recent_predictions = (
            AIPrediction.query
            .join(LesionImage, AIPrediction.image_id == LesionImage.image_id)
            .join(Examination, LesionImage.exam_id == Examination.exam_id)
            .filter(Examination.doctor_id == doctor_id)
            .order_by(AIPrediction.created_at.desc())
            .limit(5)
            .all()
        )

        disease_stats = (
            db.session.query(
                AIPredictionDetail.predicted_class,
                db.func.count(AIPredictionDetail.detail_id)
            )
            .join(AIPrediction, AIPredictionDetail.prediction_id == AIPrediction.prediction_id)
            .join(LesionImage, AIPrediction.image_id == LesionImage.image_id)
            .join(Examination, LesionImage.exam_id == Examination.exam_id)
            .filter(Examination.doctor_id == doctor_id)
            .group_by(AIPredictionDetail.predicted_class)
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