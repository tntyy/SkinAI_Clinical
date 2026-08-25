# ==========================================================
# ICD-10 MAPPING
# ==========================================================
#
# File này dùng để:
# - Ánh xạ một số mã ICD-10 quan trọng sang tiếng Việt
# - Dịch các thuật ngữ ICD-10 thường gặp
# - Làm dữ liệu fallback khi *_vi trong database đang NULL
#
# Dữ liệu gốc tiếng Anh trong PostgreSQL KHÔNG bị thay đổi.
#
# ==========================================================


# ==========================================================
# 1. ÁNH XẠ CÁC MÃ ICD-10 DA LIỄU THƯỜNG GẶP
# ==========================================================

ICD10_CODE_MAPPING = {

    # ------------------------------------------------------
    # Nhiễm trùng da và mô dưới da
    # ------------------------------------------------------

    "L00": "Hội chứng da phỏng rộp do tụ cầu",
    "L01": "Chốc lở",
    "L02": "Áp xe da, nhọt và nhọt cụm",
    "L03": "Viêm mô tế bào",
    "L04": "Viêm hạch bạch huyết cấp",
    "L05": "Nang lông cùng",
    "L08": "Các nhiễm trùng tại chỗ khác của da và mô dưới da",

    # ------------------------------------------------------
    # Bệnh da do phóng xạ
    # ------------------------------------------------------

    "L55": "Cháy nắng",
    "L56": "Các biến đổi da khác do tia cực tím",
    "L57": "Biến đổi da do phơi nhiễm bức xạ không ion hóa mạn tính",
    "L57.0": "Dày sừng ánh sáng",
    "L57.8": "Các biến đổi da khác do phơi nhiễm bức xạ không ion hóa mạn tính",

    # ------------------------------------------------------
    # Viêm da và chàm
    # ------------------------------------------------------

    "L20": "Viêm da cơ địa",
    "L21": "Viêm da tiết bã",
    "L22": "Viêm da tiết bã ở trẻ sơ sinh",
    "L23": "Viêm da do hăm tã",
    "L24": "Viêm da tiếp xúc kích ứng",
    "L25": "Viêm da tiếp xúc dị ứng",
    "L26": "Viêm da tiếp xúc không xác định",
    "L27": "Viêm da do tiếp xúc với chất khác",
    "L28": "Viêm da và chàm khác",
    "L29": "Viêm da và chàm không xác định",

    # ------------------------------------------------------
    # Bệnh da và mô dưới da do tác nhân bên ngoài
    # ------------------------------------------------------

    "L50": "Bỏng độ I",
    "L51": "Bỏng độ II",
    "L52": "Bỏng độ III",
    "L53": "Bỏng độ IV",
    "L54": "Bỏng do ăn mòn hóa chất",

    # ------------------------------------------------------
    # Bệnh da dạng sẩn
    # ------------------------------------------------------

    "L40": "Vảy nến",
    "L41": "Vảy phấn hồng",
    "L42": "Lichen phẳng",
    "L43": "Các bệnh da dạng sẩn khác",

    # ------------------------------------------------------
    # Mề đay và ban đỏ
    # ------------------------------------------------------

    "L50": "Mề đay",
    "L51": "Mề đay do tác động vật lý",
    "L52": "Mề đay khác",
    "L53": "Mề đay không xác định",

    # ------------------------------------------------------
    # Bệnh da do nấm
    # ------------------------------------------------------

    "B35": "Nhiễm nấm da",
    "B35.0": "Nấm da đầu và râu",
    "B35.1": "Nấm móng",
    "B35.2": "Nấm da bàn tay",
    "B35.3": "Nấm da bàn chân",
    "B35.4": "Nấm da thân",
    "B35.5": "Nấm da vùng bẹn",
    "B35.6": "Nấm da khác",
    "B36": "Nhiễm nấm nông khác",

    # ------------------------------------------------------
    # Bệnh do virus liên quan đến da
    # ------------------------------------------------------

    "B00": "Nhiễm virus herpes",
    "B01": "Thủy đậu",
    "B02": "Zona",
    "B07": "Mụn cóc do virus",
    "B08": "Các nhiễm virus khác đặc trưng bởi tổn thương da và niêm mạc",

    # ------------------------------------------------------
    # Bệnh ký sinh trùng
    # ------------------------------------------------------

    "B86": "Bệnh ghẻ",
    "B87": "Bệnh do ấu trùng ruồi",

    # ------------------------------------------------------
    # Bệnh móng
    # ------------------------------------------------------

    "L60": "Các bệnh về móng",
    "L60.0": "Móng mọc quặp",
    "L60.1": "Tách móng",
    "L60.2": "Hội chứng móng vàng",
    "L60.3": "Loạn dưỡng móng",
    "L60.8": "Các bệnh khác của móng",
    "L60.9": "Bệnh móng không xác định",

    # ------------------------------------------------------
    # Bệnh tóc và nang lông
    # ------------------------------------------------------

    "L63": "Rụng tóc từng vùng",
    "L64": "Rụng tóc do androgen",
    "L65": "Rụng tóc không để lại sẹo khác",
    "L66": "Rụng tóc để lại sẹo",
    "L67": "Các bất thường về màu và thân tóc",
    "L68": "Các bất thường khác của tóc và nang lông",

    # ------------------------------------------------------
    # Bệnh tuyến mồ hôi
    # ------------------------------------------------------

    "L70": "Các bệnh tuyến mồ hôi",

    # ------------------------------------------------------
    # Bệnh da phụ thuộc ánh sáng
    # ------------------------------------------------------

    "L56.0": "Phản ứng da do thuốc gây nhạy cảm với ánh sáng",
    "L56.1": "Viêm da ánh sáng do tiếp xúc",
    "L56.2": "Viêm da ánh sáng do thuốc",

    # ------------------------------------------------------
    # Bệnh da khác
    # ------------------------------------------------------

    "L80": "Bệnh bạch biến",
    "L81": "Các rối loạn sắc tố khác",
    "L82": "Dày sừng da tiết bã",
    "L85": "Các rối loạn biểu bì khác",
    "L87": "Các thay đổi da liên quan đến bệnh mạn tính",
    "L88": "Các bệnh da và mô dưới da khác",
    "L89": "Các bệnh da và mô dưới da khác chưa được phân loại",
    "L90": "Teo da",
    "L91": "Phì đại da",
    "L92": "Rối loạn da do tia phóng xạ",
    "L93": "Loét mạn tính của da",
    "L94": "Loét da do áp lực",
    "L95": "Viêm mạch giới hạn ở da",
    "L97": "Loét chi dưới chưa được phân loại ở nơi khác",
    "L98": "Các rối loạn khác của da và mô dưới da",
    "L99": "Rối loạn da và mô dưới da không xác định",

    # ------------------------------------------------------
    # U hắc tố ác tính của da
    # ------------------------------------------------------

    "C43": "U hắc tố ác tính của da",
    "C43.0": "U hắc tố ác tính của môi",
    "C43.1": "U hắc tố ác tính của mí mắt, kể cả góc mắt",
    "C43.2": "U hắc tố ác tính của tai và ống tai ngoài",
    "C43.3": "U hắc tố ác tính của các phần khác của mặt",
    "C43.4": "U hắc tố ác tính của da đầu và cổ",
    "C43.5": "U hắc tố ác tính của thân mình",
    "C43.6": "U hắc tố ác tính của chi trên",
    "C43.7": "U hắc tố ác tính của chi dưới",
    "C43.8": "U hắc tố ác tính chồng lấp",
    "C43.9": "U hắc tố ác tính của da, không xác định vị trí",

    # ------------------------------------------------------
    # Ung thư da không phải melanoma
    # ------------------------------------------------------

    "C44": "U ác tính khác của da",
    "C44.0": "U ác tính của da môi",
    "C44.1": "U ác tính của da mí mắt",
    "C44.2": "U ác tính của da tai và ống tai ngoài",
    "C44.3": "U ác tính của da các phần khác của mặt",
    "C44.4": "U ác tính của da đầu và cổ",
    "C44.5": "U ác tính của da thân mình",
    "C44.6": "U ác tính của da chi trên",
    "C44.7": "U ác tính của da chi dưới",
    "C44.8": "U ác tính của da tại vị trí chồng lấp",
    "C44.9": "U ác tính của da, không xác định vị trí",
}


