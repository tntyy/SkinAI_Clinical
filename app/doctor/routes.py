from flask import render_template
from flask_login import login_required

from app.doctor import doctor


@doctor.route("/dashboard")
@login_required
def dashboard():
    return render_template("doctor/dashboard.html")


@doctor.route("/patients")
@login_required
def patients():
    return render_template("doctor/patients.html")


@doctor.route("/examinations")
@login_required
def examinations():
    return render_template("doctor/examinations.html")


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