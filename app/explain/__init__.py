from flask import Blueprint

explain = Blueprint(
    "explain",
    __name__,
    url_prefix="/explain",
)
