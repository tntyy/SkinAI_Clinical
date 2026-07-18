# API Documentation

## Giới thiệu

API (Application Programming Interface) là cầu nối giữa giao diện người dùng (Website, Mobile) với hệ thống Backend.

Trong dự án SkinAI Clinical, tất cả chức năng như đăng nhập, quản lý bệnh nhân, AI dự đoán, lịch sử khám,... đều thông qua REST API.

---

## Kiến trúc

Web / Mobile

↓

REST API

↓

Business Logic (Service)

↓

Database (PostgreSQL)

↓

AI Model

---

## Nhóm API

### Authentication

- POST /api/login
- POST /api/logout
- POST /api/change-password

---

### Patient

- GET /api/patients
- GET /api/patient/{id}
- POST /api/patient
- PUT /api/patient/{id}
- DELETE /api/patient/{id}

---

### Examination

- POST /api/examination
- GET /api/examination/{id}
- GET /api/history/{patient_id}

---

### AI

- POST /api/predict
- GET /api/prediction/{id}
- GET /api/heatmap/{id}

---

### Doctor

- POST /api/report
- GET /api/report/{id}

---

### Admin

- GET /api/dashboard
- GET /api/statistics
- GET /api/audit

---

## Định dạng dữ liệu

Request và Response sử dụng JSON.

Ví dụ:

{
    "patient_id":15,
    "gender":"male",
    "age":42
}