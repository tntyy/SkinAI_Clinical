from app.ai.inference import run_prediction


class AIService:

    @staticmethod
    def predict(image_path):

        return run_prediction(image_path)