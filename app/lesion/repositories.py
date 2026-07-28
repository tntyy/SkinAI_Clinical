from app.models.lesion_image import LesionImage
from app.database.db import db


class LesionRepository:

    @staticmethod
    def create(image):

        db.session.add(image)
        db.session.commit()

        return image


    @staticmethod
    def get_by_exam(exam_id):

        return LesionImage.query.filter_by(
            exam_id=exam_id
        ).all()