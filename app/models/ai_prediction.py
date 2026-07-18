from datetime import datetime
from app.database.db import db


class AIPrediction(db.Model):
    __tablename__ = "ai_predictions"

    prediction_id = db.Column(
        db.Integer,
        primary_key=True
    )

    image_id = db.Column(
        db.Integer,
        db.ForeignKey("lesion_images.image_id"),
        nullable=False
    )

    model_name = db.Column(
        db.String(100),
        nullable=False
    )

    model_version = db.Column(
        db.String(30)
    )

    inference_time = db.Column(
        db.Float
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    lesion_image = db.relationship(
        "LesionImage",
        backref="predictions"
    )