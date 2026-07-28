from flask import (
    render_template,
    redirect,
    url_for,
    flash
)

from flask_login import login_required

from app.metadata import metadata

from app.metadata.forms import MetadataForm

from app.metadata.services import MetadataService


@metadata.route(

    "/create/<int:image_id>",

    methods=["GET", "POST"]

)

@login_required

def create_metadata(image_id):

    form = MetadataForm()

    if form.validate_on_submit():

        MetadataService.create(

            image_id,

            form

        )

        flash(

            "Đã lưu Metadata.",

            "success"

        )

        return redirect(

            url_for(

                "ai.predict",

                image_id=image_id

            )

        )

    return render_template(

        "metadata/create.html",

        form=form

    )