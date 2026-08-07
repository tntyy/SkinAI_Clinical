from flask import (
    render_template,
    redirect,
    url_for,
    flash
)

from flask import render_template
from flask_login import login_required

from app.doctor import doctor

from flask_login import current_user

from app.doctor.forms import DoctorReviewForm
from app.doctor.services import DoctorReportService
from app.doctor.dashboard_service import DashboardService
from app.ai.repositories import AIRepository
from app.lesion.repositories import LesionImageRepository
from app.models.report_prediction_ref import ReportPredictionRef
from app.models.disease import Disease

from flask import send_file

from app.doctor.pdf_service import PDFService

from app.doctor.repositories import DoctorReportRepository
from app.lesion.repositories import LesionImageRepository


@doctor.route("/dashboard")
@login_required
def dashboard():

    data = DashboardService.get_dashboard()

    return render_template(
        "doctor/dashboard.html",
        data=data
    )


@doctor.route("/patients")
@login_required
def patients():
    return render_template("doctor/patients.html")


@doctor.route("/lesions")
@login_required
def lesions():
    return render_template("doctor/lesions.html")


@doctor.route("/ai")
@login_required
def ai():
    return render_template("doctor/ai.html")


@doctor.route("/explain")
@login_required
def explain():
    return render_template("doctor/explain.html")

@doctor.route("/history")
@login_required
def history():
    return render_template("doctor/history.html")

@doctor.route("/reports")
@login_required
def reports():

    reports = DoctorReportRepository.get_all()

    return render_template(
        "doctor/report.html",
        reports=reports
    )

@doctor.route(
    "/reports/<int:report_id>/export-pdf"
)
@login_required
def export_report_pdf(report_id):

    # ==================================================
    # 1. LẤY BÁO CÁO
    # ==================================================

    report = DoctorReportRepository.get_by_id(
        report_id
    )

    if report is None:

        flash(
            "Không tìm thấy báo cáo.",
            "danger"
        )

        return redirect(
            url_for("doctor.reports")
        )

    # ==================================================
    # 2. EXAMINATION
    # ==================================================

    exam = report.examination

    if exam is None:

        flash(
            "Không tìm thấy thông tin ca khám.",
            "danger"
        )

        return redirect(
            url_for("doctor.reports")
        )

    # ==================================================
    # 3. PATIENT
    # ==================================================

    patient = exam.patient

    # ==================================================
    # 4. DOCTOR
    # ==================================================

    doctor = report.doctor

    # ==================================================
    # 5. LESION IMAGE
    # ==================================================

    lesion = (
        LesionImageRepository
        .get_first_by_exam(
            exam.exam_id
        )
    )

    if lesion is None:

        flash(
            "Không tìm thấy ảnh tổn thương.",
            "danger"
        )

        return redirect(
            url_for("doctor.reports")
        )

    # ==================================================
    # 6. AI PREDICTION
    # ==================================================

    prediction_ref = (
        ReportPredictionRef.query
        .filter_by(
            report_id=report.report_id
        )
        .first()
    )

    prediction = None
    results = []
    heatmap = None

    # ==================================================
    # 7. AI RESULTS
    # ==================================================

    if prediction_ref:

        prediction = (
            prediction_ref.prediction
        )

        if prediction:

            results = (
                AIRepository
                .get_prediction_details(
                    prediction.prediction_id
                )
            )

            heatmap = (
                AIRepository
                .get_heatmap(
                    prediction.prediction_id
                )
            )

    # ==================================================
    # 8. GENERATE PDF
    # ==================================================

    pdf = PDFService.generate_pdf({

        "patient": patient,

        "doctor": doctor,

        "exam": exam,

        "lesion": lesion,

        "lesion_image": lesion.image_path,

        "prediction": prediction,

        "results": results,

        "report": report,

        "heatmap": heatmap

    })

    # ==================================================
    # 9. DOWNLOAD
    # ==================================================

    return send_file(

        pdf,

        download_name=(
            f"SkinAI_Report_{report.report_id}.pdf"
        ),

        mimetype="application/pdf",

        as_attachment=True

    )

@doctor.route("/settings")
@login_required
def settings():
    return render_template("doctor/settings.html")

@doctor.route(
    "/review/<int:image_id>",
    methods=["GET", "POST"]
)
@login_required
def review(image_id):

    lesion = LesionImageRepository.get_by_id(image_id)

    prediction = AIRepository.get_prediction_by_image(image_id)

    if prediction is None:

        flash(
            "Ảnh chưa được AI dự đoán.",
            "warning"
        )

        return redirect(
            url_for(
                "lesion.detail",
                image_id=image_id
            )
        )

    form = DoctorReviewForm()

    if form.validate_on_submit():

        DoctorReportService.confirm(

            lesion.exam_id,

            current_user.doctor_profile.doctor_id,

            prediction.prediction_id,

            form

        )

        flash(
            "Đã xác nhận kết quả AI.",
            "success"
        )

        return redirect(
            url_for(
                "lesion.detail",
                image_id=image_id
            )
        )

    return render_template(

        "doctor/review.html",

        lesion=lesion,

        prediction=prediction,

        form=form

    )
@doctor.route("/prediction-history/<int:patient_id>")
@login_required
def prediction_history(patient_id):

    history = DoctorReportService.prediction_history(
        patient_id
    )

    return render_template(

        "doctor/prediction_history.html",

        history=history

    )

@doctor.route("/export-pdf/<int:image_id>")
@login_required
def export_pdf(image_id):

    lesion = LesionImageRepository.get_by_id(image_id)

    if lesion is None:
        return "Image not found"

    prediction = AIRepository.get_prediction_by_image(image_id)

    if prediction is None:
        return "Prediction not found"

    results = AIRepository.get_prediction_details(
        prediction.prediction_id
    )

    heatmap = AIRepository.get_heatmap(
        prediction.prediction_id
    )

    report = DoctorReportRepository.get_by_image(
        image_id
    )

    exam = lesion.examination

    patient = exam.patient

    doctor = exam.doctor

    pdf = PDFService.generate_pdf({

        "patient": patient,
        "doctor": doctor,
        "exam": exam,
        "lesion": lesion,
        "prediction": prediction,
        "results": results,
        "report": report,
        "heatmap": heatmap

    })

    return send_file(

        pdf,

        download_name=f"SkinAI_Report_{image_id}.pdf",

        mimetype="application/pdf",

        as_attachment=True

    )