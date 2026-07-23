from flask import render_template

from app.patient import patient


@patient.route("/")
def list_patients():

    return render_template("patient/index.html")