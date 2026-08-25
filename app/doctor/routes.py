from flask import (
    render_template,
    redirect,
    url_for,
    flash,
    send_file,
    request,
    jsonify
)

from flask_login import (
    login_required,
    current_user
)

from werkzeug.security import (
    check_password_hash,
    generate_password_hash
)
from sqlalchemy import text

from app.ai.grok_service import GrokService

from app.database.db import db

from app.doctor import doctor

from app.doctor.forms import DoctorReviewForm

from app.doctor.services import DoctorReportService

from app.doctor.dashboard_service import DashboardService

from app.ai.repositories import AIRepository

from app.models.patient import Patient

from app.lesion.repositories import (
    LesionImageRepository
)

from app.models.report_prediction_ref import (
    ReportPredictionRef
)

from app.doctor.pdf_service import PDFService

from app.doctor.repositories import (
    DoctorReportRepository
)

from app.doctor.icd10_mapping import (
    get_vietnamese_name,
    get_vietnamese_description,
    get_chapter_name,
    search_codes_by_vietnamese_name   # THÊM MỚI
)

from app.doctor.icd10_analysis_data import get_analysis
from app.doctor.icd10_mapping import get_chapter_name

# ==========================================================
# DASHBOARD
# ==========================================================

@doctor.route("/dashboard")
@login_required
def dashboard():

    data = DashboardService.get_dashboard()

    return render_template(
        "doctor/dashboard.html",
        data=data
    )


# ==========================================================
# PATIENTS
# ==========================================================

@doctor.route("/patients")
@login_required
def patients():

    return render_template(
        "doctor/patients.html"
    )


# ==========================================================
# LESIONS
# ==========================================================

@doctor.route("/lesions")
@login_required
def lesions():

    return render_template(
        "doctor/lesions.html"
    )


# ==========================================================
# AI
# ==========================================================

@doctor.route("/ai")
@login_required
def ai():

    return render_template(
        "doctor/ai.html"
    )

# ==========================================================
# SKINAI CHAT
# ==========================================================

@doctor.route(
    "/chat",
    methods=["POST"]
)
@login_required
def chat():

    try:

        data = request.get_json(silent=True) or {}

        message = (
            data.get("message", "")
            .strip()
        )

        if not message:

            return jsonify({
                "success": False,
                "message": "Vui lòng nhập câu hỏi."
            }), 400

        # ==========================================
        # LẤY KẾT QUẢ AI MỚI NHẤT
        # ==========================================

        context = (
            AIRepository
            .get_latest_prediction_for_chat()
        )

        if not context:

            return jsonify({
                "success": False,
                "message": (
                    "Hiện tại chưa có kết quả AI "
                    "để hỗ trợ trả lời."
                )
            }), 404

        # ==========================================
        # GỌI GROK
        # ==========================================

        reply = GrokService.chat(
            message,
            context
        )

        # ==========================================
        # RESPONSE
        # ==========================================

        return jsonify({

            "success": True,

            "reply": reply,

            "context": {

                "disease":
                    context.get("disease"),

                "prediction":
                    context.get("prediction"),

                "confidence":
                    context.get("confidence"),

                "icd10":
                    context.get("icd10"),

                "risk":
                    context.get("risk")

            }

        })

    except Exception as e:

        print(
            "❌ GROK CHAT ERROR:",
            repr(e)
        )

        return jsonify({

            "success": False,

            "message":
                "Không thể kết nối với SkinAI Assistant.",

            "error":
                str(e)

        }), 500


# ==========================================================
# EXPLAIN
# ==========================================================

@doctor.route("/explain")
@login_required
def explain():

    return render_template(
        "doctor/explain.html"
    )


# ==========================================================
# AI HISTORY
# ==========================================================

