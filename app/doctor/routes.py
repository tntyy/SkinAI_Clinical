from flask import Blueprint
from flask import render_template
from flask_login import login_required


doctor = Blueprint(
    "doctor",
    __name__,
    url_prefix="/doctor"
)


@doctor.route("/dashboard")
@login_required
def dashboard():
    return render_template("doctor/dashboard.html")