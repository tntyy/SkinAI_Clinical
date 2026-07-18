from app.database.db import db


class DoctorProfile(db.Model):

    __tablename__ = "doctor_profiles"

    doctor_id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.user_id"),
        unique=True,
        nullable=False
    )

    fullname = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(100)
    )

    phone = db.Column(
        db.String(20)
    )

    hospital = db.Column(
        db.String(150)
    )

    department = db.Column(
        db.String(100)
    )

    avatar_path = db.Column(
        db.String(255)
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    user = db.relationship(
        "User",
        back_populates="doctor_profile"
    )
    patients = db.relationship(
        "Patient",
        back_populates="doctor"
    )