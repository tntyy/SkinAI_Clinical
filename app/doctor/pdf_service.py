from io import BytesIO
from pathlib import Path
from urllib.parse import urlparse, unquote

from flask import render_template, current_app
from xhtml2pdf import pisa


class PDFService:

    # ==========================================================
    # RESOLVE FILE
    # ==========================================================

    @staticmethod
    def _resolve_file(uri):

        if not uri:
            return None

        uri = str(uri).strip()

        # ------------------------------------------------------
        # HTTP / HTTPS
        # ------------------------------------------------------

        if uri.startswith(("http://", "https://")):
            return uri

        # ------------------------------------------------------
        # FILE URI
        # ------------------------------------------------------

        if uri.startswith("file:///"):

            parsed = urlparse(uri)

            path = unquote(parsed.path)

            # Windows:
            # /C:/Users/... -> C:/Users/...

            if (
                path.startswith("/")
                and len(path) > 2
                and path[2] == ":"
            ):
                path = path[1:]

            file_path = Path(path).resolve()

            if file_path.is_file():
                return str(file_path)

            print("❌ FILE URI NOT FOUND:", file_path)

        # ------------------------------------------------------
        # Chuẩn hóa
        # ------------------------------------------------------

        uri = unquote(uri)

        uri = uri.replace("\\", "/")

        if "?" in uri:
            uri = uri.split("?", 1)[0]

        # ------------------------------------------------------
        # Project
        # ------------------------------------------------------

        root_path = Path(
            current_app.root_path
        ).resolve()

        static_path = Path(
            current_app.static_folder
        ).resolve()

        clean_uri = uri.lstrip("/")

        # ------------------------------------------------------
        # static/...
        # ------------------------------------------------------

        if clean_uri.startswith("static/"):

            clean_uri = clean_uri[
                len("static/"):
            ]

        # ------------------------------------------------------
        # Candidates
        # ------------------------------------------------------

        candidates = [

            static_path / clean_uri,

            root_path / clean_uri,

            root_path / "static" / clean_uri,

            static_path / "uploads" / Path(clean_uri).name,

            root_path / "uploads" / Path(clean_uri).name,

        ]

        # ------------------------------------------------------
        # Find
        # ------------------------------------------------------

        for candidate in candidates:

            candidate = candidate.resolve()

            if candidate.is_file():

                print(
                    "✅ PDF FILE:",
                    candidate
                )

                return str(candidate)

        print(
            "❌ PDF FILE NOT FOUND:",
            uri
        )

        return None

    # ==========================================================
    # LINK CALLBACK
    # ==========================================================

    @staticmethod
    def link_callback(uri, rel):

        print("-----------------------------------")
        print("PDF URI:", uri)
        print("PDF REL:", rel)

        result = PDFService._resolve_file(uri)

        print("RESOLVED:", result)
        print("-----------------------------------")

        if result:
            return result

        return uri

    # ==========================================================
    # GENERATE PDF
    # ==========================================================

    @staticmethod
    def generate_pdf(context):

        # ======================================================
        # FONT
        # ======================================================

        fonts_dir = (
            Path(current_app.root_path)
            / "static"
            / "fonts"
        ).resolve()

        normal_font = (
            fonts_dir / "DejaVuSans.ttf"
        ).resolve()

        bold_font = (
            fonts_dir / "DejaVuSans-Bold.ttf"
        ).resolve()

        # ======================================================
        # CHECK FONT
        # ======================================================

        print("===================================")
        print("PDF FONT CHECK")
        print("Fonts dir :", fonts_dir)
        print("Normal    :", normal_font)
        print("Bold      :", bold_font)
        print("Normal OK :", normal_font.is_file())
        print("Bold OK   :", bold_font.is_file())
        print("===================================")

        if not normal_font.is_file():

            raise FileNotFoundError(
                f"Không tìm thấy font:\n{normal_font}"
            )

        if not bold_font.is_file():

            raise FileNotFoundError(
                f"Không tìm thấy font:\n{bold_font}"
            )

        # ======================================================
        # COPY CONTEXT
        # ======================================================

        pdf_context = dict(context)

        # ======================================================
        # LESION IMAGE
        # ======================================================

        lesion_image = pdf_context.get(
            "lesion_image"
        )

        if lesion_image:

            lesion_image = PDFService._resolve_file(
                lesion_image
            )

        pdf_context["lesion_image"] = lesion_image

        # ======================================================
        # HEATMAP
        # ======================================================

        heatmap_image = None
        overlay_image = None

        heatmap = pdf_context.get("heatmap")

        if heatmap:

            if heatmap.heatmap_path:

                heatmap_image = (
                    PDFService._resolve_file(
                        heatmap.heatmap_path
                    )
                )

            if heatmap.overlay_path:

                overlay_image = (
                    PDFService._resolve_file(
                        heatmap.overlay_path
                    )
                )

        pdf_context["heatmap_image"] = heatmap_image
        pdf_context["overlay_image"] = overlay_image

        # ======================================================
        # LOGO
        # ======================================================

        logo = pdf_context.get("logo")

        if logo:

            logo = PDFService._resolve_file(
                logo
            )

        pdf_context["logo"] = logo

        # ======================================================
        # FONT PATH
        # ======================================================

        # Quan trọng:
        # Dùng file:/// thay vì fonts/...
        #
        # Path.as_uri() sẽ tạo:
        #
        # file:///C:/Users/admin/.../DejaVuSans.ttf

        pdf_context["font_path"] = (
            normal_font.as_uri()
        )

        pdf_context["bold_font_path"] = (
            bold_font.as_uri()
        )

        print("FONT URI NORMAL:")
        print(pdf_context["font_path"])

        print("FONT URI BOLD:")
        print(pdf_context["bold_font_path"])

        # ======================================================
        # RENDER HTML
        # ======================================================

        html = render_template(
            "doctor/pdf.html",
            **pdf_context
        )

        # ======================================================
        # CREATE PDF
        # ======================================================

        pdf = BytesIO()

        pisa_status = pisa.CreatePDF(

            html,

            dest=pdf,

            encoding="UTF-8",

            link_callback=PDFService.link_callback

        )

        # ======================================================
        # ERROR
        # ======================================================

        if pisa_status.err:

            raise Exception(
                "Không thể tạo PDF."
            )

        pdf.seek(0)

        return pdf