from app.database.db import db

from app.models.lesion_image import (
    LesionImage
)


class LesionImageRepository:

    # ======================================================
    # CREATE
    # ======================================================

    @staticmethod
    def create(image):

        db.session.add(
            image
        )

        db.session.commit()

        return image

    # ======================================================
    # GET BY ID
    # ======================================================

    @staticmethod
    def get_by_id(
        image_id
    ):

        return (
            LesionImage.query
            .get(image_id)
        )

    # ======================================================
    # GET BY EXAMINATION
    # ======================================================

    @staticmethod
    def get_by_examination(
        exam_id
    ):

        return (

            LesionImage.query

            .filter_by(
                exam_id=exam_id
            )

            .all()

        )

    # ======================================================
    # UPDATE
    # ======================================================

    @staticmethod
    def update():

        db.session.commit()

    # ======================================================
    # DELETE
    # ======================================================

    @staticmethod
    def delete(
        image
    ):

        db.session.delete(
            image
        )

        db.session.commit()

    # ======================================================
    # GET FIRST IMAGE BY EXAM
    # ======================================================

    @staticmethod
    def get_first_by_exam(
        exam_id
    ):

        return (

            LesionImage.query

            .filter_by(
                exam_id=exam_id
            )

            .order_by(
                LesionImage
                .image_id
                .asc()
            )

            .first()

        )