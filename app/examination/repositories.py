from app.models.examination import Examination
from app.database.db import db


class ExaminationRepository:

    @staticmethod
    def create(examination):

        db.session.add(examination)
        db.session.commit()

        return examination

    @staticmethod
    def get_by_id(exam_id):

        return Examination.query.get(exam_id)

    @staticmethod
    def get_by_patient(patient_id):

        return Examination.query.filter_by(
            patient_id=patient_id
        ).all()

    @staticmethod
    def get_all_by_patient(patient_id):
        return Examination.query.filter_by(
            patient_id=patient_id
        ).order_by(
            Examination.exam_date.desc()
        ).all()