from flask_login import current_user

from app.examination.repositories import ExaminationRepository

from app.models.examination import Examination
from app.models.doctor_profile import DoctorProfile


class ExaminationService:

    @staticmethod
    def create_examination(patient_id, form):

        doctor = DoctorProfile.query.filter_by(
            user_id=current_user.user_id
        ).first()

        examination = Examination(

            patient_id=patient_id,

            doctor_id=doctor.doctor_id,

            chief_complaint=form.chief_complaint.data,

            note=form.note.data

        )

        return ExaminationRepository.create(
            examination
        )

    @staticmethod
    def get_patient_examinations(patient_id):
        return ExaminationRepository.get_all_by_patient(
            patient_id
        )

    @staticmethod
    def get_detail(exam_id):
        return ExaminationRepository.get_by_id(
            exam_id
        )