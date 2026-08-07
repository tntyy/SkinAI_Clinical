from app.database.db import db
from app.models.lesion_image import LesionImage


class LesionImageRepository:

    @staticmethod
    def create(image):

        db.session.add(image)
        db.session.commit()

        return image

    @staticmethod
    def get_by_id(image_id):

        return LesionImage.query.get(image_id)

    @staticmethod
    def get_by_examination(exam_id):

        return (
            LesionImage.query
            .filter_by(exam_id=exam_id)
            .all()
        )

    @staticmethod
    def update():

        db.session.commit()

    @staticmethod
    def delete(image):

        db.session.delete(image)
        db.session.commit()

    @staticmethod
    def get_first_by_exam(exam_id):
        return (
            LesionImage.query
            .filter_by(exam_id=exam_id)
            .order_by(
                LesionImage.image_id.asc()
            )
            .first()
        )