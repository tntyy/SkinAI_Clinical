from flask import (
    render_template,
    redirect,
    url_for,
    flash,
    request
)

from flask_login import login_required

from app.patient import patient

from app.patient.forms import PatientForm
from app.patient.services import PatientService


####################################################
# Danh sách bệnh nhân
####################################################

@patient.route("/")
@login_required
def list_patients():

    keyword = request.args.get("keyword")

    if keyword:
        patients = PatientService.search(keyword)
    else:
        patients = PatientService.get_all()

    print("========== DEBUG ==========")
    print("Patients:", patients)
    print("Count:", len(patients))
    for p in patients:
        print(p.patient_id, p.fullname)
    print("===========================")

    return render_template(
        "patient/list.html",
        patients=patients,
        keyword=keyword
    )


####################################################
# Thêm bệnh nhân
####################################################

@patient.route("/create", methods=["GET", "POST"])
@login_required
def create_patient():

    form = PatientForm()

    if form.validate_on_submit():

        PatientService.create_patient(form)

        flash(

            "Thêm bệnh nhân thành công.",

            "success"

        )

        return redirect(

            url_for("patient.list_patients")

        )

    return render_template(

        "patient/create.html",

        form=form

    )


####################################################
# Chi tiết bệnh nhân
####################################################

@patient.route("/<int:patient_id>")
@login_required
def detail_patient(patient_id):

    patient_data = PatientService.get_by_id(

        patient_id

    )

    if patient_data is None:

        flash(

            "Không tìm thấy bệnh nhân.",

            "danger"

        )

        return redirect(

            url_for("patient.list_patients")

        )

    return render_template(

        "patient/detail.html",

        patient=patient_data

    )


####################################################
# Cập nhật bệnh nhân
####################################################

@patient.route(

    "/<int:patient_id>/edit",

    methods=["GET", "POST"]

)

@login_required
def edit_patient(patient_id):

    patient_data = PatientService.get_by_id(

        patient_id

    )

    if patient_data is None:

        flash(

            "Không tìm thấy bệnh nhân.",

            "danger"

        )

        return redirect(

            url_for("patient.list_patients")

        )

    form = PatientForm(

        obj=patient_data

    )

    if form.validate_on_submit():

        PatientService.update_patient(

            patient_data,

            form

        )

        flash(

            "Đã cập nhật bệnh nhân.",

            "success"

        )

        return redirect(

            url_for(

                "patient.list_patients"

            )

        )

    return render_template(

        "patient/edit.html",

        form=form,

        patient=patient_data

    )


####################################################
# Xóa bệnh nhân
####################################################

@patient.route(

    "/<int:patient_id>/delete",

    methods=["POST"]

)

@login_required
def delete_patient(patient_id):

    patient_data = PatientService.get_by_id(

        patient_id

    )

    if patient_data is None:

        flash(

            "Không tìm thấy bệnh nhân.",

            "danger"

        )

        return redirect(

            url_for(

                "patient.list_patients"

            )

        )

    PatientService.delete_patient(

        patient_data

    )

    flash(

        "Đã xóa bệnh nhân.",

        "success"

    )

    return redirect(

        url_for(

            "patient.list_patients"

        )

    )
####################################################
# Tạo lần khám
####################################################

@patient.route("/<int:patient_id>/new-examination")
@login_required
def new_examination(patient_id):

    return redirect(

        url_for(

            "examination.create_examination",

            patient_id=patient_id

        )

    )
