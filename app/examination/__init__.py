from flask import Blueprint

examination = Blueprint(
    "examination",
    __name__,
    url_prefix="/examination"
)

from app.examination import routes