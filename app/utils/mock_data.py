"""
Dữ liệu mẫu (mock) để dựng giao diện khi CSDL Postgres chưa được cấu hình/kết nối.
Cấu trúc field đặt trùng tên với các model thật (app/models/*) để sau này
thay bằng truy vấn thật (qua repositories/services) chỉ cần đổi nguồn dữ liệu,
không cần sửa template.

TODO: Xoá module này khi đã nối repositories/services thật với DB.
"""

from datetime import datetime, timedelta

MOCK_DOCTOR = {
    "doctor_id": 1,
    "fullname": "Nguyễn Văn A",
    "hospital": "Bệnh viện Da liễu TP.HCM",
    "department": "Khoa Da liễu",
}

MOCK_PATIENTS = [
    {
        "patient_id": 1,
        "patient_code": "BN-0001",
        "fullname": "Trần Thị Hoa",
        "gender": "Nữ",
        "birth_year": 1990,
        "phone": "0901234567",
        "created_at": datetime.now() - timedelta(days=40),
        "exam_count": 3,
        "last_exam_date": datetime.now() - timedelta(days=2),
    },
    {
        "patient_id": 2,
        "patient_code": "BN-0002",
        "fullname": "Lê Văn Bình",
        "gender": "Nam",
        "birth_year": 1985,
        "phone": "0912345678",
        "created_at": datetime.now() - timedelta(days=25),
        "exam_count": 1,
        "last_exam_date": datetime.now() - timedelta(days=10),
    },
    {
        "patient_id": 3,
        "patient_code": "BN-0003",
        "fullname": "Phạm Thị Cúc",
        "gender": "Nữ",
        "birth_year": 2001,
        "phone": "0987654321",
        "created_at": datetime.now() - timedelta(days=5),
        "exam_count": 0,
        "last_exam_date": None,
    },
]

MOCK_EXAMINATIONS = [
    {
        "exam_id": 101,
        "patient_id": 1,
        "exam_date": datetime.now() - timedelta(days=2),
        "chief_complaint": "Nốt ruồi vùng lưng thay đổi màu sắc",
        "status": "confirmed",
    },
    {
        "exam_id": 102,
        "patient_id": 1,
        "exam_date": datetime.now() - timedelta(days=20),
        "chief_complaint": "Ngứa, đỏ da vùng cánh tay",
        "status": "confirmed",
    },
    {
        "exam_id": 103,
        "patient_id": 2,
        "exam_date": datetime.now() - timedelta(days=10),
        "chief_complaint": "Mụn viêm vùng mặt",
        "status": "pending",
    },
]

MOCK_AI_RESULT = [
    {"label": "Nốt ruồi lành tính (Nevus)", "prob": 0.78},
    {"label": "Dày sừng tiết bã (Seborrheic keratosis)", "prob": 0.12},
    {"label": "Ung thư hắc tố (Melanoma)", "prob": 0.06},
    {"label": "Khác", "prob": 0.04},
]


def get_patient_by_id(patient_id):
    return next((p for p in MOCK_PATIENTS if p["patient_id"] == patient_id), None)


def get_examinations_by_patient(patient_id):
    return [e for e in MOCK_EXAMINATIONS if e["patient_id"] == patient_id]


def get_examination_by_id(exam_id):
    return next((e for e in MOCK_EXAMINATIONS if e["exam_id"] == exam_id), None)