@doctor.route("/history")
@login_required
def history():

    patient_id = request.args.get(
        "patient_id",
        type=int
    )

    search = request.args.get(
        "search",
        "",
        type=str
    ).strip()

    date_from = request.args.get(
        "date_from",
        "",
        type=str
    ).strip()

    date_to = request.args.get(
        "date_to",
        "",
        type=str
    ).strip()

    # ==========================================
    # CHƯA CHỌN BỆNH NHÂN
    # ==========================================

    if not patient_id:

        return render_template(
            "doctor/history.html",

            patient=None,

            history=[],

            patient_id=None,

            search=search,

            date_from=date_from,

            date_to=date_to
        )

    # ==========================================
    # LẤY BỆNH NHÂN
    # ==========================================

    patient = Patient.query.get(patient_id)

    if patient is None:

        flash(
            "Không tìm thấy bệnh nhân.",
            "warning"
        )

        return redirect(
            url_for("doctor.patients")
        )
    if patient.created_by_doctor != current_user.doctor_profile.doctor_id:
        flash("Bạn không có quyền xem bệnh nhân này.", "danger")
        return redirect(url_for("doctor.patients"))

    # ==========================================
    # LẤY LỊCH SỬ AI
    # ==========================================

    history_data = (
        DoctorReportService
        .prediction_history(

            patient_id=patient_id,

            search=search,

            date_from=(
                date_from
                if date_from
                else None
            ),

            date_to=(
                date_to
                if date_to
                else None
            )
        )
    )

    # ==========================================
    # RENDER
    # ==========================================

    return render_template(

        "doctor/history.html",

        patient=patient,

        history=history_data,

        patient_id=patient_id,

        search=search,

        date_from=date_from,

        date_to=date_to
    )

# ==========================================================
# REPORTS
# ==========================================================

@doctor.route("/reports")
@login_required
def reports():

    # ==================================================
    # 1. LẤY THAM SỐ TÌM KIẾM
    # ==================================================

    keyword = request.args.get(
        "keyword",
        "",
        type=str
    ).strip()

    from_date_str = request.args.get(
        "from_date",
        "",
        type=str
    ).strip()

    to_date_str = request.args.get(
        "to_date",
        "",
        type=str
    ).strip()

    page = request.args.get(
        "page",
        1,
        type=int
    )

    # ==================================================
    # 2. CHUYỂN NGÀY
    # ==================================================

    from datetime import datetime, timedelta

    from_date = None
    to_date = None

    if from_date_str:

        try:

            from_date = datetime.strptime(
                from_date_str,
                "%Y-%m-%d"
            )

        except ValueError:

            from_date_str = ""
            from_date = None

    if to_date_str:

        try:

            # cộng 1 ngày để lấy trọn ngày đến
            to_date = (
                datetime.strptime(
                    to_date_str,
                    "%Y-%m-%d"
                )
                + timedelta(days=1)
            )

        except ValueError:

            to_date_str = ""
            to_date = None

    # ==================================================
    # 3. LẤY DỮ LIỆU
    # ==================================================

    pagination = (
        DoctorReportRepository
        .search_reports(
            keyword=keyword,
            from_date=from_date,
            to_date=to_date,
            page=page,
            per_page=10,
            doctor_id=current_user.doctor_profile.doctor_id
        )
    )

    # ==================================================
    # 4. RENDER
    # ==================================================

    return render_template(
        "doctor/report.html",

        reports=pagination.items,

        pagination=pagination,

        keyword=keyword,

        from_date=from_date_str,

        to_date=to_date_str
    )


# ==========================================================
# EXPORT REPORT PDF
#
# /doctor/reports/19/export-pdf
# ==========================================================

