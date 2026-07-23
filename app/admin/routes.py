from flask import render_template
from flask_login import login_required

from app.admin import admin


@admin.route("/dashboard")
@login_required
def dashboard():
    return render_template("admin/dashboard.html")


@admin.route("/users")
@login_required
def users():
    return render_template("admin/users.html")


@admin.route("/doctors")
@login_required
def doctors():
    return render_template("admin/doctors.html")


@admin.route("/patients")
@login_required
def patients():
    return render_template("admin/patients.html")


@admin.route("/datasets")
@login_required
def datasets():
    return render_template("admin/datasets.html")


@admin.route("/models")
@login_required
def models():
    return render_template("admin/models.html")


@admin.route("/diseases")
@login_required
def diseases():
    return render_template("admin/diseases.html")


@admin.route("/statistics")
@login_required
def statistics():
    return render_template("admin/statistics.html")


@admin.route("/logs")
@login_required
def logs():
    return render_template("admin/logs.html")


@admin.route("/settings")
@login_required
def settings():
    return render_template("admin/settings.html")