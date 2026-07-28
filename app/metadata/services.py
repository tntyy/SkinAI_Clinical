from app.models.image_metadata import ImageMetadata

from app.metadata.repositories import MetadataRepository


class MetadataService:

    @staticmethod
    def create(image_id, form):

        metadata = ImageMetadata(

            image_id=image_id,

            age=form.age.data,

            gender=form.gender.data,

            lesion_location=form.lesion_location.data,

            skin_type=form.skin_type.data,

            device=form.device.data,

            note=form.note.data

        )

        return MetadataRepository.create(metadata)