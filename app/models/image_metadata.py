from app.database.db import db


class ImageMetadata(db.Model):
    __tablename__ = "image_metadata"

    metadata_id = db.Column(
        db.Integer,
        primary_key=True
    )

    image_id = db.Column(
        db.Integer,
        db.ForeignKey("lesion_images.image_id"),
        unique=True,
        nullable=False
    )

    age = db.Column(
        db.Integer
    )

    gender = db.Column(
        db.String(10)
    )

    lesion_location = db.Column(
        db.String(100)
    )

    skin_type = db.Column(
        db.String(50)
    )

    device = db.Column(
        db.String(100)
    )

    note = db.Column(
        db.Text
    )

    lesion_image = db.relationship(
        "LesionImage",
        backref="metadata",
        uselist=False
    )