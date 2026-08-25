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
        backref=db.backref(
            "prediction_refs",
            cascade="all, delete-orphan"
        )
    )

    prediction = db.relationship(
        "AIPrediction",
        backref=db.backref(
            "report_refs",
            cascade="all, delete-orphan"
        )
    )