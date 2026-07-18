from app.database.db import db


class AIPredictionDetail(db.Model):
    __tablename__ = "ai_prediction_details"

    detail_id = db.Column(
        db.Integer,
        primary_key=True
    )

    prediction_id = db.Column(
        db.Integer,
        db.ForeignKey("ai_predictions.prediction_id"),
        nullable=False
    )

    rank = db.Column(
        db.Integer,
        nullable=False
    )

    predicted_class = db.Column(
        db.String(100),
        nullable=False
    )

    confidence = db.Column(
        db.Float,
        nullable=False
    )

    prediction = db.relationship(
        "AIPrediction",
        backref="details"
    )