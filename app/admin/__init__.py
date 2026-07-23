from flask import Blueprint

auth = Blueprint(
    "admin",
    __name__,
    url_prefix="/admin"
)

from app.admin import routes