from app.database.db import db
from app.models.examination import Examination


class ExaminationRepository:

    @staticmethod
    def create(exam):
        db.session.add(exam)
        db.session.commit()
        return exam

    @staticmethod
    def update():
        db.session.commit()

    @staticmethod
    def delete(exam):
        db.session.delete(exam)
        db.session.commit()

    @staticmethod
    def get_by_id(exam_id):
        return Examination.query.get(exam_id)

    @staticmethod
    def get_by_patient(patient_id):
        return (
            Examination.query
            .filter_by(patient_id=patient_id)
            .order_by(Examination.created_at.desc())
            .all()
        )

    @staticmethod
    def get_all():
        return (
            Examination.query
            .order_by(Examination.created_at.desc())
            .all()
        )
    @staticmethod
    def search(keyword):

        return Examination.query.filter(

            Examination.chief_complaint.ilike(f"%{keyword}%")

        ).order_by(

            Examination.created_at.desc()

        ).all()

    @staticmethod
    def count():

        return Examination.query.count()