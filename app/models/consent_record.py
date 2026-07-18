from datetime import datetime
from app.database.db import db


class ConsentRecord(db.Model):
    __tablename__ = "consent_records"

    consent_id = db.Column(
        db.Integer,
        primary_key=True
    )

    exam_id = db.Column(
        db.Integer,
        db.ForeignKey("examinations.exam_id"),
        nullable=False
    )

    purpose = db.Column(
        db.String(50),
        nullable=False
    )

    granted_by = db.Column(
        db.Integer,
        db.ForeignKey("doctor_profiles.doctor_id"),
        nullable=False
    )

    granted_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    examination = db.relationship(
        "Examination",
        backref="consents"
    )

    doctor = db.relationship(
        "DoctorProfile",
        backref="consents"
    )