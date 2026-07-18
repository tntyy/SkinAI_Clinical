from datetime import datetime
from app.database.db import db


class DoctorReport(db.Model):
    __tablename__ = "doctor_reports"

    report_id = db.Column(
        db.Integer,
        primary_key=True
    )

    exam_id = db.Column(
        db.Integer,
        db.ForeignKey("examinations.exam_id"),
        nullable=False
    )

    doctor_id = db.Column(
        db.Integer,
        db.ForeignKey("doctor_profiles.doctor_id"),
        nullable=False
    )

    diagnosis = db.Column(
        db.String(255),
        nullable=False
    )

    treatment = db.Column(
        db.Text
    )

    note = db.Column(
        db.Text
    )

    status = db.Column(
        db.String(20),
        default="confirmed"
    )

    confirmed_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    examination = db.relationship(
        "Examination",
        backref="doctor_reports"
    )

    doctor = db.relationship(
        "DoctorProfile",
        backref="doctor_reports"
    )