# ==========================================================
# 2. ÁNH XẠ CÁC THUẬT NGỮ ICD-10 THƯỜNG GẶP
# ==========================================================

TERM_MAPPING = {

    # ------------------------------------------------------
    # Tổn thương / bệnh
    # ------------------------------------------------------

    "malignant melanoma": "u hắc tố ác tính",
    "melanoma": "u hắc tố",
    "malignant neoplasm": "u ác tính",
    "neoplasm": "tân sinh",
    "carcinoma": "ung thư biểu mô",
    "squamous cell carcinoma": "ung thư biểu mô tế bào vảy",
    "basal cell carcinoma": "ung thư biểu mô tế bào đáy",
    "benign neoplasm": "u lành tính",
    "neoplasm of uncertain behavior": "u có hành vi không xác định",

    # ------------------------------------------------------
    # Da
    # ------------------------------------------------------

    "skin": "da",
    "subcutaneous tissue": "mô dưới da",
    "soft tissue": "mô mềm",
    "cutaneous": "thuộc da",
    "dermatitis": "viêm da",
    "eczema": "chàm",
    "rash": "phát ban",
    "lesion": "tổn thương",

    # ------------------------------------------------------
    # Viêm / nhiễm trùng
    # ------------------------------------------------------

    "inflammation": "viêm",
    "inflammatory": "viêm",
    "infection": "nhiễm trùng",
    "infectious": "do nhiễm trùng",
    "bacterial": "do vi khuẩn",
    "viral": "do virus",
    "fungal": "do nấm",

    # ------------------------------------------------------
    # Da liễu
    # ------------------------------------------------------

    "actinic keratosis": "dày sừng ánh sáng",
    "seborrheic keratosis": "dày sừng tiết bã",
    "psoriasis": "vảy nến",
    "urticaria": "mề đay",
    "vitiligo": "bạch biến",
    "scabies": "ghẻ",
    "alopecia": "rụng tóc",
    "acne": "trứng cá",
    "cellulitis": "viêm mô tế bào",
    "abscess": "áp xe",
    "boil": "nhọt",
    "impetigo": "chốc lở",

    # ------------------------------------------------------
    # Mô tả
    # ------------------------------------------------------

    "unspecified": "không xác định",
    "other": "khác",
    "specified": "được xác định",
    "acute": "cấp tính",
    "chronic": "mạn tính",
    "recurrent": "tái phát",
    "congenital": "bẩm sinh",
    "acquired": "mắc phải",
    "superficial": "nông",
    "deep": "sâu",
    "multiple": "nhiều",
    "single": "đơn độc",
    "localized": "khu trú",
    "generalized": "lan tỏa",

    # ------------------------------------------------------
    # Vị trí cơ thể
    # ------------------------------------------------------

    "lip": "môi",
    "eye": "mắt",
    "eyelid": "mí mắt",
    "ear": "tai",
    "face": "mặt",
    "scalp": "da đầu",
    "neck": "cổ",
    "trunk": "thân mình",
    "chest": "ngực",
    "back": "lưng",
    "abdomen": "bụng",
    "upper limb": "chi trên",
    "lower limb": "chi dưới",
    "arm": "cánh tay",
    "forearm": "cẳng tay",
    "hand": "bàn tay",
    "finger": "ngón tay",
    "leg": "chân",
    "foot": "bàn chân",
    "toe": "ngón chân",
    "nail": "móng",
    "nails": "móng",
    "scalp and neck": "da đầu và cổ",

    # ------------------------------------------------------
    # Các từ khác
    # ------------------------------------------------------

    "due to": "do",
    "with": "kèm",
    "without": "không kèm",
    "associated with": "liên quan đến",
    "involving": "liên quan đến",
    "other specified": "loại khác được xác định",
    "not elsewhere classified": "chưa được phân loại ở nơi khác",
}


