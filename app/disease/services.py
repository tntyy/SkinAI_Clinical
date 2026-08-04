from app.models.disease import Disease


class DiseaseRepository:

    @staticmethod
    def get_all():
        return Disease.query.all()

    @staticmethod
    def get_by_code(code):
        return Disease.query.filter_by(
            disease_code=code
        ).first()

    @staticmethod
    def get_by_id(disease_id):
        return Disease.query.get(disease_id)