from app.models.patient import Patient
from app.patient.repositories import PatientRepository
from flask_login import current_user


class PatientService:

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
    def create_patient(form):
        doctor = current_user.doctor_profile

        patient = Patient(
            patient_code=PatientService.generate_patient_code(),

            created_by_doctor=doctor.doctor_id,

            fullname=form.fullname.data,
            gender=form.gender.data,
            birth_year=form.birth_year.data,
            phone=form.phone.data,

            drug_allergies=form.drug_allergies.data,
            chronic_diseases=form.chronic_diseases.data,
            hereditary_diseases=form.hereditary_diseases.data
        )

        return PatientRepository.create(patient)

    @staticmethod
    def update_patient(patient, form):

        patient.fullname = form.fullname.data

        patient.gender = form.gender.data

        patient.birth_year = form.birth_year.data

        patient.phone = form.phone.data

        # ==========================
        # BỆNH SỬ
        # ==========================

        patient.drug_allergies = form.drug_allergies.data

        patient.chronic_diseases = form.chronic_diseases.data

        patient.hereditary_diseases = form.hereditary_diseases.data

        PatientRepository.update()

        return patient

    @staticmethod
    def delete_patient(patient):
        PatientRepository.delete(patient)

    @staticmethod
    def generate_patient_code():

        # Nếu project hiện tại của bạn đã có
        # cách sinh patient_code thì GIỮ NGUYÊN
        import uuid

        return "BN-" + uuid.uuid4().hex[:8].upper()