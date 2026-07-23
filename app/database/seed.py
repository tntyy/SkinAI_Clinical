from werkzeug.security import generate_password_hash

from app.database.db import db
from app.models.user import User
from app.models.disease import Disease

def seed_admin():

    # Username: admin
    # Password: Admin@123
    # Role: admin


    admin = User.query.filter_by(username="admin").first()

    if admin:
        print("✔ Admin already exists.")
        return

    admin = User(
        username="admin",
        password_hash=generate_password_hash("Admin@123"),
        role="admin",
        is_active=True
    )

    db.session.add(admin)
    db.session.commit()

    print("✔ Admin created.")

def seed_diseases():

    if Disease.query.first():
        print("✔ Diseases already exist.")
        return

    diseases = [
        Disease(
            disease_code="mel",
            disease_name="Melanoma",
            disease_name_vi="Ung thư hắc tố",

            category="Ung thư da ác tính",

            overview="""
        Melanoma là loại ung thư da nguy hiểm nhất, phát triển từ các tế bào hắc tố.
        Bệnh có khả năng xâm lấn nhanh và di căn đến các cơ quan khác nếu không được
        phát hiện sớm.
        """,

            symptoms="""
        • Nốt ruồi thay đổi kích thước
        • Màu sắc không đồng đều
        • Bờ không rõ
        • Chảy máu
        • Ngứa
        """,

            causes="""
        Tiếp xúc tia UV kéo dài, di truyền và đột biến tế bào hắc tố.
        """,

            risk_factors="""
        Da trắng
        Tiền sử gia đình
        Nhiều nốt ruồi
        Tiếp xúc ánh nắng nhiều
        """,

            diagnosis="""
        Khám lâm sàng
        Dermoscopy
        Sinh thiết
        """,

            treatment="""
        Phẫu thuật
        Miễn dịch trị liệu
        Liệu pháp nhắm trúng đích
        Hóa trị
        """,

            prevention="""
        Sử dụng kem chống nắng
        Hạn chế tia UV
        Theo dõi nốt ruồi định kỳ
        """,

            follow_up="""
        Tái khám mỗi 3-6 tháng.
        """,

            common_locations="""
        Lưng
        Chân
        Mặt
        Cổ
        """,

            age_group="30-70",

            gender_prevalence="Nam và nữ",

            prevalence="Khoảng 1-2% ung thư da",

            risk_level="High",

            icd10_code="C43",

            reference_image="mel.jpg"
        ),
        Disease(
            disease_code="bcc",
            disease_name="Basal Cell Carcinoma",
            disease_name_vi="Ung thư biểu mô tế bào đáy",

            category="Ung thư da",

            overview="Là loại ung thư da phổ biến nhất và phát triển chậm.",

            symptoms="Vết loét lâu lành, sẩn bóng màu hồng.",

            causes="Tia UV.",

            risk_factors="Người lớn tuổi, da trắng.",

            diagnosis="Khám lâm sàng, sinh thiết.",

            treatment="Phẫu thuật, Mohs, Laser.",

            prevention="Kem chống nắng.",

            follow_up="Khám định kỳ.",

            common_locations="Mặt, cổ.",

            age_group="40+",

            gender_prevalence="Nam",

            prevalence="Chiếm khoảng 70% ung thư da.",

            risk_level="Medium",

            icd10_code="C44",

            reference_image="bcc.jpg"
        ),
        Disease(
            disease_code="bkl",
            disease_name="Benign Keratosis",
            disease_name_vi="Dày sừng lành tính",

            category="Tổn thương da lành tính",

            overview="""
        Benign Keratosis là nhóm tổn thương da lành tính thường gặp ở người trưởng thành
        và người cao tuổi. Bao gồm nhiều dạng như Seborrheic Keratosis, Solar Lentigo
        và Lichen Planus-like Keratosis. Bệnh không phải ung thư và hiếm khi tiến triển
        thành ác tính nhưng đôi khi có hình dạng giống Melanoma nên cần được bác sĩ
        da liễu đánh giá.
        """,

            symptoms="""
        • Mảng da màu nâu hoặc đen
        • Bề mặt sần sùi
        • Có thể hơi gồ lên
        • Không đau
        • Đôi khi ngứa nhẹ
        """,

            causes="""
        Lão hóa da, yếu tố di truyền và tiếp xúc ánh nắng mặt trời lâu dài là những
        nguyên nhân phổ biến.
        """,

            risk_factors="""
        • Người trên 40 tuổi
        • Tiếp xúc nhiều với tia UV
        • Tiền sử gia đình
        """,

            diagnosis="""
        Khám lâm sàng
        Dermoscopy
        Sinh thiết khi nghi ngờ ung thư
        """,

            treatment="""
        Không bắt buộc điều trị nếu không ảnh hưởng thẩm mỹ.
        Có thể:
        • Đốt điện
        • Laser
        • Áp lạnh Nitơ lỏng
        """,

            prevention="""
        Sử dụng kem chống nắng
        Khám da định kỳ
        Hạn chế tiếp xúc tia UV
        """,

            follow_up="""
        Theo dõi mỗi năm hoặc khi tổn thương thay đổi hình dạng.
        """,

            common_locations="""
        Mặt
        Lưng
        Ngực
        Vai
        """,

            age_group="40-80",

            gender_prevalence="Nam và nữ",

            prevalence="Rất phổ biến ở người trung niên và cao tuổi",

            risk_level="Low",

            icd10_code="L82",

            reference_image="bkl.jpg"
        ),
        Disease(
            disease_code="akiec",
            disease_name="Actinic Keratosis",
            disease_name_vi="Dày sừng ánh sáng",

            category="Tiền ung thư",

            overview="""
        Actinic Keratosis là tổn thương tiền ung thư do tiếp xúc tia cực tím kéo dài.
        Nếu không điều trị, một tỷ lệ nhỏ có thể tiến triển thành ung thư biểu mô tế bào
        vảy (Squamous Cell Carcinoma).
        """,

            symptoms="""
        • Da khô ráp
        • Bong vảy
        • Mảng đỏ
        • Cảm giác rát khi chạm
        • Có thể đau nhẹ
        """,

            causes="""
        Tiếp xúc ánh nắng kéo dài trong nhiều năm.
        """,

            risk_factors="""
        • Người lớn tuổi
        • Da trắng
        • Làm việc ngoài trời
        • Tiền sử cháy nắng
        """,

            diagnosis="""
        Khám lâm sàng
        Dermoscopy
        Sinh thiết nếu nghi ngờ
        """,

            treatment="""
        • Áp lạnh
        • Kem 5-Fluorouracil
        • Imiquimod
        • Liệu pháp quang động
        """,

            prevention="""
        Đội mũ
        Mặc áo chống nắng
        Kem chống nắng SPF cao
        """,

            follow_up="""
        Tái khám mỗi 6 tháng.
        """,

            common_locations="""
        Mặt
        Tai
        Da đầu
        Mu bàn tay
        """,

            age_group="50+",

            gender_prevalence="Nam",

            prevalence="Khoảng 10-25% người trên 60 tuổi",

            risk_level="Medium",

            icd10_code="L57.0",

            reference_image="akiec.jpg"
        ),
        Disease(
            disease_code="df",
            disease_name="Dermatofibroma",
            disease_name_vi="U xơ da",

            category="Khối u lành tính",

            overview="""
        Dermatofibroma là khối u xơ lành tính của da, thường xuất hiện sau các chấn
        thương nhỏ như côn trùng cắn hoặc viêm nang lông. Bệnh không nguy hiểm và rất
        hiếm khi chuyển thành ác tính.
        """,

            symptoms="""
        • Nốt cứng nhỏ
        • Màu nâu hoặc đỏ
        • Ấn vào lõm xuống
        • Không đau
        """,

            causes="""
        Có thể liên quan đến phản ứng sau chấn thương nhẹ hoặc côn trùng cắn.
        """,

            risk_factors="""
        • Nữ giới
        • Người trẻ
        • Chấn thương da
        """,

            diagnosis="""
        Khám lâm sàng
        Dermoscopy
        Sinh thiết khi cần
        """,

            treatment="""
        Thông thường không cần điều trị.
        Có thể phẫu thuật nếu gây khó chịu.
        """,

            prevention="""
        Không có biện pháp phòng ngừa đặc hiệu.
        """,

            follow_up="""
        Theo dõi khi kích thước thay đổi.
        """,

            common_locations="""
        Cẳng chân
        Đùi
        Cánh tay
        """,

            age_group="20-50",

            gender_prevalence="Nữ",

            prevalence="Khá phổ biến",

            risk_level="Low",

            icd10_code="D23",

            reference_image="df.jpg"
        ),
        Disease(
            disease_code="nv",
            disease_name="Melanocytic Nevus",
            disease_name_vi="Nốt ruồi sắc tố",

            category="Tổn thương sắc tố lành tính",

            overview="""
        Melanocytic Nevus là nốt ruồi hình thành do sự tăng sinh của tế bào hắc tố.
        Đa số đều lành tính và không cần điều trị, tuy nhiên cần theo dõi nếu có dấu
        hiệu thay đổi theo quy tắc ABCDE.
        """,

            symptoms="""
        • Nốt màu nâu hoặc đen
        • Hình tròn
        • Bờ rõ
        • Kích thước ổn định
        """,

            causes="""
        Do yếu tố di truyền và sự phát triển của tế bào hắc tố.
        """,

            risk_factors="""
        • Di truyền
        • Tiếp xúc tia UV
        """,

            diagnosis="""
        Khám lâm sàng
        Dermoscopy
        Sinh thiết nếu nghi ngờ Melanoma
        """,

            treatment="""
        Không cần điều trị nếu lành tính.
        Có thể cắt bỏ vì lý do thẩm mỹ.
        """,

            prevention="""
        Theo dõi quy tắc ABCDE
        Khám định kỳ
        Kem chống nắng
        """,

            follow_up="""
        Khám mỗi năm.
        """,

            common_locations="""
        Toàn thân
        """,

            age_group="Mọi lứa tuổi",

            gender_prevalence="Nam và nữ",

            prevalence="Rất phổ biến",

            risk_level="Low",

            icd10_code="D22",

            reference_image="nv.jpg"
        ),
        Disease(
            disease_code="vasc",
            disease_name="Vascular Lesion",
            disease_name_vi="Tổn thương mạch máu",

            category="Bệnh lý mạch máu lành tính",

            overview="""
        Vascular Lesion là nhóm tổn thương liên quan đến sự phát triển bất thường của
        mạch máu trong da. Phần lớn là lành tính như Cherry Angioma hoặc Hemangioma và
        ít khi gây nguy hiểm đến sức khỏe.
        """,

            symptoms="""
        • Nốt đỏ
        • Màu tím
        • Có thể chảy máu khi va chạm
        • Không đau
        """,

            causes="""
        Bẩm sinh hoặc do sự tăng sinh mạch máu theo tuổi.
        """,

            risk_factors="""
        • Tuổi cao
        • Yếu tố di truyền
        """,

            diagnosis="""
        Khám lâm sàng
        Dermoscopy
        Siêu âm Doppler nếu cần
        """,

            treatment="""
        • Laser
        • Đốt điện
        • Phẫu thuật trong một số trường hợp
        """,

            prevention="""
        Không có biện pháp phòng ngừa đặc hiệu.
        """,

            follow_up="""
        Theo dõi khi tổn thương tăng kích thước hoặc chảy máu.
        """,

            common_locations="""
        Thân mình
        Mặt
        Chi trên
        """,

            age_group="Mọi lứa tuổi",

            gender_prevalence="Nam và nữ",

            prevalence="Ít gặp hơn các tổn thương sắc tố",

            risk_level="Low",

            icd10_code="D18",

            reference_image="vasc.jpg"
        )
    ]

    db.session.add_all(diseases)

    db.session.commit()

    print("✔ Diseases created.")

def seed_all():

    print("========== SEED ==========")

    seed_admin()

    seed_diseases()

    print("========== DONE ==========")