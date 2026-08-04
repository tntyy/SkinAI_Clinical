from app.doctor.repositories import DoctorReportRepository
from app.models.patient import Patient
from app.models.examination import Examination
from app.models.ai_prediction import AIPrediction
from app.models.doctor_report import DoctorReport
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