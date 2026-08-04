"""
seed_diseases.py
Seed dữ liệu cho bảng diseases - 7 lớp bệnh khớp với model AI (HAM10000).
Chạy: python seed_diseases.py

Lưu ý: Đây là thông tin y khoa tổng quát mang tính tham khảo cho bác sĩ,
KHÔNG dùng để tự chẩn đoán, không thay thế ý kiến chuyên môn.
"""

from app import create_app
from app.database.db import db
from app.models.disease import Disease

app = create_app()

DISEASES_DATA = [
    {
        "disease_code": "akiec",
        "disease_name": "Actinic Keratosis / Intraepithelial Carcinoma",
        "disease_name_vi": "Dày sừng quang hóa / Ung thư biểu mô tại chỗ",
        "category": "Tiền ung thư / Ung thư tại chỗ",
        "overview": (
            "Actinic keratosis (AK) là tổn thương tiền ung thư da phổ biến nhất, "
            "hình thành do tổn thương tế bào sừng bởi tia UV tích lũy lâu năm. "
            "Bệnh Bowen (ung thư biểu mô tế bào vảy tại chỗ) là giai đoạn nặng hơn, "
            "khi tế bào bất thường còn giới hạn ở lớp thượng bì, chưa xâm lấn."
        ),
        "symptoms": (
            "Mảng hoặc sẩn nhỏ, thô ráp, có vảy, màu hồng - nâu - đỏ; "
            "bề mặt như giấy nhám khi sờ; có thể ngứa hoặc châm chích nhẹ; "
            "kích thước thường dưới 1cm, có thể tăng dần theo thời gian."
        ),
        "causes": (
            "Tích lũy tổn thương DNA tế bào sừng do tia cực tím (UVB chủ yếu) "
            "trong thời gian dài, dẫn đến tăng sinh tế bào bất thường ở lớp thượng bì."
        ),
        "risk_factors": (
            "Da sáng màu (phototype I-II), tuổi cao, tiền sử phơi nắng nhiều năm, "
            "sống ở vùng nhiều nắng, suy giảm miễn dịch (ghép tạng, HIV), "
            "tiền sử cháy nắng nặng lúc trẻ."
        ),
        "diagnosis": (
            "Khám lâm sàng bằng mắt thường và dermoscopy (soi da); "
            "sinh thiết da nếu nghi ngờ tiến triển thành ung thư biểu mô tế bào vảy xâm lấn."
        ),
        "treatment": (
            "Áp lạnh (cryotherapy) bằng nitơ lỏng cho tổn thương đơn lẻ; "
            "liệu pháp quang động (PDT), thuốc bôi tại chỗ theo chỉ định bác sĩ da liễu "
            "cho tổn thương lan rộng; nạo và đốt điện hoặc cắt bỏ phẫu thuật với bệnh Bowen."
        ),
        "prevention": (
            "Chống nắng hàng ngày (kem chống nắng SPF 30+), tránh nắng giờ cao điểm, "
            "mặc đồ bảo hộ, khám da định kỳ nếu có nhiều tổn thương hoặc tiền sử phơi nắng nhiều."
        ),
        "follow_up": (
            "Tái khám 6-12 tháng để theo dõi tổn thương mới hoặc tiến triển; "
            "cần sinh thiết ngay nếu tổn thương dày lên, chảy máu hoặc loét."
        ),
        "common_locations": "Mặt, tai, da đầu hói, mu bàn tay, cẳng tay - vùng tiếp xúc nắng nhiều",
        "age_group": "Thường gặp trên 40 tuổi, tăng dần theo tuổi",
        "gender_prevalence": "Nam giới gặp nhiều hơn nữ (liên quan phơi nắng nghề nghiệp)",
        "prevalence": "Rất phổ biến, ước tính hàng chục triệu ca trên toàn cầu",
        "risk_level": "medium",
        "icd10_code": "L57.0",
    },
    {
        "disease_code": "bcc",
        "disease_name": "Basal Cell Carcinoma",
        "disease_name_vi": "Ung thư biểu mô tế bào đáy",
        "category": "Ung thư da",
        "overview": (
            "Là loại ung thư da phổ biến nhất, phát triển từ tế bào đáy của thượng bì. "
            "Tiến triển chậm, hiếm khi di căn xa nhưng có thể xâm lấn tại chỗ và phá hủy mô "
            "nếu không điều trị kịp thời."
        ),
        "symptoms": (
            "Sẩn hoặc nốt bóng như hạt ngọc trai, có thể thấy mạch máu giãn trên bề mặt; "
            "vết loét lâu lành, dễ chảy máu; mảng phẳng màu hồng nhạt giống sẹo ở thể nông."
        ),
        "causes": (
            "Đột biến gen liên quan đường tín hiệu Hedgehog do tổn thương tích lũy từ tia UV."
        ),
        "risk_factors": (
            "Da sáng màu, phơi nắng kéo dài, tiền sử cháy nắng, tuổi cao, "
            "tiền sử xạ trị vùng da, hội chứng di truyền (Gorlin syndrome)."
        ),
        "diagnosis": "Khám lâm sàng, soi da (dermoscopy), sinh thiết mô bệnh học để xác định chẩn đoán.",
        "treatment": (
            "Phẫu thuật cắt bỏ là điều trị chính (phẫu thuật Mohs cho vùng mặt/nhạy cảm); "
            "nạo và đốt điện cho tổn thương nhỏ nông; xạ trị cho bệnh nhân không thể phẫu thuật; "
            "thuốc bôi tại chỗ hoặc liệu pháp quang động cho thể nông rất sớm theo chỉ định chuyên khoa."
        ),
        "prevention": "Chống nắng nghiêm ngặt, khám da định kỳ, đặc biệt với người có tiền sử BCC.",
        "follow_up": "Tái khám định kỳ 6-12 tháng do nguy cơ tái phát và xuất hiện tổn thương mới.",
        "common_locations": "Vùng mặt, mũi, tai, cổ - nơi tiếp xúc ánh nắng nhiều nhất",
        "age_group": "Phổ biến trên 50 tuổi, ngày càng ghi nhận ở người trẻ hơn",
        "gender_prevalence": "Nam giới nhỉnh hơn nữ giới",
        "prevalence": "Ung thư da phổ biến nhất, chiếm khoảng 80% các ca ung thư da không melanoma",
        "risk_level": "high",
        "icd10_code": "C44.91",
    },
    {
        "disease_code": "bkl",
        "disease_name": "Benign Keratosis-like Lesions",
        "disease_name_vi": "Tổn thương dạng dày sừng lành tính",
        "category": "Lành tính",
        "overview": (
            "Nhóm tổn thương lành tính bao gồm dày sừng tiết bã (seborrheic keratosis), "
            "đốm lão hóa (solar lentigo) và dày sừng dạng lichen. Rất phổ biến, không nguy hiểm "
            "nhưng đôi khi cần phân biệt với tổn thương ác tính bằng dermoscopy."
        ),
        "symptoms": (
            "Mảng sẫm màu (nâu, đen hoặc be), bề mặt sáp hoặc sần sùi như 'dán lên da'; "
            "ranh giới rõ, không đau, có thể ngứa nhẹ; kích thước tăng chậm theo thời gian."
        ),
        "causes": "Liên quan đến lão hóa da và tích lũy phơi nắng; có yếu tố di truyền.",
        "risk_factors": "Tuổi cao, tiền sử gia đình có tổn thương tương tự, phơi nắng nhiều.",
        "diagnosis": "Khám lâm sàng và dermoscopy thường đủ để chẩn đoán; sinh thiết nếu hình ảnh không điển hình.",
        "treatment": (
            "Thường không cần điều trị nếu không gây khó chịu; áp lạnh, nạo hoặc đốt laser "
            "nếu bệnh nhân có nhu cầu thẩm mỹ hoặc tổn thương gây kích ứng."
        ),
        "prevention": "Không có biện pháp phòng ngừa đặc hiệu; chống nắng giúp giảm tốc độ xuất hiện.",
        "follow_up": "Theo dõi định kỳ nếu tổn thương thay đổi hình dạng, màu sắc hoặc kích thước bất thường.",
        "common_locations": "Thân mình, mặt, cổ - có thể xuất hiện ở bất kỳ vị trí nào",
        "age_group": "Tăng dần từ tuổi 40 trở lên, rất phổ biến ở người cao tuổi",
        "gender_prevalence": "Không có khác biệt rõ rệt giữa nam và nữ",
        "prevalence": "Cực kỳ phổ biến, gần như ai cũng có ít nhất một tổn thương khi lớn tuổi",
        "risk_level": "low",
        "icd10_code": "L82",
    },
    {
        "disease_code": "df",
        "disease_name": "Dermatofibroma",
        "disease_name_vi": "U xơ da (u xơ bì)",
        "category": "Lành tính",
        "overview": (
            "U xơ da là tổn thương lành tính phổ biến của mô liên kết ở trung bì, "
            "thường xuất hiện sau chấn thương nhỏ (côn trùng cắn, cạo lông...). "
            "Không có nguy cơ ác tính hóa."
        ),
        "symptoms": (
            "Nốt cứng chắc, thường màu nâu đỏ hoặc nâu sẫm; dấu hiệu đặc trưng là "
            "'dimple sign' - lõm xuống khi bóp hai bên tổn thương; đường kính thường dưới 1cm."
        ),
        "causes": "Được cho là phản ứng tăng sinh xơ sau chấn thương da nhẹ hoặc côn trùng đốt.",
        "risk_factors": "Thường gặp hơn ở nữ giới; có thể liên quan chấn thương lặp lại (cạo chân).",
        "diagnosis": "Khám lâm sàng với dấu hiệu dimple sign đặc trưng; dermoscopy hỗ trợ; sinh thiết nếu không điển hình.",
        "treatment": "Thường không cần điều trị; cắt bỏ phẫu thuật nếu gây khó chịu, đau hoặc vì lý do thẩm mỹ.",
        "prevention": "Không có biện pháp phòng ngừa đặc hiệu.",
        "follow_up": "Không cần theo dõi đặc biệt trừ khi tổn thương thay đổi bất thường.",
        "common_locations": "Cẳng chân là vị trí phổ biến nhất, cũng gặp ở cánh tay, thân mình",
        "age_group": "Người trưởng thành, phổ biến nhất 20-50 tuổi",
        "gender_prevalence": "Nữ giới gặp nhiều hơn nam giới",
        "prevalence": "Phổ biến, một trong những u da lành tính thường gặp nhất",
        "risk_level": "low",
        "icd10_code": "D23.9",
    },
    {
        "disease_code": "mel",
        "disease_name": "Melanoma",
        "disease_name_vi": "U hắc tố ác tính (Melanoma)",
        "category": "Ung thư da ác tính",
        "overview": (
            "Melanoma là loại ung thư da nguy hiểm nhất, phát sinh từ tế bào hắc tố (melanocyte). "
            "Có khả năng di căn xa nếu không phát hiện và điều trị sớm. Chẩn đoán và can thiệp "
            "kịp thời ở giai đoạn sớm có tiên lượng rất tốt."
        ),
        "symptoms": (
            "Áp dụng quy tắc ABCDE: Asymmetry (bất đối xứng), Border (bờ không đều), "
            "Color (màu sắc không đồng nhất - đen, nâu, đỏ, trắng, xanh), "
            "Diameter (đường kính thường trên 6mm), Evolving (thay đổi theo thời gian - "
            "kích thước, màu sắc, hình dạng, hoặc xuất hiện triệu chứng như ngứa, chảy máu)."
        ),
        "causes": (
            "Đột biến gen ở tế bào hắc tố do tổn thương UV tích lũy hoặc cháy nắng nặng "
            "(đặc biệt ở tuổi nhỏ); một số trường hợp có yếu tố di truyền (đột biến CDKN2A)."
        ),
        "risk_factors": (
            "Da sáng màu, nhiều nốt ruồi hoặc nốt ruồi không điển hình, tiền sử gia đình melanoma, "
            "tiền sử cháy nắng nặng (đặc biệt thời thơ ấu), suy giảm miễn dịch, tiếp xúc UV nhân tạo (giường tắm nắng)."
        ),
        "diagnosis": (
            "Dermoscopy bởi bác sĩ chuyên khoa, sinh thiết cắt trọn tổn thương để xác định "
            "độ dày Breslow - yếu tố tiên lượng quan trọng nhất; có thể cần sinh thiết hạch canh gác "
            "tùy giai đoạn."
        ),
        "treatment": (
            "Phẫu thuật cắt rộng là điều trị chính cho giai đoạn sớm; đối với giai đoạn tiến xa "
            "có thể cần liệu pháp miễn dịch, liệu pháp nhắm trúng đích hoặc hóa trị theo phác đồ "
            "chuyên khoa ung bướu."
        ),
        "prevention": (
            "Chống nắng nghiêm ngặt, tránh giường tắm nắng, tự kiểm tra da định kỳ, "
            "khám chuyên khoa da liễu ngay khi phát hiện nốt ruồi thay đổi bất thường."
        ),
        "follow_up": (
            "Theo dõi sát 3-6 tháng/lần trong những năm đầu sau điều trị, tùy giai đoạn bệnh; "
            "cần tái khám ngay nếu phát hiện tổn thương mới hoặc hạch bất thường."
        ),
        "common_locations": "Thân mình (nam giới), chân (nữ giới); có thể xuất hiện ở bất kỳ vị trí da nào",
        "age_group": "Có thể gặp ở mọi lứa tuổi, tăng nguy cơ theo tuổi",
        "gender_prevalence": "Tỷ lệ khác nhau theo vị trí: nam thân mình, nữ chi dưới",
        "prevalence": "Ít phổ biến hơn BCC/SCC nhưng là nguyên nhân tử vong do ung thư da hàng đầu",
        "risk_level": "critical",
        "icd10_code": "C43.9",
    },
    {
        "disease_code": "nv",
        "disease_name": "Melanocytic Nevus",
        "disease_name_vi": "Nốt ruồi (nốt ruồi sắc tố lành tính)",
        "category": "Lành tính",
        "overview": (
            "Nốt ruồi là tổn thương lành tính cực kỳ phổ biến, hình thành từ sự tập trung "
            "tế bào hắc tố. Đại đa số không nguy hiểm, nhưng cần theo dõi thay đổi bất thường "
            "vì hiếm khi có thể là dấu hiệu sớm của melanoma."
        ),
        "symptoms": (
            "Đốm hoặc sẩn tròn, đối xứng, bờ đều, màu nâu đồng nhất (từ nhạt đến sẫm); "
            "kích thước ổn định theo thời gian, thường dưới 6mm."
        ),
        "causes": "Tăng sinh tế bào hắc tố bẩm sinh hoặc mắc phải, ảnh hưởng bởi gen và phơi nắng.",
        "risk_factors": "Da sáng màu, phơi nắng nhiều, tiền sử gia đình có nhiều nốt ruồi.",
        "diagnosis": "Khám lâm sàng và dermoscopy để phân biệt với tổn thương ác tính (quy tắc ABCDE).",
        "treatment": "Không cần điều trị nếu tổn thương ổn định, đối xứng, đều màu; cắt bỏ nếu nghi ngờ hoặc vì lý do thẩm mỹ.",
        "prevention": "Chống nắng để hạn chế hình thành nốt ruồi mới và giảm nguy cơ biến đổi ác tính.",
        "follow_up": "Tự kiểm tra da định kỳ; khám chuyên khoa nếu nốt ruồi thay đổi kích thước, màu sắc, bờ hoặc gây ngứa/chảy máu.",
        "common_locations": "Có thể xuất hiện ở bất kỳ vị trí nào trên cơ thể",
        "age_group": "Xuất hiện từ nhỏ, tăng số lượng đến tuổi trung niên rồi giảm dần",
        "gender_prevalence": "Không có khác biệt rõ rệt giữa nam và nữ",
        "prevalence": "Cực kỳ phổ biến, người trưởng thành trung bình có 10-40 nốt ruồi",
        "risk_level": "low",
        "icd10_code": "D22",
    },
    {
        "disease_code": "vasc",
        "disease_name": "Vascular Lesions",
        "disease_name_vi": "Tổn thương mạch máu da",
        "category": "Lành tính",
        "overview": (
            "Nhóm tổn thương liên quan đến mạch máu da như u máu anh đào (cherry angioma), "
            "u hạt sinh mủ (pyogenic granuloma), và các dị dạng mạch máu khác. "
            "Phần lớn lành tính, một số có thể chảy máu do va chạm."
        ),
        "symptoms": (
            "Nốt hoặc mảng màu đỏ tươi đến đỏ tía, bờ rõ; có thể phẳng hoặc gồ nhẹ; "
            "u hạt sinh mủ thường phát triển nhanh và dễ chảy máu khi va chạm."
        ),
        "causes": "Tăng sinh mạch máu bất thường; u hạt sinh mủ thường liên quan chấn thương nhỏ hoặc thai kỳ.",
        "risk_factors": "Tuổi tác (u máu anh đào tăng theo tuổi), thai kỳ, một số thuốc, chấn thương da.",
        "diagnosis": "Khám lâm sàng và dermoscopy; sinh thiết nếu tổn thương phát triển nhanh bất thường hoặc không điển hình.",
        "treatment": (
            "Thường không cần điều trị nếu không triệu chứng; đốt điện, laser mạch máu hoặc "
            "cắt bỏ nếu chảy máu tái diễn hoặc vì lý do thẩm mỹ."
        ),
        "prevention": "Không có biện pháp phòng ngừa đặc hiệu với u máu anh đào; tránh chấn thương da lặp lại.",
        "follow_up": "Theo dõi nếu tổn thương phát triển nhanh, loét hoặc chảy máu tái diễn.",
        "common_locations": "Thân mình (u máu anh đào); bất kỳ vị trí nào có chấn thương (u hạt sinh mủ)",
        "age_group": "U máu anh đào tăng dần theo tuổi, thường sau 30 tuổi",
        "gender_prevalence": "Không có khác biệt rõ rệt; u hạt sinh mủ có thể liên quan thai kỳ ở nữ",
        "prevalence": "Phổ biến, đặc biệt u máu anh đào ở người trung niên và cao tuổi",
        "risk_level": "low",
        "icd10_code": "D18.0",
    },
]


def seed_diseases():
    with app.app_context():
        created = 0
        skipped = 0

        for data in DISEASES_DATA:
            existing = Disease.query.filter_by(disease_code=data["disease_code"]).first()

            if existing:
                print(f"⏭  Bỏ qua (đã tồn tại): {data['disease_code']} - {data['disease_name_vi']}")
                skipped += 1
                continue

            disease = Disease(**data)
            db.session.add(disease)
            created += 1
            print(f"✅ Đã thêm: {data['disease_code']} - {data['disease_name_vi']}")

        db.session.commit()

        print("=" * 50)
        print(f"Hoàn tất! Đã thêm {created} bệnh, bỏ qua {skipped} bệnh đã tồn tại.")
        print("=" * 50)


if __name__ == "__main__":
    seed_diseases()