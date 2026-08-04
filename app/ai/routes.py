from flask import render_template
from flask_login import login_required
from app.ai import ai

import os

from app.ai.services import AIService
from app.lesion.repositories import LesionImageRepository


@ai.route("/predict/<int:lesion_image_id>")
@login_required
def predict(lesion_image_id):

    lesion = LesionImageRepository.get_by_id(
        lesion_image_id
    )

    if lesion is None:
        return "Image not found"

    image_path = os.path.join(
        "app",
        "static",
        lesion.image_path
    )

    data = AIService.predict(
        image_path,
        lesion_image_id
    )

    return render_template(
        "lesion/detail.html",
        lesion=lesion,
        results=data["results"],
        heatmap_path=data["heatmap_path"],
        overlay_path=data["overlay_path"]
    )