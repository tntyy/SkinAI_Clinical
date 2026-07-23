from flask import Blueprint

auth = Blueprint(
    "preprocessing",
    __name__,
    url_prefix="/preprocessing"
)

