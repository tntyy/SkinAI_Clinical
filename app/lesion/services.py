import os
import uuid

from werkzeug.utils import secure_filename
from app.lesion.validators import blur_score

from app.models.lesion_image import LesionImage
from app.lesion.repositories import LesionImageRepository


UPLOAD_FOLDER = "app/static/uploads/original"


class LesionService:

    @staticmethod
    def upload(form, exam_id):

        file = form.image.data

        ext = file.filename.split(".", 1)[1].lower()

        filename = f"{uuid.uuid4()}.{ext}"

        os.makedirs(
            UPLOAD_FOLDER,
            exist_ok=True
        )

        filepath = os.path.join(
            UPLOAD_FOLDER,
            filename
        )

        file.save(filepath)

        score = float(blur_score(filepath))

        lesion = LesionImage(

            exam_id=exam_id,

            image_path=f"uploads/original/{filename}",

            blur_score=score,

            is_valid=(score >= 100)

        )

        return LesionImageRepository.create(lesion)


    @staticmethod
    def get_by_id(image_id):

        return LesionImageRepository.get_by_id(
            image_id
        )

    @staticmethod
    def get_by_examination(exam_id):

        return LesionImageRepository.get_by_examination(
            exam_id
        )

    @staticmethod
    def delete(image):

        return LesionImageRepository.delete(
            image
        )

    @staticmethod
    def upload_file(file, exam_id):
        filename = f"{uuid.uuid4().hex}.png"

        filepath = os.path.join(

            UPLOAD_FOLDER,

            filename

        )

        os.makedirs(
            UPLOAD_FOLDER,
            exist_ok=True
        )

        file.save(filepath)

        score = float(blur_score(filepath))

        lesion = LesionImage(

            exam_id=exam_id,

            image_path=f"uploads/original/{filename}",

            blur_score=score,

            is_valid=(score >= 100)

        )

        return LesionImageRepository.create(lesion)
