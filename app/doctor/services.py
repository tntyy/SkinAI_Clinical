from app.doctor.repositories import DoctorReportRepository
from app.models.patient import Patient
from app.models.examination import Examination
from app.models.ai_prediction import AIPrediction
from app.models.doctor_report import DoctorReport
from app.models.lesion_image import LesionImage
from app.models.ai_prediction_detail import AIPredictionDetail
from app.database.db import db

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
    def prediction_history(patient_id):
        return DoctorReportRepository.get_prediction_history(
            patient_id
        )

    @staticmethod
    def report_dashboard():

        total_patients = Patient.query.count()

        total_exam = Examination.query.count()

        total_images = LesionImage.query.count()

        valid_images = LesionImage.query.filter_by(
            is_valid=True
        ).count()

        blur_images = LesionImage.query.filter_by(
            is_valid=False
        ).count()

        total_predictions = AIPrediction.query.count()

        total_reports = DoctorReport.query.count()

        return {

             "patients": total_patients,

            "examinations": total_exam,

            "images": total_images,

            "valid_images": valid_images,

            "blur_images": blur_images,

            "predictions": total_predictions,

            "reports": total_reports

        }