@doctor.route(
    "/reports/<int:report_id>/export-pdf"
)
@login_required
def export_report_pdf(report_id):

    # ======================================================
    # 1. REPORT
    # ======================================================

    report = (
        DoctorReportRepository
        .get_by_id(
            report_id
        )
    )

    if report is None:

        flash(
            "Không tìm thấy báo cáo.",
            "danger"
        )

        return redirect(
            url_for(
                "doctor.reports"
            )
        )

    # ======================================================
    # 2. EXAM
    # ======================================================

    exam = report.examination

    if exam is None:

        flash(
            "Không tìm thấy thông tin ca khám.",
            "danger"
        )

        return redirect(
            url_for(
                "doctor.reports"
            )
        )

    # ======================================================
    # 3. PATIENT
    # ======================================================

    patient = exam.patient

    # ======================================================
    # 4. DOCTOR
    # ======================================================

    doctor = report.doctor

    # ======================================================
    # 5. LESION
    # ======================================================

    lesion = (
        LesionImageRepository
        .get_first_by_exam(
            exam.exam_id
        )
    )

    if lesion is None:

        flash(
            "Không tìm thấy ảnh tổn thương.",
            "danger"
        )

        return redirect(
            url_for(
                "doctor.reports"
            )
        )

    # ======================================================
    # 6. AI PREDICTION
    # ======================================================

    prediction_ref = (

        ReportPredictionRef.query

        .filter_by(
            report_id=report.report_id
        )

        .first()

    )

    prediction = None

    results = []

    heatmap = None

    if prediction_ref:

        prediction = (
            prediction_ref.prediction
        )

        if prediction:

            results = (
                AIRepository
                .get_prediction_details(
                    prediction.prediction_id
                )
            )

            heatmap = (
                AIRepository
                .get_heatmap(
                    prediction.prediction_id
                )
            )

    # ======================================================
    # DEBUG
    # ======================================================

    print(
        "=========================================="
    )

    print(
        "PDF REPORT:",
        report.report_id
    )

    print(
        "LESION IMAGE:",
        lesion.image_path
    )

    print(
        "PREDICTION:",
        prediction
    )

    print(
        "AI RESULTS:",
        results
    )

    print(
        "HEATMAP:",
        heatmap
    )

    if heatmap:

        print(
            "HEATMAP PATH:",
            heatmap.heatmap_path
        )

        print(
            "OVERLAY PATH:",
            heatmap.overlay_path
        )

    print(
        "=========================================="
    )

    # ======================================================
    # 7. GENERATE PDF
    # ======================================================

    pdf = PDFService.generate_pdf({

        "patient": patient,

        "doctor": doctor,

        "exam": exam,

        "lesion": lesion,

        "lesion_image": lesion.image_path,

        "prediction": prediction,

        "results": results,

        "report": report,

        "heatmap": heatmap

    })

    # ======================================================
    # 8. RESET BUFFER
    # ======================================================

    pdf.seek(0)

    # ======================================================
    # 9. DOWNLOAD
    # ======================================================

    return send_file(

        pdf,

        download_name=(
            f"SkinAI_Report_{report.report_id}.pdf"
        ),

        mimetype="application/pdf",

        as_attachment=True
    )


# ==========================================================
# SETTINGS
#
# /doctor/settings
# ==========================================================

@doctor.route(
    "/settings",
    methods=["GET", "POST"]
)
@login_required
def settings():

    # ======================================================
    # CHANGE PASSWORD
    # ======================================================

    if request.method == "POST":

        current_password = (
            request.form.get(
                "current_password",
                ""
            ).strip()
        )

        new_password = (
            request.form.get(
                "new_password",
                ""
            ).strip()
        )

        confirm_password = (
            request.form.get(
                "confirm_password",
                ""
            ).strip()
        )

        # --------------------------------------------------
        # Kiểm tra mật khẩu hiện tại
        # --------------------------------------------------

        if not current_password:

            flash(
                "Vui lòng nhập mật khẩu hiện tại.",
                "warning"
            )

            return redirect(
                url_for(
                    "doctor.settings"
                )
            )

        if not check_password_hash(
            current_user.password_hash,
            current_password
        ):

            flash(
                "Mật khẩu hiện tại không chính xác.",
                "danger"
            )

            return redirect(
                url_for(
                    "doctor.settings"
                )
            )

        # --------------------------------------------------
        # Kiểm tra mật khẩu mới
        # --------------------------------------------------

        if not new_password:

            flash(
                "Vui lòng nhập mật khẩu mới.",
                "warning"
            )

            return redirect(
                url_for(
                    "doctor.settings"
                )
            )

        # --------------------------------------------------
        # Độ dài mật khẩu
        # --------------------------------------------------

        if len(new_password) < 6:

            flash(
                "Mật khẩu mới phải có ít nhất 6 ký tự.",
                "warning"
            )

            return redirect(
                url_for(
                    "doctor.settings"
                )
            )

        # --------------------------------------------------
        # Xác nhận mật khẩu
        # --------------------------------------------------

        if new_password != confirm_password:

            flash(
                "Mật khẩu xác nhận không khớp.",
                "danger"
            )

            return redirect(
                url_for(
                    "doctor.settings"
                )
            )

        # --------------------------------------------------
        # Không cho dùng lại mật khẩu cũ
        # --------------------------------------------------

        if check_password_hash(
            current_user.password_hash,
            new_password
        ):

            flash(
                "Mật khẩu mới phải khác mật khẩu hiện tại.",
                "warning"
            )

            return redirect(
                url_for(
                    "doctor.settings"
                )
            )

        # --------------------------------------------------
        # Tạo password hash mới
        # --------------------------------------------------

        current_user.password_hash = (
            generate_password_hash(
                new_password
            )
        )

        db.session.commit()

        flash(
            "Đổi mật khẩu thành công.",
            "success"
        )

        return redirect(
            url_for(
                "doctor.settings"
            )
        )

    # ======================================================
    # DOCTOR PROFILE
    # ======================================================

    doctor_profile = (
        current_user.doctor_profile
    )

    return render_template(
        "doctor/settings.html",
        doctor_profile=doctor_profile
    )


