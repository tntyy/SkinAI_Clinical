from app.database.db import db
from app.models.image_metadata import ImageMetadata


class MetadataRepository:

    @staticmethod
    def create(metadata):

        db.session.add(metadata)

        db.session.commit()

        return metadata

    @staticmethod
    def get_by_image(image_id):

        return ImageMetadata.query.filter_by(

            image_id=image_id

        ).first()