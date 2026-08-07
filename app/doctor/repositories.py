from datetime import datetime

from app.database.db import db

from app.models.doctor_report import DoctorReport
from app.models.report_prediction_ref import ReportPredictionRef
from app.models.patient import Patient
from app.models.examination import Examination
from app.models.lesion_image import LesionImage
from app.models.ai_prediction import AIPrediction
from app.models.ai_prediction_detail import AIPredictionDetail
from app.models.ai_heatmap import AIHeatmap


class DoctorReportRepository:

    @staticmethod
    def save(

            exam_id,
            doctor_id,
            prediction_id,
            diagnosis,
            treatment,
            note

    ):

        report = DoctorReport(

            exam_id=exam_id,

            doctor_id=doctor_id,

            diagnosis=diagnosis,

            treatment=treatment,

            note=note,

            status="confirmed",

            confirmed_at=datetime.utcnow()

        )

        db.session.add(report)
        db.session.flush()

        ref = ReportPredictionRef(

            report_id=report.report_id,

            prediction_id=prediction_id

        )

        db.session.add(ref)

        db.session.commit()

        return report
    @staticmethod
    def get_report_by_exam(exam_id):

        return (

            DoctorReport.query

            .filter_by(exam_id=exam_id)

            .order_by(DoctorReport.report_id.desc())

            .first()

        )

    @staticmethod
    def get_prediction_history(patient_id):
        return (
            db.session.query(

                Examination.exam_date,

                LesionImage.image_id,
                LesionImage.image_path,

                AIPrediction.prediction_id,

                AIPredictionDetail.predicted_class,
                AIPredictionDetail.confidence,

                DoctorReport.status

            )

            .join(
                Examination,
                Examination.exam_id == LesionImage.exam_id
            )

            .join(
                AIPrediction,
                AIPrediction.image_id == LesionImage.image_id
            )

            .join(
                AIPredictionDetail,
                AIPredictionDetail.prediction_id == AIPrediction.prediction_id
            )

            .outerjoin(
                DoctorReport,
                DoctorReport.exam_id == Examination.exam_id
            )

            .filter(
                Examination.patient_id == patient_id
            )

            .filter(
                AIPredictionDetail.rank == 1
            )

            .order_by(
                Examination.exam_date.desc()
            )

            .all()
        )
    @staticmethod
    def get_by_image(image_id):

        return (

            DoctorReport.query

            .join(
                Examination,
                Examination.exam_id == DoctorReport.exam_id
            )

            .join(
                LesionImage,
                LesionImage.exam_id == Examination.exam_id
            )

            .filter(
                LesionImage.image_id == image_id
            )

            .order_by(
                DoctorReport.report_id.desc()
            )

            .first()

        )

    @staticmethod
    def get_all():
        return (

            DoctorReport.query

            .order_by(
                DoctorReport.confirmed_at.desc()
            )

            .all()

        )

    @staticmethod
    def get_by_id(report_id):
        return (
            DoctorReport.query
            .filter_by(report_id=report_id)
            .first()
        )