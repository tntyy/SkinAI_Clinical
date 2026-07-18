from app.database.db import db


class ReportPredictionRef(db.Model):
    __tablename__ = "report_prediction_refs"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    report_id = db.Column(
        db.Integer,
        db.ForeignKey("doctor_reports.report_id"),
        nullable=False
    )

    prediction_id = db.Column(
        db.Integer,
        db.ForeignKey("ai_predictions.prediction_id"),
        nullable=False
    )

    report = db.relationship(
        "DoctorReport",
        backref="prediction_refs"
    )

    prediction = db.relationship(
        "AIPrediction",
        backref="report_refs"
    )