from app.doctor.repositories import DoctorReportRepository
from app.models.patient import Patient
from app.models.examination import Examination
from app.models.ai_prediction import AIPrediction
from app.models.doctor_report import DoctorReport
from app.models.lesion_image import LesionImage
from app.models.ai_prediction_detail import AIPredictionDetail
from app.database.db import db
from flask_login import current_user

class DoctorReportService:

    @staticmethod
    def confirm(

            exam_id,
            doctor_id,
            prediction_id,
            form

    ):

        return DoctorReportRepository.save(

            exam_id,

            doctor_id,

            prediction_id,

            form.diagnosis.data,

            form.treatment.data,

            form.note.data

        )
    @staticmethod
    def get_report(exam_id):

        return DoctorReportRepository.get_report_by_exam(
            exam_id
        )

    @staticmethod
    def prediction_history(
            patient_id,
            search=None,
            date_from=None,
            date_to=None
    ):
        return DoctorReportRepository.get_prediction_history(
            patient_id=patient_id,
            search=search,
            date_from=date_from,
            date_to=date_to
        )

    @staticmethod
    def report_dashboard():
        doctor_id = current_user.doctor_profile.doctor_id

        total_patients = Patient.query.filter_by(
            created_by_doctor=doctor_id
        ).count()

        total_exam = Examination.query.filter_by(
            doctor_id=doctor_id
        ).count()

        total_images = (
            LesionImage.query
            .join(Examination, LesionImage.exam_id == Examination.exam_id)
            .filter(Examination.doctor_id == doctor_id)
            .count()
        )

        valid_images = (
            LesionImage.query
            .join(Examination, LesionImage.exam_id == Examination.exam_id)
            .filter(
                Examination.doctor_id == doctor_id,
                LesionImage.is_valid == True
            )
            .count()
        )

        blur_images = (
            LesionImage.query
            .join(Examination, LesionImage.exam_id == Examination.exam_id)
            .filter(
                Examination.doctor_id == doctor_id,
                LesionImage.is_valid == False
            )
            .count()
        )

        total_predictions = (
            AIPrediction.query
            .join(LesionImage, AIPrediction.image_id == LesionImage.image_id)
            .join(Examination, LesionImage.exam_id == Examination.exam_id)
            .filter(Examination.doctor_id == doctor_id)
            .count()
        )

        total_reports = DoctorReport.query.filter_by(
            doctor_id=doctor_id
        ).count()

        return {
            "patients": total_patients,
            "examinations": total_exam,
            "images": total_images,
            "valid_images": valid_images,
            "blur_images": blur_images,
            "predictions": total_predictions,
            "reports": total_reports
        }