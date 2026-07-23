from flask import Blueprint

auth = Blueprint(
    "explain",
    __name__,
    url_prefix="/explain",
)
