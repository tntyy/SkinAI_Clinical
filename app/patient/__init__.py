from flask import Blueprint

patient = Blueprint(
    "patient",
    __name__,
    url_prefix="/patient"
)

from app.patient import routes