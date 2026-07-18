# Database Design

## Giới thiệu

Hệ thống sử dụng PostgreSQL để lưu trữ dữ liệu.

Mô hình thiết kế theo chuẩn quan hệ (Relational Database).

---

## Nhóm bảng

### Người dùng

- users
- doctor_profiles

---

### Bệnh nhân

- patients
- examinations

---

### Hình ảnh

- lesion_images
- image_metadata

---

### AI

- ai_predictions
- ai_prediction_details
- ai_heatmaps

---

### Báo cáo

- doctor_reports
- report_prediction_refs

---

### Bảo mật

- consent_records
- audit_logs

---

## Quan hệ

Doctor

↓

Patient

↓

Examination

↓

Lesion Image

↓

AI Prediction

↓

Doctor Report