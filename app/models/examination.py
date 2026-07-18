from app.database.db import db


class Examination(db.Model):

    __tablename__ = "examinations"

    exam_id = db.Column(
        db.Integer,
        primary_key=True
    )

    patient_id = db.Column(
        db.Integer,
        db.ForeignKey("patients.patient_id"),
        nullable=False
    )

    doctor_id = db.Column(
        db.Integer,
        db.ForeignKey("doctor_profiles.doctor_id"),
        nullable=False
    )

    exam_date = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    chief_complaint = db.Column(
        db.String(255)
    )

    note = db.Column(
        db.Text
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )
    patient = db.relationship(
        "Patient",
        back_populates="examinations"
    )

    doctor = db.relationship(
        "DoctorProfile"
    )