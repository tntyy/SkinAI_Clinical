import os
from werkzeug.utils import secure_filename

from app.models.lesion_image import LesionImage
from app.lesion.repositories import LesionRepository


UPLOAD_FOLDER = "app/static/uploads/original"


class LesionService:

    @staticmethod
    def upload(form, exam_id):

        file = form.image.data

        filename = secure_filename(file.filename)

        os.makedirs(
            UPLOAD_FOLDER,
            exist_ok=True
        )

        path = os.path.join(
            UPLOAD_FOLDER,
            filename
        )

        file.save(path)

        lesion = LesionImage(

            exam_id=exam_id,

            image_path=f"uploads/original/{filename}"

        )

        return LesionRepository.create(
            lesion
        )