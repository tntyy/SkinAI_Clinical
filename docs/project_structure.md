# Project Structure

## Giới thiệu

Tài liệu này mô tả cấu trúc thư mục của dự án **SkinAI Clinical**, đồng thời giải thích chức năng của từng thành phần trong hệ thống.



---

# Cấu trúc tổng thể

```text
SkinAI_Clinical/
```

Là thư mục gốc chứa toàn bộ mã nguồn của dự án.

---

# app/

Chứa toàn bộ mã nguồn Backend được xây dựng bằng Flask.

Đây là nơi xử lý toàn bộ nghiệp vụ của hệ thống.

---

# app/api/

Chứa các REST API phục vụ:

- Website
- Thiết bị di động
- Hệ thống bệnh viện
- Các dịch vụ bên ngoài

Các API được chia theo từng chức năng:

- auth_api.py
- doctor_api.py
- patient_api.py
- examination_api.py
- ai_api.py
- admin_api.py

---

# app/auth/

Module xác thực người dùng.

Bao gồm:

- Đăng nhập
- Đăng xuất
- Đổi mật khẩu
- Phân quyền

---

# app/doctor/

Module dành riêng cho bác sĩ.

Chức năng:

- Quản lý bệnh nhân
- Chụp ảnh
- Xem kết quả AI
- Viết kết luận
- Quản lý lịch sử khám

---

# app/admin/

Module dành cho quản trị viên.

Chức năng:

- Quản lý tài khoản
- Quản lý bác sĩ
- Thống kê hệ thống
- Audit Log
- Quản lý AI

---

# app/patient/

Quản lý thông tin bệnh nhân.

Bao gồm:

- Thêm
- Sửa
- Xóa
- Tìm kiếm
- Lịch sử bệnh nhân

---

# app/examination/

Quản lý từng lần khám.

Mỗi lần khám bao gồm:

- Thông tin khám
- Hình ảnh
- Metadata
- AI Prediction
- Báo cáo

---

# app/ai/

Module xử lý AI.

Bao gồm:

- Load Model
- Prediction
- Inference
- Lưu kết quả AI

---

# app/preprocessing/

Tiền xử lý ảnh.

Bao gồm:

- Kiểm tra ảnh mờ
- Crop vùng tổn thương
- Chuẩn hóa ảnh
- Chuẩn hóa metadata
- Kiểm tra chất lượng ảnh

---

# app/explain/

Giải thích kết quả AI.

Bao gồm:

- Grad-CAM
- Heatmap

Giúp bác sĩ hiểu AI tập trung vào vùng nào của ảnh.

---

# app/database/

Cấu hình PostgreSQL.

Bao gồm:

- SQLAlchemy
- Flask-Migrate
- Seed dữ liệu

---

# app/models/

Khai báo các Model SQLAlchemy.

Mỗi file tương ứng với một bảng trong PostgreSQL.

Ví dụ:

- users
- patients
- examinations
- ai_predictions
- doctor_reports

---

# app/repositories/

Data Access Layer.

Chỉ thực hiện:

- SELECT
- INSERT
- UPDATE
- DELETE

Không xử lý nghiệp vụ.

---

# app/services/

Business Logic Layer.

Đây là tầng quan trọng nhất.

Ví dụ:

- Kiểm tra dữ liệu
- Chuẩn hóa dữ liệu
- Gọi AI
- Gọi Repository
- Trả kết quả

---

# app/utils/

Các hàm dùng chung.

Ví dụ:

- Validation
- Security
- Response
- Helper

---

# app/templates/

Giao diện HTML.

Được chia theo từng module:

- auth
- doctor
- admin
- patient
- examination
- ai

---

# app/static/

Chứa tài nguyên tĩnh.

Bao gồm:

- CSS
- JavaScript
- Hình ảnh
- Icon
- Upload

Trong uploads gồm:

- original
- crop
- heatmap
- overlay

---

# dataset/

Lưu các bộ dữ liệu phục vụ huấn luyện AI.

Ví dụ:

- HAM10000
- Mobile Dataset
- UPath20

---

# model/

Lưu mô hình AI.

Ví dụ:

- skin_model.keras
- best_model.keras
- TensorFlow Lite

---

# training/

Chứa toàn bộ chương trình huấn luyện AI.

Bao gồm:

- Train Model
- Evaluate
- Export TensorFlow Lite
- Grad-CAM Test

---

# migrations/

Lưu lịch sử thay đổi cơ sở dữ liệu PostgreSQL.

Được Flask-Migrate quản lý.

---

# docs/

Chứa tài liệu của dự án.

Bao gồm:

- API
- Database
- Training
- Deployment
- Architecture
- Project Structure
- Báo cáo

---

# logs/

Lưu nhật ký hoạt động của hệ thống.

Bao gồm:

- system.log
- error.log
- prediction.log
- audit.log

Các file này sẽ được Python tự tạo khi chương trình chạy.

---

# tests/

Chứa Unit Test và Integration Test.

Dùng để kiểm tra toàn bộ hệ thống.

---

# config.py

Chứa toàn bộ cấu hình dự án.

Ví dụ:

- PostgreSQL
- Secret Key
- Upload Folder
- AI Model Path

---

# run.py

Điểm khởi động của hệ thống Flask.

---

# requirements.txt

Danh sách toàn bộ thư viện Python.

Sử dụng:

pip install -r requirements.txt

để cài đặt.

---

# .env

Lưu các thông tin cấu hình bí mật.

Ví dụ:

- Database
- Secret Key

Không đưa file này lên GitHub.

---

# .gitignore

Danh sách các file và thư mục không đưa lên GitHub.

Ví dụ:

- .venv
- __pycache__
- .env
- logs
- uploads

---

# Kiến trúc hoạt động

```
Bác sĩ

↓

Website

↓

REST API

↓

Service Layer

↓

Repository Layer

↓

PostgreSQL

↓

AI Model

↓

Grad-CAM

↓

Kết quả AI

↓

Bác sĩ xác nhận

↓

Lưu lịch sử khám
```

---

# Mục tiêu của cấu trúc

- Dễ bảo trì
- Dễ mở rộng
- Tách biệt từng chức năng
- Dễ triển khai lên Server
- Hỗ trợ Website và Mobile
- Phù hợp với hệ thống AI hỗ trợ chẩn đoán trong lĩnh vực y tế