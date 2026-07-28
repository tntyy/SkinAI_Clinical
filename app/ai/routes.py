from flask import render_template

from flask_login import login_required

from app.ai import ai

from app.ai.services import AIService


@ai.route("/predict/<path:image_path>")

@login_required

def predict(image_path):

    results = AIService.predict(

        image_path

    )

    return render_template(

        "ai/result.html",

        results=results

    )