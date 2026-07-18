from datetime import datetime
from app.database.db import db


class LesionImage(db.Model):
    __tablename__ = "lesion_images"

    image_id = db.Column(
        db.Integer,
        primary_key=True
    )

    exam_id = db.Column(
        db.Integer,
        db.ForeignKey("examinations.exam_id"),
        nullable=False
    )

    image_path = db.Column(
        db.String(255),
        nullable=False
    )

    crop_path = db.Column(
        db.String(255)
    )

    blur_score = db.Column(
        db.Float
    )

    quality_score = db.Column(
        db.Float
    )

    is_valid = db.Column(
        db.Boolean,
        default=True
    )

    captured_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    examination = db.relationship(
        "Examination",
        backref="lesion_images"
    )