from app.models.patient import Patient
from app.database.db import db


class PatientRepository:

    @staticmethod
    def get_all():

        return Patient.query.order_by(

            Patient.created_at.desc()

        ).all()

    @staticmethod
    def get_by_id(

            patient_id

    ):

        return Patient.query.get(

            patient_id

        )

    @staticmethod
    def create(

            patient

    ):

        db.session.add(

            patient

        )

        db.session.commit()

        return patient

    @staticmethod
    def update():

        db.session.commit()

    @staticmethod
    def delete(

            patient

    ):

        db.session.delete(

            patient

        )

        db.session.commit()

    @staticmethod
    def get_by_code(

            patient_code

    ):

        return Patient.query.filter_by(

            patient_code=patient_code

        ).first()

    @staticmethod
    def search(keyword):
        return Patient.query.filter(

            Patient.fullname.ilike(f"%{keyword}%")

        ).all()

    @staticmethod
    def count():
        return Patient.query.count()

    @staticmethod
    def get_all_by_doctor(doctor_id):
        return (
            Patient.query
            .filter_by(created_by_doctor=doctor_id)
            .order_by(Patient.created_at.desc())
            .all()
        )

    @staticmethod
    def search_by_doctor(keyword, doctor_id):
        return (
            Patient.query
            .filter(
                Patient.created_by_doctor == doctor_id,
                Patient.fullname.ilike(f"%{keyword}%")
            )
            .all()
        )