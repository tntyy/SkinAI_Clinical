from flask import Blueprint

disease = Blueprint(
    "disease",
    __name__,
    url_prefix="/disease"
)

from app.disease import routes