# ==========================================================
# REVIEW
# ==========================================================

@doctor.route(
    "/review/<int:image_id>",
    methods=["GET", "POST"]
)
@login_required
def review(image_id):

# ======================================================
# 1. LẤY ẢNH TỔN THƯƠNG
# ======================================================

    lesion = (
        LesionImageRepository
        .get_by_id(image_id)
    )

    if lesion is None:

        flash(
            "Không tìm thấy ảnh tổn thương.",
            "danger"
        )

        return redirect(
            url_for(
                "doctor.lesions"
            )
        )


    # ======================================================
    # 2. LẤY CA KHÁM
    # ======================================================

    exam = lesion.examination

    if exam is None:

        flash(
            "Không tìm thấy thông tin ca khám.",
            "danger"
        )

        return redirect(
            url_for(
                "lesion.detail",
                image_id=image_id
            )
        )


    # ======================================================
    # 3. LẤY BỆNH NHÂN
    # ======================================================

    patient = exam.patient

    if patient is None:

        flash(
            "Không tìm thấy thông tin bệnh nhân.",
            "danger"
        )

        return redirect(
            url_for(
                "lesion.detail",
                image_id=image_id
            )
        )


    # ======================================================
    # 4. LẤY KẾT QUẢ AI
    # ======================================================

    prediction = (
        AIRepository
        .get_prediction_by_image(
            image_id
        )
    )

    if prediction is None:

        flash(
            "Ảnh này chưa có kết quả AI. "
            "Không thể thực hiện kết luận.",
            "warning"
        )

        return redirect(
            url_for(
                "lesion.detail",
                image_id=image_id
            )
        )


    # ======================================================
    # 5. LẤY CHI TIẾT AI
    # ======================================================

    results = (
        AIRepository
        .get_prediction_details(
            prediction.prediction_id
        )
    )


    # ======================================================
    # 6. LẤY FORM
    # ======================================================

    form = DoctorReviewForm()


    # ======================================================
    # 7. BÁC SĨ XÁC NHẬN
    # ======================================================

    if form.validate_on_submit():

        DoctorReportService.confirm(

            exam.exam_id,

            current_user
            .doctor_profile
            .doctor_id,

            prediction.prediction_id,

            form

        )

        flash(
            "Đã xác nhận kết luận bác sĩ.",
            "success"
        )

        return redirect(
            url_for(
                "lesion.detail",
                image_id=image_id
            )
        )


    # ======================================================
    # 8. RENDER
    # ======================================================

    return render_template(

        "doctor/review.html",

        lesion=lesion,

        exam=exam,

        patient=patient,

        prediction=prediction,

        results=results,

        form=form

    )


# ==========================================================
# ICD-10 LOOKUP
# ==========================================================

