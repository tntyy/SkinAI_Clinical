from app.database.db import db


class Patient(db.Model):

    __tablename__ = "patients"

    patient_id = db.Column(
        db.Integer,
        primary_key=True
    )

    patient_code = db.Column(
        db.String(30),
        unique=True,
        nullable=False
    )

    created_by_doctor = db.Column(
        db.Integer,
        db.ForeignKey("doctor_profiles.doctor_id"),
        nullable=False
    )

    fullname = db.Column(
        db.String(100),
        nullable=False
    )

    gender = db.Column(
        db.String(10)
    )

    birth_year = db.Column(
        db.Integer
    )

    phone = db.Column(
        db.String(20)
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )
    doctor = db.relationship(
        "DoctorProfile",
        back_populates="patients"
    )

    examinations = db.relationship(
        "Examination",
        back_populates="patient",
        cascade="all, delete-orphan"
    )