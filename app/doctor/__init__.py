from flask import Blueprint

auth = Blueprint(
    "doctor",
    __name__,
    url_prefix="/doctor"
)

from app.doctor import routes