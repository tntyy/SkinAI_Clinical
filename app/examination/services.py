from datetime import datetime

from flask_login import current_user

from app.models.examination import Examination
from app.examination.repositories import ExaminationRepository


class ExaminationService:

    @staticmethod
    def create(patient_id, form):

        exam = Examination(

            patient_id=patient_id,

            doctor_id=current_user.doctor_profile.doctor_id,

            exam_date=datetime.now(),

            chief_complaint=form.chief_complaint.data,

            note=form.note.data,

            created_at=datetime.now()

        )

        return ExaminationRepository.create(exam)

    @staticmethod
    def get_all():

        return ExaminationRepository.get_all()

    @staticmethod
    def get_by_id(exam_id):

        return ExaminationRepository.get_by_id(exam_id)

    @staticmethod
    def get_by_patient(patient_id):

        return ExaminationRepository.get_by_patient(patient_id)

    @staticmethod
    def get_patient_examinations(patient_id):

        return ExaminationRepository.get_by_patient(patient_id)

    @staticmethod
    def get_detail(exam_id):

        return ExaminationRepository.get_by_id(exam_id)
    @staticmethod
    def update(exam, form):

        exam.chief_complaint = form.chief_complaint.data
        exam.note = form.note.data

        ExaminationRepository.update()

        return exam

    @staticmethod
    def delete(exam):

        ExaminationRepository.delete(exam)

    @staticmethod
    def search(keyword):

        return ExaminationRepository.search(keyword)

    @staticmethod
    def count():

        return ExaminationRepository.count()