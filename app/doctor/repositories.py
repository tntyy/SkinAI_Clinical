from datetime import datetime

from app.database.db import db
from sqlalchemy import (
    text,
    or_,
    cast,
    String
)

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
    def get_prediction_history(
            patient_id,
            search=None,
            date_from=None,
            date_to=None
    ):
        sql = text("""
            SELECT
                p.patient_id,
                p.patient_code,
                p.fullname,

                e.exam_id,
                e.exam_date,
                e.chief_complaint,

                li.image_id,
                li.image_path,

                ap.prediction_id,
                ap.model_name,
                ap.model_version,
                ap.inference_time,
                ap.created_at AS prediction_created_at,

                detail.predicted_class,
                detail.confidence

            FROM patients p

            INNER JOIN examinations e
                ON e.patient_id = p.patient_id

            INNER JOIN lesion_images li
                ON li.exam_id = e.exam_id

            INNER JOIN ai_predictions ap
                ON ap.image_id = li.image_id

            LEFT JOIN ai_prediction_details detail
                ON detail.prediction_id = ap.prediction_id
                AND detail.rank = 1

            WHERE p.patient_id = :patient_id

            AND (
                :search = ''
                OR LOWER(p.fullname)
                    LIKE LOWER(:search_pattern)

                OR LOWER(p.patient_code)
                    LIKE LOWER(:search_pattern)

                OR LOWER(e.chief_complaint)
                    LIKE LOWER(:search_pattern)

                OR LOWER(detail.predicted_class)
                    LIKE LOWER(:search_pattern)

                OR LOWER(ap.model_name)
                    LIKE LOWER(:search_pattern)
            )

            AND (
                :date_from IS NULL
                OR ap.created_at >= CAST(:date_from AS timestamp)
            )

            AND (
                :date_to IS NULL
                OR ap.created_at <
                    CAST(:date_to AS date)
                    + INTERVAL '1 day'
            )

            ORDER BY
                ap.created_at DESC,
                ap.prediction_id DESC
        """)

        search = (search or "").strip()

        search_pattern = (
            f"%{search}%"
            if search
            else "%"
        )

        result = db.session.execute(
            sql,
            {
                "patient_id": patient_id,
                "search": search,
                "search_pattern": search_pattern,
                "date_from": date_from,
                "date_to": date_to
            }
        )

        return result.mappings().all()

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

    @staticmethod
    def search_reports(
            keyword=None,
            from_date=None,
            to_date=None,
            page=1,
            per_page=10
    ):
        query = (
            DoctorReport.query
            .join(
                Examination,
                DoctorReport.exam_id == Examination.exam_id
            )
            .join(
                Patient,
                Examination.patient_id == Patient.patient_id
            )
        )

        # ==================================================
        # TÌM KIẾM
        # ==================================================

        if keyword:
            keyword = keyword.strip()

            search = f"%{keyword}%"

            query = query.filter(
                or_(
                    cast(
                        DoctorReport.report_id,
                        String
                    ).ilike(search),

                    Patient.fullname.ilike(search),

                    Patient.patient_code.ilike(search)
                )
            )

        # ==================================================
        # TỪ NGÀY
        # ==================================================

        if from_date:
            query = query.filter(
                DoctorReport.confirmed_at >= from_date
            )

        # ==================================================
        # ĐẾN NGÀY
        # ==================================================

        if to_date:
            query = query.filter(
                DoctorReport.confirmed_at < to_date
            )

        # ==================================================
        # SẮP XẾP
        # ==================================================

        query = query.order_by(
            DoctorReport.confirmed_at.desc()
        )

        # ==================================================
        # PHÂN TRANG
        # ==================================================

        pagination = query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )

        return pagination