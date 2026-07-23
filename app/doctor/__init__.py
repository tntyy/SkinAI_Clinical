from flask import Blueprint

doctor = Blueprint(
    "doctor",
    __name__,
    url_prefix="/doctor"
)

from app.doctor import routes