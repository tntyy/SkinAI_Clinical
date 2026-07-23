from flask import Blueprint

auth = Blueprint(
    "api",
    __name__,
    url_prefix="/api"
)

