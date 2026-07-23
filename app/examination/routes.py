from flask import render_template

from app.examination import examination


@examination.route("/")
def new_examination():
    return render_template("examination/index.html")