# ==========================================================
# 3. HÀM CHUYỂN MÃ ICD-10 SANG TIẾNG VIỆT
# ==========================================================

def translate_code(code, english_text=None):
    """
    Trả về tên tiếng Việt dựa trên mã ICD-10.

    Ưu tiên:
    1. Ánh xạ mã cụ thể (kể cả khi code không có dấu chấm, vd "C4339").
    2. Ánh xạ mã rút gọn dần (C43.39 -> C43.3 -> C43).
    3. Dịch thuật ngữ tiếng Anh.
    4. Nếu không có ánh xạ thì trả None.
    """

    if not code:
        return None

    code = str(code).strip().upper()

    # ------------------------------------------------------
    # Mã đầy đủ, đúng y như trong DB (vd "C4339")
    # ------------------------------------------------------

    if code in ICD10_CODE_MAPPING:
        return ICD10_CODE_MAPPING[code]

    # ------------------------------------------------------
    # Chuẩn hoá về dạng có dấu chấm: "C4339" -> "C43.39"
    # (giữ nguyên nếu code đã có dấu chấm sẵn, vd "C43.39")
    # ------------------------------------------------------

    raw = code.replace(".", "")

    dotted = (
        f"{raw[:3]}.{raw[3:]}"
        if len(raw) > 3
        else raw
    )

    if dotted in ICD10_CODE_MAPPING:
        return ICD10_CODE_MAPPING[dotted]

    # ------------------------------------------------------
    # Rút gọn dần phần thập phân: C43.39 -> C43.3
    # (để bắt các mã con chưa được khai báo riêng)
    # ------------------------------------------------------

    if "." in dotted:

        integer_part, decimal_part = dotted.split(".")

        for i in range(len(decimal_part) - 1, 0, -1):

            candidate = f"{integer_part}.{decimal_part[:i]}"

            if candidate in ICD10_CODE_MAPPING:
                return ICD10_CODE_MAPPING[candidate]

    # ------------------------------------------------------
    # Mã nhóm 3 ký tự (vd "C43")
    # ------------------------------------------------------

    category = raw[:3]

    if category in ICD10_CODE_MAPPING:
        return ICD10_CODE_MAPPING[category]

    # ------------------------------------------------------
    # Thử dịch từ tên tiếng Anh (chỉ khi thật sự không có
    # ánh xạ mã nào khớp)
    # ------------------------------------------------------

    if english_text:
        translated = translate_text(english_text)

        if translated != english_text:
            return translated

    return None


