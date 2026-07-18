from flask import Blueprint
from flask import render_template

doctor = Blueprint(
    "doctor",
    __name__,
    url_prefix="/doctor"
)


@doctor.route("/dashboard")
def dashboard():
    return render_template("doctor/dashboard.html")