@doctor.route("/icd10")
@login_required
def icd10():

    q = request.args.get(
        "q",
        "",
        type=str
    ).strip()

    selected_code = request.args.get(
        "code",
        "",
        type=str
    ).strip()

    # Chưa tìm kiếm
    if not q:
        return render_template(
            "doctor/icd10.html",
            results=[],
            result=None,
            total=0,
            q=""
        )

    keyword = f"%{q}%"

    # ======================================================
    # THÊM MỚI: tìm mã ICD-10 có tên tiếng Việt khớp từ khóa
    # (vì cột *_vi trong DB thường NULL, tên VI chỉ có trong
    # ICD10_CODE_MAPPING ở app code)
    # ======================================================

    vi_matched_codes = search_codes_by_vietnamese_name(q)

    extra_where = ""
    extra_params = {}

    if vi_matched_codes:

        clauses = []

        for i, code in enumerate(vi_matched_codes):
            key = f"vi_code_{i}"
            clauses.append(f"code ILIKE :{key}")
            extra_params[key] = f"{code}%"

        extra_where = " OR " + " OR ".join(clauses)

    # ======================================================
    # TÌM ICD-10 (liệt kê nhiều kết quả để bác sĩ chọn)
    # ======================================================

    sql = text(f"""
        SELECT
            id,
            code,
            code_display,
            short_description_en,
            long_description_en,
            short_description_vi,
            long_description_vi
        FROM icd10
        WHERE
            code ILIKE :keyword
            OR code_display ILIKE :keyword
            OR short_description_en ILIKE :keyword
            OR long_description_en ILIKE :keyword
            OR short_description_vi ILIKE :keyword
            OR long_description_vi ILIKE :keyword
            {extra_where}
        ORDER BY
            CASE
                WHEN UPPER(code) = UPPER(:exact)
                    THEN 0

                WHEN UPPER(code_display) = UPPER(:exact)
                    THEN 1

                WHEN UPPER(code) LIKE UPPER(:prefix)
                    THEN 2

                WHEN LOWER(short_description_en)
                     LIKE LOWER(:prefix)
                    THEN 3

                WHEN LOWER(short_description_vi)
                     LIKE LOWER(:prefix)
                    THEN 4

                ELSE 5
            END,
            code_display ASC
        LIMIT 20
    """)

    rows = db.session.execute(
        sql,
        {
            "keyword": keyword,
            "exact": q,
            "prefix": f"{q}%",
            **extra_params
        }
    ).mappings().all()

    total = len(rows)

    # ======================================================
    # CHUYỂN DANH SÁCH KẾT QUẢ
    # ======================================================

    def build_item(row):

        name_vi = (
            row["short_description_vi"]
            or get_vietnamese_name(
                row["code"],
                row["short_description_en"]
            )
        )

        description_vi = (
            row["long_description_vi"]
            or get_vietnamese_description(
                row["code"],
                row["long_description_en"]
            )
        )

        if not description_vi:
            description_vi = (
                name_vi
                or "Chưa có mô tả tiếng Việt."
            )

        return {

            "id": row["id"],

            "code": row["code"],

            "code_display": row["code_display"],

            "chapter_name": get_chapter_name(row["code"]),

            "name_vi": name_vi,

            "name_en": (
                row["short_description_en"]
                or "Chưa có thông tin"
            ),

            "description_vi": description_vi,

            "description_en": (
                row["long_description_en"]
                or "Chưa có thông tin"
            )
        }

    results = [build_item(row) for row in rows]

    # ======================================================
    # CHỌN KẾT QUẢ ĐANG XEM CHI TIẾT
    #
    # Ưu tiên:
    # 1. Mã bác sĩ bấm chọn (?code=...)
    # 2. Nếu chỉ có đúng 1 kết quả -> tự chọn luôn
    # 3. Ngược lại -> chưa hiện chi tiết, chờ bác sĩ chọn
    # ======================================================

    result_data = None

    if selected_code:

        result_data = next(
            (
                item for item in results
                if item["code_display"] == selected_code
                or item["code"] == selected_code
            ),
            None
        )

    elif total == 1:

        result_data = results[0]

    return render_template(
        "doctor/icd10.html",
        results=results,
        result=result_data,
        total=total,
        q=q,
        selected_code=selected_code
    )