# ==========================================================
# 4. HÀM DỊCH THUẬT NGỮ
# ==========================================================

def translate_text(text):
    """
    Dịch các thuật ngữ ICD-10 phổ biến sang tiếng Việt.

    Đây là lớp fallback.
    Không thay thế bản dịch y khoa chính thức.
    """

    if not text:
        return text

    result = str(text)

    # ------------------------------------------------------
    # Sắp xếp theo độ dài giảm dần
    # để cụm từ dài được thay trước.
    # ------------------------------------------------------

    mappings = sorted(
        TERM_MAPPING.items(),
        key=lambda item: len(item[0]),
        reverse=True
    )

    for english, vietnamese in mappings:

        result = result.replace(
            english,
            vietnamese
        )

        result = result.replace(
            english.title(),
            vietnamese
        )

    return result


# ==========================================================
# 5. HÀM LẤY THÔNG TIN HIỂN THỊ
# ==========================================================

def get_vietnamese_name(
    code,
    short_description_en=None
):
    """
    Lấy tên tiếng Việt để hiển thị.
    """

    translated = translate_code(
        code,
        short_description_en
    )

    if translated:
        return translated

    if short_description_en:
        return translate_text(
            short_description_en
        )

    return "Chưa có bản dịch tiếng Việt"


def get_vietnamese_description(
    code,
    long_description_en=None
):
    """
    Lấy mô tả tiếng Việt để hiển thị.
    """

    if not long_description_en:
        return None

    # Nếu mã có bản dịch cụ thể và mô tả
    # tiếng Anh chỉ giống tên bệnh thì dùng bản dịch mã.
    code_translation = translate_code(code)

    if (
        code_translation
        and long_description_en.strip().lower()
        == code_translation.lower()
    ):
        return code_translation

    return translate_text(
        long_description_en
    )
