"""
seed_sample_data.py
Seed dữ liệu mẫu cho toàn bộ luồng nghiệp vụ:
users/doctor_profiles -> patients -> examinations -> lesion_images
-> image_metadata -> ai_predictions -> ai_prediction_details -> ai_heatmaps
-> doctor_reports -> consent_records -> audit_logs

Chạy: python seed_sample_data.py

⚠️ ĐIỀU CHỈNH TRƯỚC KHI CHẠY:
- Kiểm tra lại đường dẫn import từng model bên dưới cho khớp với project thật.
- Kiểm tra tên field (vd: fullname/full_name, patient_code/code...) khớp với model thật.
- image_path/heatmap_path ở đây là đường dẫn GIẢ ĐỊNH (chưa có file thật),
  chỉ dùng để test giao diện/API, KHÔNG dùng để test model AI thật.
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import random
from datetime import datetime, timedelta

from werkzeug.security import generate_password_hash

from app import create_app
from app.database.db import db
from app.models.user import User
from app.models.doctor_profile import DoctorProfile
from app.models.patient import Patient
from app.models.examination import Examination
from app.models.lesion_image import LesionImage
from app.models.image_metadata import ImageMetadata
from app.models.ai_prediction import AIPrediction
from app.models.ai_prediction_detail import AIPredictionDetail
from app.models.ai_heatmap import AIHeatmap
from app.models.doctor_report import DoctorReport
from app.models.consent_record import ConsentRecord
from app.models.audit_log import AuditLog

app = create_app()
random.seed(42)

# ============================================
# DỮ LIỆU MẪU DÙNG CHUNG
# ============================================
PATIENT_NAMES = [
    "Nguyễn Văn An", "Trần Thị Bích", "Lê Hoàng Cường", "Phạm Thị Dung",
    "Hoàng Văn Em", "Vũ Thị Phương", "Đặng Văn Giang", "Bùi Thị Hoa",
    "Ngô Văn Inh", "Đỗ Thị Kim"
]

CHIEF_COMPLAINTS = [
    "Nổi mụn nước ngứa vùng cẳng tay",
    "Xuất hiện nốt ruồi thay đổi màu sắc",
    "Mảng da khô, bong vảy vùng mặt",
    "Nốt sần cứng vùng cẳng chân, không đau",
    "Theo dõi tổn thương da định kỳ",
    "Vết loét nhỏ lâu lành vùng mũi",
    "Đốm đỏ dễ chảy máu khi va chạm",
    "Mảng sắc tố sẫm màu vùng lưng"
]

# Khớp với disease_code đã seed ở bảng diseases
DISEASE_CODES = ["akiec", "bcc", "bkl", "df", "mel", "nv", "vasc"]

DEVICES = ["iPhone 13 Pro - Camera cận cảnh", "Dermoscope DermLite DL4",
           "Samsung Galaxy S22 - Macro mode", "Canon EOS + Macro lens"]

LESION_LOCATIONS = ["Mặt", "Cổ", "Lưng", "Ngực", "Cẳng tay", "Cẳng chân",
                    "Bàn tay", "Bàn chân", "Da đầu"]

SKIN_TYPES = ["I - Rất sáng", "II - Sáng", "III - Trung bình", "IV - Ngăm"]


def get_or_create_doctors():
    """Lấy doctor có sẵn (từ seed_admin) và tạo thêm 1 doctor nữa để dữ liệu đa dạng."""
    doctors_users = []

    doctor1 = User.query.filter_by(username="doctor").first()
    if not doctor1:
        raise Exception("Chưa có tài khoản 'doctor'. Hãy chạy script tạo doctor trước.")
    doctors_users.append(doctor1)

    doctor2 = User.query.filter_by(username="doctor2").first()
    if not doctor2:
        doctor2 = User(
            username="doctor2",
            password_hash=generate_password_hash("Doctor@123"),
            role="doctor",
            is_active=True
        )
        db.session.add(doctor2)
        db.session.commit()
        print("✅ Đã tạo thêm tài khoản doctor2")
    doctors_users.append(doctor2)

    doctor_profiles = []
    profile_data = [
        {"user": doctor1, "fullname": "BS. Nguyễn Minh Tuấn",
         "email": "tuan.nguyen@hospital.vn", "phone": "0901234567",
         "hospital": "Bệnh viện Da liễu TP.HCM", "department": "Khoa Da liễu"},
        {"user": doctor2, "fullname": "BS. Trần Thị Ngọc Anh",
         "email": "anh.tran@hospital.vn", "phone": "0912345678",
         "hospital": "Bệnh viện Da liễu Trung ương", "department": "Khoa Ung bướu da"},
    ]

    for data in profile_data:
        existing = DoctorProfile.query.filter_by(user_id=data["user"].user_id).first()
        if existing:
            doctor_profiles.append(existing)
            continue

        profile = DoctorProfile(
            user_id=data["user"].user_id,
            fullname=data["fullname"],
            email=data["email"],
            phone=data["phone"],
            hospital=data["hospital"],
            department=data["department"],
            avatar_path=None
        )
        db.session.add(profile)
        doctor_profiles.append(profile)

    db.session.commit()
    print(f"✅ Đã có {len(doctor_profiles)} hồ sơ bác sĩ")
    return doctor_profiles


def seed_patients(doctor_profiles):
    patients = []
    for i, name in enumerate(PATIENT_NAMES):
        code = f"BN{2025}{str(i + 1).zfill(4)}"

        existing = Patient.query.filter_by(patient_code=code).first()
        if existing:
            patients.append(existing)
            continue

        patient = Patient(
            patient_code=code,
            created_by_doctor=random.choice(doctor_profiles).doctor_id,
            fullname=name,
            gender=random.choice(["male", "female"]),
            birth_year=random.randint(1955, 2005),
            phone=f"09{random.randint(10000000, 99999999)}"
        )
        db.session.add(patient)
        patients.append(patient)

    db.session.commit()
    print(f"✅ Đã có {len(patients)} bệnh nhân")
    return patients


def seed_examinations(patients, doctor_profiles):
    examinations = []

    for patient in patients:
        num_exams = random.randint(1, 2)  # mỗi bệnh nhân 1-2 lần khám

        for _ in range(num_exams):
            exam_date = datetime.now() - timedelta(days=random.randint(1, 180))

            exam = Examination(
                patient_id=patient.patient_id,
                doctor_id=random.choice(doctor_profiles).doctor_id,
                exam_date=exam_date,
                chief_complaint=random.choice(CHIEF_COMPLAINTS),
                note="Bệnh nhân tỉnh táo, hợp tác khám. Không có tiền sử dị ứng đặc biệt."
            )
            db.session.add(exam)
            examinations.append(exam)

    db.session.commit()
    print(f"✅ Đã có {len(examinations)} lượt khám")
    return examinations


def seed_images_and_metadata(examinations):
    images = []

    for exam in examinations:
        num_images = random.randint(1, 2)  # mỗi ca khám 1-2 ảnh

        for j in range(num_images):
            image_path = f"uploads/lesion_images/exam_{exam.exam_id}_img_{j + 1}.jpg"
            crop_path = f"uploads/lesion_images/cropped/exam_{exam.exam_id}_img_{j + 1}_crop.jpg"

            image = LesionImage(
                exam_id=exam.exam_id,
                image_path=image_path,
                crop_path=crop_path,
                blur_score=round(random.uniform(0.05, 0.35), 2),  # thấp = ít mờ
                quality_score=round(random.uniform(0.65, 0.98), 2),
                is_valid=True,
                captured_at=exam.exam_date
            )
            db.session.add(image)
            db.session.flush()  # để lấy image_id ngay mà không cần commit

            metadata = ImageMetadata(
                image_id=image.image_id,
                age=2025 - random.randint(1955, 2005),
                gender=random.choice(["male", "female"]),
                lesion_location=random.choice(LESION_LOCATIONS),
                skin_type=random.choice(SKIN_TYPES),
                device=random.choice(DEVICES),
                note="Ảnh chụp dưới ánh sáng tự nhiên, khoảng cách ~15cm"
            )
            db.session.add(metadata)

            images.append(image)

    db.session.commit()
    print(f"✅ Đã có {len(images)} ảnh tổn thương + metadata")
    return images


def seed_ai_predictions(images):
    predictions = []

    for image in images:
        prediction = AIPrediction(
            image_id=image.image_id,
            model_name="ResNet50",
            model_version="v1.0-finetuned",
            created_at=image.captured_at + timedelta(minutes=random.randint(1, 10))
        )
        db.session.add(prediction)
        db.session.flush()

        # Sinh Top-3 confidence hợp lý: giảm dần và tổng gần 1.0
        top1 = round(random.uniform(0.55, 0.92), 4)
        remaining = 1 - top1
        top2 = round(remaining * random.uniform(0.5, 0.8), 4)
        top3 = round(remaining - top2, 4)

        chosen_classes = random.sample(DISEASE_CODES, 3)
        confidences = sorted([top1, top2, top3], reverse=True)

        for rank, (cls, conf) in enumerate(zip(chosen_classes, confidences), start=1):
            detail = AIPredictionDetail(
                prediction_id=prediction.prediction_id,
                rank=rank,
                predicted_class=cls,
                confidence=conf
            )
            db.session.add(detail)

        heatmap = AIHeatmap(
            prediction_id=prediction.prediction_id,
            heatmap_path=f"uploads/heatmaps/prediction_{prediction.prediction_id}_gradcam.jpg",
            method="GradCAM"
        )
        db.session.add(heatmap)

        predictions.append(prediction)

    db.session.commit()
    print(f"✅ Đã có {len(predictions)} lượt AI dự đoán (kèm Top-3 + heatmap)")
    return predictions


def seed_doctor_reports(examinations, doctor_profiles):
    reports = []

    diagnosis_options = [
        "Nốt ruồi lành tính (Melanocytic nevus), theo dõi định kỳ 12 tháng",
        "Dày sừng tiết bã lành tính, không cần can thiệp",
        "Nghi ngờ ung thư biểu mô tế bào đáy, chỉ định sinh thiết xác định",
        "U xơ da lành tính, tư vấn theo dõi",
        "Dày sừng quang hóa, chỉ định áp lạnh nitơ lỏng",
    ]

    # Chỉ khoảng 70% ca khám đã có kết luận (số còn lại đang chờ bác sĩ xác nhận)
    for exam in examinations:
        if random.random() > 0.3:
            report = DoctorReport(
                exam_id=exam.exam_id,
                doctor_id=exam.doctor_id,
                diagnosis=random.choice(diagnosis_options),
                treatment="Theo dõi định kỳ, tái khám nếu có thay đổi bất thường (kích thước, màu sắc, chảy máu).",
                note="Đã tư vấn bệnh nhân về dấu hiệu cảnh báo cần tái khám sớm.",
                status="confirmed",
                confirmed_at=exam.exam_date + timedelta(hours=1)
            )
            db.session.add(report)
            reports.append(report)

    db.session.commit()
    print(f"✅ Đã có {len(reports)} kết luận của bác sĩ")
    return reports


def seed_consent_records(examinations, doctor_profiles):
    count = 0
    for exam in examinations:
        consent = ConsentRecord(
            exam_id=exam.exam_id,
            purpose=random.choice(["diagnosis", "ai_training"]),
            granted_by=exam.doctor_id,
            granted_at=exam.exam_date
        )
        db.session.add(consent)
        count += 1

    db.session.commit()
    print(f"✅ Đã có {count} bản ghi đồng ý sử dụng dữ liệu")


def seed_audit_logs(doctor_profiles):
    admin = User.query.filter_by(role="admin").first()
    doctor_users = User.query.filter_by(role="doctor").all()

    actions = ["view", "create", "update"]
    tables = ["patients", "examinations", "lesion_images", "doctor_reports"]

    count = 0
    all_users = ([admin] if admin else []) + doctor_users

    for user in all_users:
        for _ in range(random.randint(3, 8)):
            log = AuditLog(
                user_id=user.user_id,
                action=random.choice(actions),
                target_table=random.choice(tables),
                target_id=random.randint(1, 20),
                ip_address=f"192.168.1.{random.randint(2, 254)}",
                created_at=datetime.now() - timedelta(days=random.randint(0, 30))
            )
            db.session.add(log)
            count += 1

    db.session.commit()
    print(f"✅ Đã có {count} bản ghi audit log")


def main():
    with app.app_context():
        print("=" * 60)
        print("BẮT ĐẦU SEED DỮ LIỆU MẪU")
        print("=" * 60)

        doctor_profiles = get_or_create_doctors()
        patients = seed_patients(doctor_profiles)
        examinations = seed_examinations(patients, doctor_profiles)
        images = seed_images_and_metadata(examinations)
        seed_ai_predictions(images)
        seed_doctor_reports(examinations, doctor_profiles)
        seed_consent_records(examinations, doctor_profiles)
        seed_audit_logs(doctor_profiles)

        print("=" * 60)
        print("✅ HOÀN TẤT SEED DỮ LIỆU MẪU!")
        print("=" * 60)
        print(f"Bác sĩ       : {len(doctor_profiles)}")
        print(f"Bệnh nhân    : {len(patients)}")
        print(f"Lượt khám    : {len(examinations)}")
        print(f"Ảnh tổn thương: {len(images)}")


if __name__ == "__main__":
    main()