# ==========================================================
# ICD-10 - PHÂN TÍCH BỆNH BẰNG AI (STUB)
# ==========================================================
#
# ⚠️ Đây là route STUB (dữ liệu mẫu cố định), CHƯA gọi AI thật.
# Thay phần TODO bên dưới bằng lệnh gọi Groq API thật,
# giữ đúng cấu trúc JSON trả về để không phải sửa giao diện.
# ==========================================================

@doctor.route(
    "/icd10/analyze",
    methods=["POST"]
)
@login_required
def icd10_analyze():

    data = request.get_json(silent=True) or {}

    code = data.get("code", "")
    name_vi = data.get("name_vi", "")

    if not code or not name_vi:

        return jsonify({
            "success": False,
            "message": "Thiếu mã ICD-10 hoặc tên bệnh."
        }), 400

    analysis = get_analysis(
        code,
        name_vi,
        get_chapter_name(code)
    )

    return jsonify({
        "success": True,
        "code": code,
        "name_vi": name_vi,
        "analysis": analysis,
        "source": "static"
    })


# ==========================================================
# EXPORT PDF BY IMAGE
#
# /doctor/export-pdf/123
# ==========================================================

@doctor.route(
    "/export-pdf/<int:image_id>"
)
@login_required
def export_pdf(image_id):

    # ======================================================
    # 1. LESION
    # ======================================================

    lesion = (
        LesionImageRepository
        .get_by_id(
            image_id
        )
    )

    if lesion is None:

        flash(
            "Không tìm thấy ảnh.",
            "danger"
        )

        return redirect(
            url_for(
                "doctor.lesions"
            )
        )

    # ======================================================
    # 2. PREDICTION
    # ======================================================

    prediction = (
        AIRepository
        .get_prediction_by_image(
            image_id
        )
    )

    if prediction is None:

        flash(
            "Ảnh chưa được AI dự đoán.",
            "warning"
        )

        return redirect(
            url_for(
                "lesion.detail",
                image_id=image_id
            )
        )

    # ======================================================
    # 3. AI RESULTS
    # ======================================================

    results = (
        AIRepository
        .get_prediction_details(
            prediction.prediction_id
        )
    )

    heatmap = (
        AIRepository
        .get_heatmap(
            prediction.prediction_id
        )
    )

    # ======================================================
    # 4. REPORT
    # ======================================================

    report = (
        DoctorReportRepository
        .get_by_image(
            image_id
        )
    )

    # ======================================================
    # 5. EXAM
    # ======================================================

    exam = lesion.examination

    if exam is None:

        flash(
            "Không tìm thấy ca khám.",
            "danger"
        )

        return redirect(
            url_for(
                "lesion.detail",
                image_id=image_id
            )
        )

    # ======================================================
    # 6. PATIENT
    # ======================================================

    patient = exam.patient

    # ======================================================
    # 7. DOCTOR
    # ======================================================

    doctor = (

        report.doctor

        if report

        else exam.doctor

    )

    # ======================================================
    # 8. DEBUG
    # ======================================================

    print(
        "=========================================="
    )

    print(
        "EXPORT BY IMAGE:",
        image_id
    )

    print(
        "IMAGE PATH:",
        lesion.image_path
    )

    print(
        "PREDICTION:",
        prediction
    )

    print(
        "RESULTS:",
        results
    )

    print(
        "HEATMAP:",
        heatmap
    )

    print(
        "=========================================="
    )

    # ======================================================
    # 9. GENERATE PDF
    # ======================================================

    pdf = PDFService.generate_pdf({

        "patient": patient,

        "doctor": doctor,

        "exam": exam,

        "lesion": lesion,

        "lesion_image": lesion.image_path,

        "prediction": prediction,

        "results": results,

        "report": report,

        "heatmap": heatmap

    })

    # ======================================================
    # 10. RESET BUFFER
    # ======================================================

    pdf.seek(0)

    # ======================================================
    # 11. DOWNLOAD
    # ======================================================

    return send_file(

        pdf,

        download_name=(
            f"SkinAI_Report_{image_id}.pdf"
        ),

        mimetype="application/pdf",

        as_attachment=True
    )

