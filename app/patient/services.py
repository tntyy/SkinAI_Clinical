import random
from datetime import datetime

from flask_login import current_user

from app.models.patient import Patient
from app.patient.repositories import PatientRepository


class PatientService:

    @staticmethod
    def generate_patient_code():

        while True:

            code = "BN" + str(random.randint(100000, 999999))

            patient = PatientRepository.get_by_code(code)

            if patient is None:
                return code

    @staticmethod
    def create_patient(form):

        patient = Patient(

            patient_code=PatientService.generate_patient_code(),

            created_by_doctor=current_user.doctor_profile.doctor_id,

            fullname=form.fullname.data,

            gender=form.gender.data,

            birth_year=form.birth_year.data,

            phone=form.phone.data,

            created_at=datetime.utcnow()

        )

        return PatientRepository.create(patient)

    @staticmethod
    def update_patient(patient, form):

        patient.fullname = form.fullname.data

        patient.gender = form.gender.data

        patient.birth_year = form.birth_year.data

        patient.phone = form.phone.data

        PatientRepository.update()

    @staticmethod
    def delete_patient(patient):

        PatientRepository.delete(patient)

    @staticmethod
    def get_all():

        return PatientRepository.get_all()

    @staticmethod
    def get_by_id(patient_id):

        return PatientRepository.get_by_id(patient_id)

    @staticmethod
    def search(keyword):

        return PatientRepository.search(keyword)

    @staticmethod
    def count():

        return PatientRepository.count()