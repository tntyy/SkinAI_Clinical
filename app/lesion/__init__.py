from flask import Blueprint

lesion = Blueprint(
    "lesion",
    __name__,
    url_prefix="/lesion"
)

from app.lesion import routes