# ==========================================================
# 6. NHÓM CHƯƠNG ICD-10 (hiển thị badge phân loại)
# ==========================================================

ICD10_CHAPTER_RANGES = [

    ("A00", "B99", "Bệnh nhiễm trùng và ký sinh trùng"),
    ("C00", "D49", "U tân sinh (khối u)"),
    ("D50", "D89", "Bệnh máu và cơ quan tạo máu"),
    ("E00", "E89", "Bệnh nội tiết, dinh dưỡng, chuyển hóa"),
    ("F01", "F99", "Rối loạn tâm thần và hành vi"),
    ("G00", "G99", "Bệnh hệ thần kinh"),
    ("H00", "H59", "Bệnh mắt"),
    ("H60", "H95", "Bệnh tai"),
    ("I00", "I99", "Bệnh hệ tuần hoàn"),
    ("J00", "J99", "Bệnh hệ hô hấp"),
    ("K00", "K95", "Bệnh hệ tiêu hóa"),
    ("L00", "L99", "Da & mô dưới da"),
    ("M00", "M99", "Bệnh cơ xương khớp"),
    ("N00", "N99", "Bệnh hệ tiết niệu - sinh dục"),
    ("R00", "R99", "Triệu chứng và dấu hiệu chưa phân loại"),
    ("S00", "T88", "Chấn thương, ngộ độc"),

]


def get_chapter_name(code):
    """
    Trả về tên nhóm chương ICD-10 dựa trên mã bệnh.
    Ví dụ: L57.0 -> "Da & mô dưới da"
    """

    if not code:
        return None

    code = str(code).strip().upper()

    if not code:
        return None

    letter = code[0]

    try:
        number = int(
            "".join(
                ch for ch in code[1:3]
                if ch.isdigit()
            ) or "0"
        )
    except ValueError:
        number = 0

    for start, end, name in ICD10_CHAPTER_RANGES:

        start_letter = start[0]
        end_letter = end[0]

        start_number = int(start[1:])
        end_number = int(end[1:])

        if start_letter == end_letter:

            if (
                letter == start_letter
                and start_number <= number <= end_number
            ):
                return name

        else:

            if start_letter <= letter <= end_letter:
                return name

    return "Chưa phân loại"
# ==========================================================
# 7. TÌM MÃ ICD-10 THEO TÊN TIẾNG VIỆT (reverse lookup)
# ==========================================================
#
# Dùng khi bác sĩ gõ tiếng Việt để tìm (vd "vảy nến", "u hắc tố")
# nhưng cột *_vi trong DB đang NULL. Ta tra ngược trong
# ICD10_CODE_MAPPING để lấy ra các mã có tên tiếng Việt khớp,
# sau đó dùng các mã này để lọc thêm trong SQL.
# ==========================================================

def search_codes_by_vietnamese_name(keyword):
    """
    Trả về danh sách mã ICD-10 (vd ["L40", "C43"])
    có tên tiếng Việt trong ICD10_CODE_MAPPING chứa `keyword`.
    """

    if not keyword:
        return []

    keyword_lower = keyword.strip().lower()

    if not keyword_lower:
        return []

    matched = [
        code
        for code, name_vi in ICD10_CODE_MAPPING.items()
        if keyword_lower in name_vi.lower()
    ]

    return matched