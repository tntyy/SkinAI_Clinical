from app.database.db import db
from flask_login import UserMixin

class User(UserMixin ,db.Model):
    __tablename__ = "users"

    user_id = db.Column(
        db.Integer,
        primary_key=True
    )

    username = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )

    password_hash = db.Column(
        db.String(255),
        nullable=False
    )

    role = db.Column(
        db.String(20),
        nullable=False
    )

    is_active = db.Column(
        db.Boolean,
        nullable=False,
        default=True
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    updated_at = db.Column(
        db.DateTime,
        server_default=db.func.now(),
        onupdate=db.func.now()
    )

    # Đăng nhập lần cuối
    last_login = db.Column(
        db.DateTime,
        nullable=True
    )

    # Quan hệ 1-1 với DoctorProfile
    doctor_profile = db.relationship(
        "DoctorProfile",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )

    def get_id(self):
        return str(self.user_id)

    def __repr__(self):
        return f"<User {self.username}>"

