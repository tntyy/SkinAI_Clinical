from datetime import datetime
from app.database.db import db


class AuditLog(db.Model):
    __tablename__ = "audit_logs"

    log_id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.user_id"),
        nullable=False
    )

    action = db.Column(
        db.String(20),
        nullable=False
    )

    target_table = db.Column(
        db.String(50),
        nullable=False
    )

    target_id = db.Column(
        db.Integer
    )

    ip_address = db.Column(
        db.String(45)
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    user = db.relationship(
        "User",
        backref="audit_logs"
    )