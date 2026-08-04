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


@doctor.route("/reports")
@login_required
def reports():
    return render_template("doctor/reports.html")


@doctor.route("/history")
@login_required
def history():
    return render_template("doctor/history.html")


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