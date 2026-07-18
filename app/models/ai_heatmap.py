from app.database.db import db


class AIHeatmap(db.Model):
    __tablename__ = "ai_heatmaps"

    heatmap_id = db.Column(
        db.Integer,
        primary_key=True
    )

    prediction_id = db.Column(
        db.Integer,
        db.ForeignKey("ai_predictions.prediction_id"),
        nullable=False
    )

    heatmap_path = db.Column(
        db.String(255),
        nullable=False
    )

    overlay_path = db.Column(
        db.String(255)
    )

    method = db.Column(
        db.String(50),
        default="GradCAM"
    )

    prediction = db.relationship(
        "AIPrediction",
        backref="heatmaps"
    )