from io import BytesIO
from pathlib import Path
from datetime import datetime

from flask import current_app

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import mm

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image as RLImage,
)


# ==========================================================
# FONT
# ==========================================================

FONT_REGULAR = "Arial"
FONT_BOLD = "Arial-Bold"


def register_fonts():

    registered = pdfmetrics.getRegisteredFontNames()

    # Arial Regular
    if FONT_REGULAR not in registered:

        pdfmetrics.registerFont(
            TTFont(
                FONT_REGULAR,
                r"C:\Windows\Fonts\arial.ttf"
            )
        )

    # Arial Bold
    if FONT_BOLD not in registered:

        pdfmetrics.registerFont(
            TTFont(
                FONT_BOLD,
                r"C:\Windows\Fonts\arialbd.ttf"
            )
        )


# Đăng ký font khi import
register_fonts()


class PDFService:

    # ======================================================
    # GET VALUE
    # Hỗ trợ cả DICT và OBJECT
    # ======================================================

    @staticmethod
    def _get_value(data, key, default=None):

        if data is None:
            return default

        # Nếu là dictionary
        if isinstance(data, dict):
            return data.get(key, default)

        # Nếu là object / SQLAlchemy model
        return getattr(
            data,
            key,
            default
        )

        # ======================================================
        # ẨN DANH BỆNH NHÂN (PRIVACY)
        # ======================================================

    @staticmethod
    def _mask_name(fullname):
        """
        Che tên bệnh nhân, chỉ giữ chữ cái đầu mỗi từ.
        Vd: "Nguyễn Văn An" -> "N** V** A*"
        """

        if not fullname:
            return ""

        words = str(fullname).strip().split()

        masked_words = []

        for word in words:

            if len(word) <= 1:
                masked_words.append(word)
            else:
                masked_words.append(
                    word[0] + "*" * (len(word) - 1)
                )

        return " ".join(masked_words)

    @staticmethod
    def _mask_phone(phone):
        """
        Che số điện thoại, giữ lại 3 số đầu và 3 số cuối.
        Vd: "0901234567" -> "090****567"
        """

        if not phone:
            return ""

        phone = str(phone).strip()

        if len(phone) <= 6:
            return "*" * len(phone)

        return (
                phone[:3]
                + "*" * (len(phone) - 6)
                + phone[-3:]
        )

    # ======================================================
    # RESOLVE FILE
    # ======================================================

    @staticmethod
    def _resolve_file(file_path):

        if not file_path:
            return None

        raw_path = str(file_path).strip()

        if not raw_path:
            return None

        # --------------------------------------------------
        # Nếu đã là file tuyệt đối
        # --------------------------------------------------

        path = Path(raw_path)

        if path.is_absolute():

            path = path.resolve()

            if path.is_file():

                print(
                    "✅ PDF FILE:",
                    path
                )

                return str(path)

        # --------------------------------------------------
        # Chuẩn hóa slash
        # --------------------------------------------------

        clean_path = raw_path.replace(
            "\\",
            "/"
        )

        clean_path = clean_path.lstrip("/")

        root_path = Path(
            current_app.root_path
        ).resolve()

        static_path = Path(
            current_app.static_folder
        ).resolve()

        # --------------------------------------------------
        # Nếu database lưu dạng:
        #
        # static/uploads/original/xxx.png
        # --------------------------------------------------

        if clean_path.startswith(
            "static/"
        ):

            clean_path = clean_path[
                len("static/"):
            ]

        # --------------------------------------------------
        # Các vị trí có thể chứa file
        # --------------------------------------------------

        candidates = [

            # app/static/...
            static_path / clean_path,

            # app/...
            root_path / clean_path,

            # app/static/...
            root_path / "static" / clean_path,

            # project/uploads/...
            root_path.parent / clean_path,

            # app/uploads/...
            root_path / "uploads" / Path(
                clean_path
            ).name,

            # app/static/uploads/...
            static_path / "uploads" / Path(
                clean_path
            ).name,
        ]

        for candidate in candidates:

            try:

                candidate = candidate.resolve()

                if candidate.is_file():

                    print(
                        "✅ PDF FILE:",
                        candidate
                    )

                    return str(candidate)

            except Exception as e:

                print(
                    "⚠️ PDF PATH ERROR:",
                    candidate,
                    e
                )

        print(
            "❌ PDF FILE NOT FOUND:",
            raw_path
        )

        return None

    # ======================================================
    # STYLES
    # ======================================================

    @staticmethod
    def _get_styles():

        styles = getSampleStyleSheet()

        # --------------------------------------------------
        # NORMAL
        # --------------------------------------------------

        styles["Normal"].fontName = FONT_REGULAR
        styles["Normal"].fontSize = 10
        styles["Normal"].leading = 14
        styles["Normal"].textColor = colors.HexColor(
            "#222222"
        )

        # --------------------------------------------------
        # TITLE
        # --------------------------------------------------

        styles.add(
            ParagraphStyle(
                name="ReportTitle",
                fontName=FONT_BOLD,
                fontSize=18,
                leading=22,
                alignment=TA_CENTER,
                textColor=colors.HexColor(
                    "#1f5f8b"
                ),
                spaceAfter=5,
            )
        )

        # --------------------------------------------------
        # SUBTITLE
        # --------------------------------------------------

        styles.add(
            ParagraphStyle(
                name="ReportSubtitle",
                fontName=FONT_REGULAR,
                fontSize=9,
                leading=12,
                alignment=TA_CENTER,
                textColor=colors.HexColor(
                    "#666666"
                ),
                spaceAfter=12,
            )
        )

        # --------------------------------------------------
        # HOSPITAL
        # --------------------------------------------------

        styles.add(
            ParagraphStyle(
                name="Hospital",
                fontName=FONT_BOLD,
                fontSize=11,
                leading=14,
                alignment=TA_CENTER,
                textColor=colors.HexColor(
                    "#1f5f8b"
                ),
                spaceAfter=4,
            )
        )

        # --------------------------------------------------
        # SECTION
        # --------------------------------------------------

        styles.add(
            ParagraphStyle(
                name="SectionHeading",
                fontName=FONT_BOLD,
                fontSize=11,
                leading=14,
                textColor=colors.white,
                spaceBefore=10,
                spaceAfter=6,
            )
        )

        # --------------------------------------------------
        # CELL
        # --------------------------------------------------

        styles.add(
            ParagraphStyle(
                name="CellText",
                fontName=FONT_REGULAR,
                fontSize=9.5,
                leading=12,
            )
        )

        styles.add(
            ParagraphStyle(
                name="CellBold",
                fontName=FONT_BOLD,
                fontSize=9.5,
                leading=12,
            )
        )

        styles.add(
            ParagraphStyle(
                name="CellHeader",
                fontName=FONT_BOLD,
                fontSize=9,
                leading=11,
                alignment=TA_CENTER,
                textColor=colors.white,
            )
        )

        # --------------------------------------------------
        # IMAGE TITLE
        # --------------------------------------------------

        styles.add(
            ParagraphStyle(
                name="ImageTitle",
                fontName=FONT_BOLD,
                fontSize=10,
                leading=13,
                alignment=TA_CENTER,
                spaceAfter=5,
            )
        )

        # --------------------------------------------------
        # WARNING
        # --------------------------------------------------

        styles.add(
            ParagraphStyle(
                name="Warning",
                fontName=FONT_REGULAR,
                fontSize=9.5,
                leading=13,
                textColor=colors.HexColor(
                    "#7c6500"
                ),
            )
        )

        # --------------------------------------------------
        # FOOTER
        # --------------------------------------------------

        styles.add(
            ParagraphStyle(
                name="Footer",
                fontName=FONT_REGULAR,
                fontSize=8,
                leading=10,
                alignment=TA_CENTER,
                textColor=colors.HexColor(
                    "#777777"
                ),
            )
        )

        return styles

    # ======================================================
    # HEADER / FOOTER
    # ======================================================

    @staticmethod
    def _draw_header_footer(
        canvas,
        doc
    ):

        canvas.saveState()

        width, height = A4

        # --------------------------------------------------
        # HEADER BAR
        # --------------------------------------------------

        canvas.setFillColor(
            colors.HexColor("#1f5f8b")
        )

        canvas.rect(
            0,
            height - 8 * mm,
            width,
            8 * mm,
            fill=1,
            stroke=0
        )

        # --------------------------------------------------
        # HEADER TEXT
        # --------------------------------------------------

        canvas.setFillColor(
            colors.white
        )

        canvas.setFont(
            FONT_BOLD,
            9
        )

        canvas.drawString(
            18 * mm,
            height - 5.5 * mm,
            "SKINAI CLINICAL"
        )

        canvas.setFont(
            FONT_REGULAR,
            8
        )

        canvas.drawRightString(
            width - 18 * mm,
            height - 5.5 * mm,
            "Hệ thống hỗ trợ phân tích tổn thương da bằng AI"
        )

        # --------------------------------------------------
        # FOOTER LINE
        # --------------------------------------------------

        canvas.setStrokeColor(
            colors.HexColor("#cccccc")
        )

        canvas.line(
            18 * mm,
            14 * mm,
            width - 18 * mm,
            14 * mm
        )

        # --------------------------------------------------
        # FOOTER TEXT
        # --------------------------------------------------

        canvas.setFillColor(
            colors.HexColor("#777777")
        )

        canvas.setFont(
            FONT_REGULAR,
            7.5
        )

        canvas.drawString(
            18 * mm,
            9 * mm,
            f"In lúc: {datetime.now().strftime('%d/%m/%Y %H:%M')}"
        )

        canvas.drawRightString(
            width - 18 * mm,
            9 * mm,
            f"Trang {doc.page}"
        )

        canvas.restoreState()

    # ======================================================
    # ESCAPE TEXT
    # ======================================================

    @staticmethod
    def _escape_text(text):

        if text is None:
            return ""

        return (
            str(text)
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )

    # ======================================================
    # PARAGRAPH
    # ======================================================

    @staticmethod
    def _p(
        text,
        style
    ):

        return Paragraph(
            PDFService._escape_text(text),
            style
        )

    # ======================================================
    # HTML PARAGRAPH
    # ======================================================

    @staticmethod
    def _p_html(
        text,
        style
    ):

        if text is None:
            text = ""

        return Paragraph(
            str(text),
            style
        )

    # ======================================================
    # SECTION HEADER
    # ======================================================

    @staticmethod
    def _section(
        title,
        styles
    ):

        table = Table(
            [[
                Paragraph(
                    title,
                    styles["SectionHeading"]
                )
            ]],
            colWidths=[
                170 * mm
            ]
        )

        table.setStyle(
            TableStyle([
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, -1),
                    colors.HexColor("#1f5f8b")
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    7
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    7
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    4
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    2
                ),
            ])
        )

        return table

    # ======================================================
    # INFO TABLE
    # ======================================================

    @staticmethod
    def _info_table(
        rows,
        styles
    ):

        data = []

        for row in rows:

            converted = []

            for index, value in enumerate(row):

                if index % 2 == 0:

                    converted.append(
                        PDFService._p(
                            value,
                            styles["CellBold"]
                        )
                    )

                else:

                    converted.append(
                        PDFService._p(
                            value,
                            styles["CellText"]
                        )
                    )

            data.append(converted)

        table = Table(
            data,
            colWidths=[
                32 * mm,
                53 * mm,
                32 * mm,
                53 * mm,
            ]
        )

        table.setStyle(
            TableStyle([
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.HexColor("#cccccc")
                ),
                (
                    "BACKGROUND",
                    (0, 0),
                    (0, -1),
                    colors.HexColor("#f3f4f6")
                ),
                (
                    "BACKGROUND",
                    (2, 0),
                    (2, -1),
                    colors.HexColor("#f3f4f6")
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "TOP"
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    6
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    6
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    5
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    5
                ),
            ])
        )

        return table

    # ======================================================
    # GENERATE PDF
    # ======================================================

    @staticmethod
    def generate_pdf(context):

        register_fonts()

        styles = PDFService._get_styles()

        # ==================================================
        # MEMORY PDF
        # ==================================================

        pdf_buffer = BytesIO()

        doc = SimpleDocTemplate(

            pdf_buffer,

            pagesize=A4,

            rightMargin=20 * mm,
            leftMargin=20 * mm,

            topMargin=24 * mm,
            bottomMargin=20 * mm,

            title="SkinAI Clinical Report",

            author="SkinAI Clinical",
        )

        story = []

        # ==================================================
        # DATA
        # ==================================================

        patient = context.get("patient")
        doctor = context.get("doctor")
        exam = context.get("exam")
        lesion = context.get("lesion")

        results = (
            context.get("results")
            or []
        )

        report = context.get("report")

        heatmap = context.get("heatmap")

        # ==================================================
        # HEADER
        # ==================================================

        story.append(
            PDFService._p(
                "SKINAI CLINICAL",
                styles["Hospital"]
            )
        )

        story.append(
            PDFService._p(
                "PHIẾU KẾT LUẬN DA LIỄU",
                styles["ReportTitle"]
            )
        )

        story.append(
            PDFService._p(
                "Báo cáo kết quả phân tích tổn thương da",
                styles["ReportSubtitle"]
            )
        )

        # ==================================================
        # 1. PATIENT
        # ==================================================

        story.append(
            PDFService._section(
                "1. THÔNG TIN BỆNH NHÂN",
                styles
            )
        )

        story.append(
            Spacer(1, 4)
        )

        birth_year = PDFService._get_value(
            patient,
            "birth_year"
        )

        exam_date = PDFService._get_value(
            exam,
            "exam_date"
        )

        exam_date_text = (
            exam_date.strftime(
                "%d/%m/%Y %H:%M"
            )
            if exam_date
            else "Không xác định"
        )

        fullname_display = PDFService._mask_name(
            PDFService._get_value(patient, "fullname", "")
        )
        phone_display = PDFService._mask_phone(
            PDFService._get_value(patient, "phone", "")
        )

        story.append(
            PDFService._info_table(
                [
                    [
                        "Họ và tên",
                        fullname_display,
                        "Mã bệnh nhân",
                        PDFService._get_value(
                            patient,
                            "patient_code",
                            ""
                        ),
                    ],
                    [
                        "Giới tính",
                        PDFService._get_value(
                            patient,
                            "gender"
                        ) or "Không xác định",
                        "Năm sinh",
                        birth_year or "Không xác định",
                    ],
                    [
                         "Số điện thoại",
                        phone_display,
                        "Ngày khám",
                        exam_date_text,
                    ],
                ],
                styles
            )
        )

        story.append(
            Spacer(1, 8)
        )

        # ==================================================
        # 2. EXAM
        # ==================================================

        story.append(
            PDFService._section(
                "2. THÔNG TIN KHÁM",
                styles
            )
        )

        story.append(
            Spacer(1, 4)
        )

        story.append(
            PDFService._info_table(
                [
                    [
                        "Bác sĩ",
                        PDFService._get_value(
                            doctor,
                            "fullname",
                            ""
                        ),
                        "",
                        "",
                    ],
                    [
                        "Bệnh viện / Cơ sở",
                        PDFService._get_value(
                            doctor,
                            "hospital"
                        ) or "SKINAI CLINICAL",
                        "",
                        "",
                    ],
                    [
                        "Chuyên khoa",
                        PDFService._get_value(
                            doctor,
                            "department"
                        ) or "Da liễu",
                        "",
                        "",
                    ],
                    [
                        "Lý do khám",
                        PDFService._get_value(
                            exam,
                            "chief_complaint"
                        ) or "Không ghi nhận",
                        "",
                        "",
                    ],
                ],
                styles
            )
        )

        story.append(
            Spacer(1, 8)
        )

        # ==================================================
        # 3. LESION IMAGE
        # ==================================================

        story.append(
            PDFService._section(
                "3. HÌNH ẢNH TỔN THƯƠNG",
                styles
            )
        )

        story.append(
            Spacer(1, 5)
        )

        lesion_image_path = PDFService._resolve_file(
            context.get("lesion_image")
        )

        if lesion_image_path:

            image = RLImage(
                lesion_image_path,
                width=75 * mm,
                height=75 * mm,
                kind="proportional"
            )

            image_table = Table(
                [[image]],
                colWidths=[
                    170 * mm
                ]
            )

            image_table.setStyle(
                TableStyle([
                    (
                        "ALIGN",
                        (0, 0),
                        (-1, -1),
                        "CENTER"
                    ),
                    (
                        "VALIGN",
                        (0, 0),
                        (-1, -1),
                        "MIDDLE"
                    ),
                    (
                        "BOX",
                        (0, 0),
                        (-1, -1),
                        0.5,
                        colors.HexColor("#cccccc")
                    ),
                    (
                        "TOPPADDING",
                        (0, 0),
                        (-1, -1),
                        8
                    ),
                    (
                        "BOTTOMPADDING",
                        (0, 0),
                        (-1, -1),
                        8
                    ),
                ])
            )

            story.append(
                image_table
            )

        else:

            story.append(
                PDFService._p(
                    "Không có hình ảnh tổn thương.",
                    styles["CellText"]
                )
            )

        story.append(
            Spacer(1, 5)
        )

        blur_score = (
            PDFService._get_value(
                lesion,
                "blur_score",
                0
            )
            or 0
        )

        quality_score = (
            PDFService._get_value(
                lesion,
                "quality_score",
                0
            )
            or 0
        )

        quality_table = Table(
            [[
                PDFService._p(
                    "Blur Score",
                    styles["CellBold"]
                ),
                PDFService._p(
                    f"{float(blur_score):.2f}",
                    styles["CellText"]
                ),
                PDFService._p(
                    "Chất lượng ảnh",
                    styles["CellBold"]
                ),
                PDFService._p(
                    f"{float(quality_score):.2f}",
                    styles["CellText"]
                ),
            ]],
            colWidths=[
                32 * mm,
                53 * mm,
                32 * mm,
                53 * mm,
            ]
        )

        quality_table.setStyle(
            TableStyle([
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.HexColor("#cccccc")
                ),
                (
                    "BACKGROUND",
                    (0, 0),
                    (0, 0),
                    colors.HexColor("#f3f4f6")
                ),
                (
                    "BACKGROUND",
                    (2, 0),
                    (2, 0),
                    colors.HexColor("#f3f4f6")
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    5
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    5
                ),
            ])
        )

        story.append(
            quality_table
        )

        story.append(
            Spacer(1, 8)
        )

        # ==================================================
        # 4. AI RESULTS
        # ==================================================

        story.append(
            PDFService._section(
                "4. KẾT QUẢ PHÂN TÍCH AI",
                styles
            )
        )

        story.append(
            Spacer(1, 5)
        )

        if results:

            prediction_data = [[

                PDFService._p(
                    "Hạng",
                    styles["CellHeader"]
                ),

                PDFService._p(
                    "Chẩn đoán dự đoán",
                    styles["CellHeader"]
                ),

                PDFService._p(
                    "Mức nguy hiểm",
                    styles["CellHeader"]
                ),

                PDFService._p(
                    "Độ tin cậy",
                    styles["CellHeader"]
                ),

            ]]

            for item in results:

                # ==========================================
                # QUAN TRỌNG:
                # item là DICT
                # ==========================================

                disease = PDFService._get_value(
                    item,
                    "disease"
                )

                if disease:

                    disease_name = (
                        PDFService._get_value(
                            disease,
                            "disease_name_vi"
                        )
                        or PDFService._get_value(
                            disease,
                            "name_vi"
                        )
                        or "Không xác định"
                    )

                    risk = (
                        PDFService._get_value(
                            disease,
                            "risk_level"
                        )
                        or "Không xác định"
                    )

                else:

                    disease_name = (
                        PDFService._get_value(
                            item,
                            "predicted_class"
                        )
                        or "Không xác định"
                    )

                    risk = "Không xác định"

                confidence = (
                    PDFService._get_value(
                        item,
                        "confidence",
                        0
                    )
                    or 0
                )

                confidence = float(
                    confidence
                ) * 100

                rank = PDFService._get_value(
                    item,
                    "rank",
                    ""
                )

                prediction_data.append([

                    PDFService._p(
                        str(rank),
                        styles["CellText"]
                    ),

                    PDFService._p(
                        disease_name,
                        styles["CellText"]
                    ),

                    PDFService._p(
                        risk,
                        styles["CellText"]
                    ),

                    PDFService._p(
                        f"{confidence:.2f}%",
                        styles["CellText"]
                    ),

                ])

            prediction_table = Table(
                prediction_data,
                colWidths=[
                    18 * mm,
                    70 * mm,
                    40 * mm,
                    42 * mm,
                ],
                repeatRows=1
            )

            prediction_table.setStyle(
                TableStyle([
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        colors.HexColor("#1f5f8b")
                    ),
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.5,
                        colors.HexColor("#cccccc")
                    ),
                    (
                        "ALIGN",
                        (0, 0),
                        (0, -1),
                        "CENTER"
                    ),
                    (
                        "ALIGN",
                        (-1, 0),
                        (-1, -1),
                        "CENTER"
                    ),
                    (
                        "VALIGN",
                        (0, 0),
                        (-1, -1),
                        "MIDDLE"
                    ),
                    (
                        "TOPPADDING",
                        (0, 0),
                        (-1, -1),
                        5
                    ),
                    (
                        "BOTTOMPADDING",
                        (0, 0),
                        (-1, -1),
                        5
                    ),
                ])
            )

            story.append(
                prediction_table
            )

        else:

            story.append(
                PDFService._p(
                    "Không có dữ liệu phân tích AI.",
                    styles["CellText"]
                )
            )

        story.append(
            Spacer(1, 8)
        )

        # ==================================================
        # 5. TOP 1
        # ==================================================

        if results:

            top = results[0]

            disease = PDFService._get_value(
                top,
                "disease"
            )

            if disease:

                disease_name = (
                    PDFService._get_value(
                        disease,
                        "disease_name_vi"
                    )
                    or PDFService._get_value(
                        disease,
                        "name_vi"
                    )
                    or "Không xác định"
                )

                risk = (
                    PDFService._get_value(
                        disease,
                        "risk_level"
                    )
                    or "Không xác định"
                )

            else:

                disease_name = (
                    PDFService._get_value(
                        top,
                        "predicted_class"
                    )
                    or "Không xác định"
                )

                risk = "Không xác định"

            confidence = (
                PDFService._get_value(
                    top,
                    "confidence",
                    0
                )
                or 0
            )

            confidence = float(
                confidence
            ) * 100

            story.append(
                PDFService._section(
                    "5. KẾT QUẢ AI CAO NHẤT",
                    styles
                )
            )

            story.append(
                Spacer(1, 5)
            )

            top_data = [

                [
                    PDFService._p(
                        "Hệ thống AI nhận diện tổn thương có khả năng cao nhất là:",
                        styles["CellText"]
                    )
                ],

                [
                    PDFService._p(
                        disease_name,
                        styles["CellBold"]
                    )
                ],

                [
                    PDFService._p(
                        f"Độ tin cậy: {confidence:.2f}%",
                        styles["CellText"]
                    )
                ],

                [
                    PDFService._p(
                        f"Mức nguy hiểm: {risk}",
                        styles["CellText"]
                    )
                ]

            ]

            top_table = Table(
                top_data,
                colWidths=[
                    170 * mm
                ]
            )

            top_table.setStyle(
                TableStyle([
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, -1),
                        colors.HexColor("#f3f8fb")
                    ),
                    (
                        "BOX",
                        (0, 0),
                        (-1, -1),
                        1,
                        colors.HexColor("#9db7c8")
                    ),
                    (
                        "LEFTPADDING",
                        (0, 0),
                        (-1, -1),
                        10
                    ),
                    (
                        "RIGHTPADDING",
                        (0, 0),
                        (-1, -1),
                        10
                    ),
                    (
                        "TOPPADDING",
                        (0, 0),
                        (-1, -1),
                        6
                    ),
                    (
                        "BOTTOMPADDING",
                        (0, 0),
                        (-1, -1),
                        6
                    ),
                ])
            )

            story.append(
                top_table
            )

            story.append(
                Spacer(1, 8)
            )

        # ==================================================
        # 6. GRADCAM
        # ==================================================

        story.append(
            PDFService._section(
                "6. GIẢI THÍCH KẾT QUẢ AI - GRADCAM",
                styles
            )
        )

        story.append(
            Spacer(1, 5)
        )

        heatmap_path = None
        overlay_path = None

        if heatmap:

            heatmap_path = PDFService._resolve_file(
                PDFService._get_value(
                    heatmap,
                    "heatmap_path"
                )
            )

            overlay_path = PDFService._resolve_file(
                PDFService._get_value(
                    heatmap,
                    "overlay_path"
                )
            )

        # --------------------------------------------------
        # HEATMAP
        # --------------------------------------------------

        heatmap_cell = [

            PDFService._p(
                "Grad-CAM Heatmap",
                styles["ImageTitle"]
            )

        ]

        if heatmap_path:

            try:

                heatmap_cell.append(
                    RLImage(
                        heatmap_path,
                        width=55 * mm,
                        height=55 * mm,
                        kind="proportional"
                    )
                )

            except Exception as e:

                print(
                    "❌ HEATMAP IMAGE ERROR:",
                    e
                )

                heatmap_cell.append(
                    PDFService._p(
                        "Không thể đọc Heatmap.",
                        styles["CellText"]
                    )
                )

        else:

            heatmap_cell.append(
                PDFService._p(
                    "Không có Heatmap.",
                    styles["CellText"]
                )
            )

        # --------------------------------------------------
        # OVERLAY
        # --------------------------------------------------

        overlay_cell = [

            PDFService._p(
                "Grad-CAM Overlay",
                styles["ImageTitle"]
            )

        ]

        if overlay_path:

            try:

                overlay_cell.append(
                    RLImage(
                        overlay_path,
                        width=55 * mm,
                        height=55 * mm,
                        kind="proportional"
                    )
                )

            except Exception as e:

                print(
                    "❌ OVERLAY IMAGE ERROR:",
                    e
                )

                overlay_cell.append(
                    PDFService._p(
                        "Không thể đọc Overlay.",
                        styles["CellText"]
                    )
                )

        else:

            overlay_cell.append(
                PDFService._p(
                    "Không có Overlay.",
                    styles["CellText"]
                )
            )

        gradcam_table = Table(
            [[
                heatmap_cell,
                overlay_cell
            ]],
            colWidths=[
                85 * mm,
                85 * mm
            ]
        )

        gradcam_table.setStyle(
            TableStyle([
                (
                    "ALIGN",
                    (0, 0),
                    (-1, -1),
                    "CENTER"
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "TOP"
                ),
                (
                    "BOX",
                    (0, 0),
                    (0, 0),
                    0.5,
                    colors.HexColor("#cccccc")
                ),
                (
                    "BOX",
                    (1, 0),
                    (1, 0),
                    0.5,
                    colors.HexColor("#cccccc")
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    8
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    8
                ),
            ])
        )

        story.append(
            gradcam_table
        )

        story.append(
            Spacer(1, 8)
        )

        # ==================================================
        # 7. DISEASE INFO
        # ==================================================

        if results:

            top = results[0]

            disease = PDFService._get_value(
                top,
                "disease"
            )

            if disease:

                story.append(
                    PDFService._section(
                        "7. THÔNG TIN TỔN THƯƠNG",
                        styles
                    )
                )

                story.append(
                    Spacer(1, 4)
                )

                disease_data = [

                    [
                        PDFService._p(
                            "Tên bệnh",
                            styles["CellBold"]
                        ),
                        PDFService._p(
                            PDFService._get_value(
                                disease,
                                "disease_name_vi"
                            ) or "Chưa cập nhật",
                            styles["CellText"]
                        )
                    ],

                    [
                        PDFService._p(
                            "Tên tiếng Anh",
                            styles["CellBold"]
                        ),
                        PDFService._p(
                            PDFService._get_value(
                                disease,
                                "disease_name"
                            ) or "Chưa cập nhật",
                            styles["CellText"]
                        )
                    ],

                    [
                        PDFService._p(
                            "Mã bệnh",
                            styles["CellBold"]
                        ),
                        PDFService._p(
                            PDFService._get_value(
                                disease,
                                "disease_code"
                            ) or "Chưa cập nhật",
                            styles["CellText"]
                        )
                    ],

                    [
                        PDFService._p(
                            "ICD-10",
                            styles["CellBold"]
                        ),
                        PDFService._p(
                            PDFService._get_value(
                                disease,
                                "icd10_code"
                            ) or "Chưa cập nhật",
                            styles["CellText"]
                        )
                    ],

                    [
                        PDFService._p(
                            "Nhóm bệnh",
                            styles["CellBold"]
                        ),
                        PDFService._p(
                            PDFService._get_value(
                                disease,
                                "category"
                            ) or "Chưa cập nhật",
                            styles["CellText"]
                        )
                    ],

                    [
                        PDFService._p(
                            "Điều trị tham khảo",
                            styles["CellBold"]
                        ),
                        PDFService._p(
                            PDFService._get_value(
                                disease,
                                "treatment"
                            ) or "Chưa cập nhật",
                            styles["CellText"]
                        )
                    ],

                    [
                        PDFService._p(
                            "Theo dõi tham khảo",
                            styles["CellBold"]
                        ),
                        PDFService._p(
                            PDFService._get_value(
                                disease,
                                "follow_up"
                            ) or "Chưa cập nhật",
                            styles["CellText"]
                        )
                    ]

                ]

                disease_table = Table(
                    disease_data,
                    colWidths=[
                        45 * mm,
                        125 * mm
                    ]
                )

                disease_table.setStyle(
                    TableStyle([
                        (
                            "GRID",
                            (0, 0),
                            (-1, -1),
                            0.5,
                            colors.HexColor("#cccccc")
                        ),
                        (
                            "BACKGROUND",
                            (0, 0),
                            (0, -1),
                            colors.HexColor("#f3f4f6")
                        ),
                        (
                            "VALIGN",
                            (0, 0),
                            (-1, -1),
                            "TOP"
                        ),
                        (
                            "LEFTPADDING",
                            (0, 0),
                            (-1, -1),
                            6
                        ),
                        (
                            "RIGHTPADDING",
                            (0, 0),
                            (-1, -1),
                            6
                        ),
                        (
                            "TOPPADDING",
                            (0, 0),
                            (-1, -1),
                            5
                        ),
                        (
                            "BOTTOMPADDING",
                            (0, 0),
                            (-1, -1),
                            5
                        ),
                    ])
                )

                story.append(
                    disease_table
                )

                story.append(
                    Spacer(1, 8)
                )

        # ==================================================
        # WARNING
        # ==================================================

        warning_data = [[

            PDFService._p_html(
                "<b>LƯU Ý QUAN TRỌNG VỀ KẾT QUẢ AI</b><br/><br/>"
                "Kết quả phân tích trong báo cáo này được tạo bởi "
                "hệ thống trí tuệ nhân tạo (AI) nhằm mục đích tham khảo "
                "và hỗ trợ bác sĩ trong quá trình đánh giá.<br/><br/>"
                "Kết quả AI không thay thế chẩn đoán, kết luận hoặc "
                "chỉ định điều trị của bác sĩ.<br/><br/>"
                "Kết luận chuyên môn cuối cùng phải được đưa ra dựa "
                "trên kết quả thăm khám lâm sàng, hình ảnh, tiền sử bệnh "
                "và đánh giá của bác sĩ chuyên khoa.",
                styles["Warning"]
            )

        ]]

        warning_table = Table(
            warning_data,
            colWidths=[
                170 * mm
            ]
        )

        warning_table.setStyle(
            TableStyle([
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, -1),
                    colors.HexColor("#fff8dc")
                ),
                (
                    "BOX",
                    (0, 0),
                    (-1, -1),
                    1,
                    colors.HexColor("#d6a700")
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    10
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    10
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    8
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    8
                ),
            ])
        )

        story.append(
            warning_table
        )

        story.append(
            Spacer(1, 8)
        )

        # ==================================================
        # 8. DOCTOR CONCLUSION
        # ==================================================

        story.append(
            PDFService._section(
                "8. KẾT LUẬN CỦA BÁC SĨ",
                styles
            )
        )

        story.append(
            Spacer(1, 4)
        )

        if report:

            confirmed_at = PDFService._get_value(
                report,
                "confirmed_at"
            )

            confirmed_text = (

                confirmed_at.strftime(
                    "%d/%m/%Y %H:%M"
                )

                if confirmed_at

                else "Không xác định"

            )

            report_data = [

                [
                    PDFService._p(
                        "Chẩn đoán",
                        styles["CellBold"]
                    ),
                    PDFService._p(
                        PDFService._get_value(
                            report,
                            "diagnosis"
                        ) or "Không ghi nhận",
                        styles["CellText"]
                    )
                ],

                [
                    PDFService._p(
                        "Điều trị",
                        styles["CellBold"]
                    ),
                    PDFService._p(
                        PDFService._get_value(
                            report,
                            "treatment"
                        ) or "Không ghi nhận",
                        styles["CellText"]
                    )
                ],

                [
                    PDFService._p(
                        "Ghi chú",
                        styles["CellBold"]
                    ),
                    PDFService._p(
                        PDFService._get_value(
                            report,
                            "note"
                        ) or "Không có",
                        styles["CellText"]
                    )
                ],

                [
                    PDFService._p(
                        "Trạng thái",
                        styles["CellBold"]
                    ),
                    PDFService._p(
                        PDFService._get_value(
                            report,
                            "status"
                        ) or "Không xác định",
                        styles["CellText"]
                    )
                ],

                [
                    PDFService._p(
                        "Thời gian xác nhận",
                        styles["CellBold"]
                    ),
                    PDFService._p(
                        confirmed_text,
                        styles["CellText"]
                    )
                ]

            ]

            report_table = Table(
                report_data,
                colWidths=[
                    45 * mm,
                    125 * mm
                ]
            )

            report_table.setStyle(
                TableStyle([
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.5,
                        colors.HexColor("#cccccc")
                    ),
                    (
                        "BACKGROUND",
                        (0, 0),
                        (0, -1),
                        colors.HexColor("#f3f4f6")
                    ),
                    (
                        "VALIGN",
                        (0, 0),
                        (-1, -1),
                        "TOP"
                    ),
                    (
                        "LEFTPADDING",
                        (0, 0),
                        (-1, -1),
                        6
                    ),
                    (
                        "RIGHTPADDING",
                        (0, 0),
                        (-1, -1),
                        6
                    ),
                    (
                        "TOPPADDING",
                        (0, 0),
                        (-1, -1),
                        6
                    ),
                    (
                        "BOTTOMPADDING",
                        (0, 0),
                        (-1, -1),
                        6
                    ),
                ])
            )

            story.append(
                report_table
            )

        else:

            story.append(
                PDFService._p(
                    "Chưa có kết luận của bác sĩ.",
                    styles["CellText"]
                )
            )

        # ==================================================
        # SIGNATURE
        # ==================================================

        story.append(
            Spacer(1, 25)
        )

        signature_data = [

            [
                "",
                PDFService._p(
                    "Ngày ..... tháng ..... năm ......",
                    styles["CellText"]
                )
            ],

            [
                "",
                PDFService._p(
                    "BÁC SĨ ĐIỀU TRỊ",
                    styles["CellBold"]
                )
            ],

            [
                "",
                PDFService._p(
                    "_______________________",
                    styles["CellText"]
                )
            ],

            [
                "",
                PDFService._p(
                    PDFService._get_value(
                        doctor,
                        "fullname",
                        ""
                    ),
                    styles["CellBold"]
                )
            ]

        ]

        signature_table = Table(
            signature_data,
            colWidths=[
                95 * mm,
                75 * mm
            ]
        )

        signature_table.setStyle(
            TableStyle([
                (
                    "ALIGN",
                    (1, 0),
                    (1, -1),
                    "CENTER"
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE"
                ),
            ])
        )

        story.append(
            signature_table
        )

        story.append(
            Spacer(1, 10)
        )

        # ==================================================
        # FOOTER NOTE
        # ==================================================

        story.append(
            PDFService._p(
                "SkinAI Clinical - Hệ thống hỗ trợ phân tích "
                "tổn thương da bằng trí tuệ nhân tạo. "
                "Tài liệu này chỉ có giá trị tham khảo và hỗ trợ "
                "chuyên môn, không thay thế kết luận của bác sĩ.",
                styles["Footer"]
            )
        )

        # ==================================================
        # BUILD
        # ==================================================

        doc.build(
            story,
            onFirstPage=PDFService._draw_header_footer,
            onLaterPages=PDFService._draw_header_footer
        )

        # ==================================================
        # RETURN
        # ==================================================

        pdf_buffer.seek(0)

        print(
            "✅ PDF GENERATED:",
            len(pdf_buffer.getvalue()),
            "bytes"
        )

        return pdf_buffer