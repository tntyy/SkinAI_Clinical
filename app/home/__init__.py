from flask import Blueprint

auth = Blueprint(
    "home",
    __name__,
    url_prefix="/home"
)

from app.home import routes