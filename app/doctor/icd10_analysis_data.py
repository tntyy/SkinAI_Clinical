# ==========================================================
# ICD-10 ANALYSIS DATA (dữ liệu tĩnh, không gọi AI)
# ==========================================================
#
# Dùng để hiển thị phần "Phân tích bệnh" khi bác sĩ bấm nút
# trên trang tra cứu ICD-10, thay cho việc gọi Grok API.
#
# Cấu trúc mỗi entry PHẢI khớp với những gì icd10.js đang
# render (causes, risk_factors, symptoms, complications,
# treatment.medication/procedure/lifestyle, prognosis,
# follow_up, emergency_warning).
#
# ⚠️ Đây là thông tin tham khảo tổng quát, không thay thế
# đánh giá lâm sàng và quyết định chuyên môn của bác sĩ.
# ==========================================================


ICD10_ANALYSIS_DATA = {

    # ------------------------------------------------------
    # C43 - U hắc tố ác tính của da (Melanoma)
    # ------------------------------------------------------
    "C43": {
        "causes": [
            "Đột biến tế bào hắc tố (melanocyte) do tổn thương DNA tích lũy",
            "Tiếp xúc tia UV (ánh nắng, giường tắm nắng) là yếu tố khởi phát chính",
            "Đột biến gen BRAF, NRAS, hoặc hội chứng u hắc tố gia đình (CDKN2A)"
        ],
        "risk_factors": [
            "Da trắng, dễ bắt nắng, nhiều nốt ruồi (>50 nốt) hoặc nốt ruồi loạn sản",
            "Tiền sử cháy nắng nặng, đặc biệt ở tuổi nhỏ",
            "Tiền sử gia đình có người bị melanoma",
            "Suy giảm miễn dịch (ghép tạng, HIV)"
        ],
        "symptoms": [
            "Tổn thương sắc tố thay đổi theo quy tắc ABCDE: bất đối xứng, bờ không đều, màu không đồng nhất, đường kính >6mm, thay đổi theo thời gian",
            "Nốt ruồi cũ to nhanh, đổi màu, ngứa hoặc chảy máu",
            "Xuất hiện tổn thương sắc tố mới ở người lớn tuổi"
        ],
        "complications": [
            "Di căn hạch bạch huyết vùng",
            "Di căn xa (phổi, gan, não, xương) ở giai đoạn muộn",
            "Loét, chảy máu tại chỗ tổn thương"
        ],
        "treatment": {
            "medication": [
                "Liệu pháp miễn dịch (ức chế điểm kiểm soát: anti-PD-1, anti-CTLA-4) cho giai đoạn di căn",
                "Liệu pháp nhắm trúng đích (BRAF/MEK inhibitor) nếu có đột biến BRAF"
            ],
            "procedure": [
                "Phẫu thuật cắt rộng tổn thương nguyên phát kèm bờ an toàn theo độ dày Breslow",
                "Sinh thiết hạch cửa (sentinel lymph node) khi có chỉ định",
                "Xạ trị hỗ trợ trong một số trường hợp"
            ],
            "lifestyle": [
                "Tránh nắng gắt, dùng kem chống nắng phổ rộng SPF ≥30",
                "Tự kiểm tra da định kỳ, chụp ảnh theo dõi nốt ruồi nghi ngờ"
            ]
        },
        "prognosis": (
            "Tiên lượng phụ thuộc chủ yếu vào độ dày Breslow và giai đoạn tại "
            "thời điểm chẩn đoán. Phát hiện sớm (giai đoạn tại chỗ) có tỷ lệ "
            "sống 5 năm rất cao; giai đoạn di căn xa tiên lượng dè dặt hơn nhiều."
        ),
        "follow_up": [
            "Khám da toàn thân định kỳ mỗi 3-6 tháng trong 2 năm đầu sau điều trị",
            "Siêu âm hạch vùng, xét nghiệm hình ảnh theo giai đoạn bệnh",
            "Tái khám ngay nếu xuất hiện tổn thương sắc tố mới"
        ],
        "emergency_warning": [
            "Tổn thương chảy máu không cầm, loét lan nhanh",
            "Nổi hạch cứng, to nhanh vùng dẫn lưu",
            "Triệu chứng gợi ý di căn: đau đầu dai dẳng, khó thở, đau xương bất thường"
        ]
    },

    # ------------------------------------------------------
    # C44 - Ung thư da không phải melanoma (BCC/SCC)
    # ------------------------------------------------------
    "C44": {
        "causes": [
            "Tích lũy tổn thương DNA do tia UV lâu dài",
            "Đột biến gen ức chế khối u (TP53, PTCH1) ở tế bào đáy hoặc tế bào vảy"
        ],
        "risk_factors": [
            "Tiếp xúc nắng nghề nghiệp/kéo dài, da trắng",
            "Tiền sử tổn thương da mạn tính, sẹo bỏng, loét lâu lành",
            "Ức chế miễn dịch, tiền sử xạ trị vùng da đó"
        ],
        "symptoms": [
            "Ung thư biểu mô tế bào đáy: nốt sẩn bóng, có mạch máu giãn, hay loét ở giữa, chảy máu tái phát",
            "Ung thư biểu mô tế bào vảy: mảng sừng hóa, loét, dễ chảy máu, phát triển nhanh hơn BCC"
        ],
        "complications": [
            "Xâm lấn tại chỗ gây phá hủy mô lân cận (đặc biệt vùng mặt)",
            "SCC có thể di căn hạch nếu không điều trị kịp thời"
        ],
        "treatment": {
            "medication": [
                "Thuốc bôi tại chỗ (5-FU, imiquimod) cho tổn thương nông, giai đoạn sớm",
                "Liệu pháp toàn thân (ức chế Hedgehog, miễn dịch) cho trường hợp tiến triển"
            ],
            "procedure": [
                "Phẫu thuật cắt bỏ tổn thương (Mohs surgery cho vùng mặt, thẩm mỹ)",
                "Áp lạnh, đốt điện hoặc xạ trị với tổn thương nhỏ, vị trí khó phẫu thuật"
            ],
            "lifestyle": [
                "Chống nắng nghiêm ngặt, tránh nắng giờ cao điểm",
                "Tự theo dõi các tổn thương da lâu lành để tái khám sớm"
            ]
        },
        "prognosis": (
            "Tiên lượng tốt nếu phát hiện và điều trị sớm, tỷ lệ khỏi cao "
            "với BCC. SCC có nguy cơ tái phát/di căn cao hơn nếu tổn thương "
            "lớn, xâm lấn sâu hoặc ở người suy giảm miễn dịch."
        ),
        "follow_up": [
            "Khám da định kỳ 6-12 tháng để phát hiện tổn thương mới hoặc tái phát",
            "Theo dõi vết mổ, đánh giá thẩm mỹ và chức năng sau phẫu thuật"
        ],
        "emergency_warning": [
            "Chảy máu tại chỗ không kiểm soát",
            "Tổn thương lan nhanh, xâm lấn cấu trúc lân cận (mắt, mũi)"
        ]
    },

    # ------------------------------------------------------
    # L40 - Vảy nến
    # ------------------------------------------------------
    "L40": {
        "causes": [
            "Rối loạn miễn dịch qua trung gian tế bào T gây tăng sinh biểu bì bất thường",
            "Yếu tố di truyền kết hợp yếu tố khởi phát (stress, nhiễm trùng, thuốc)"
        ],
        "risk_factors": [
            "Tiền sử gia đình mắc vảy nến",
            "Stress, nhiễm liên cầu khuẩn, một số thuốc (lithium, beta-blocker)",
            "Béo phì, hút thuốc lá, uống rượu"
        ],
        "symptoms": [
            "Mảng đỏ, giới hạn rõ, phủ vảy trắng bạc, hay gặp ở khuỷu tay, đầu gối, da đầu",
            "Ngứa hoặc rát nhẹ tại vùng tổn thương",
            "Có thể kèm tổn thương móng (rỗ móng, dày móng)"
        ],
        "complications": [
            "Viêm khớp vảy nến (psoriatic arthritis)",
            "Tăng nguy cơ hội chứng chuyển hóa, bệnh tim mạch",
            "Ảnh hưởng tâm lý, chất lượng cuộc sống"
        ],
        "treatment": {
            "medication": [
                "Corticosteroid bôi tại chỗ, dẫn xuất vitamin D3 (calcipotriol)",
                "Thuốc toàn thân (methotrexate, cyclosporine) cho thể nặng",
                "Thuốc sinh học (anti-TNF, anti-IL17/23) cho thể trung bình-nặng kháng trị"
            ],
            "procedure": [
                "Quang trị liệu (UVB dải hẹp, PUVA)"
            ],
            "lifestyle": [
                "Dưỡng ẩm da thường xuyên, tránh chà xát/gãi mạnh",
                "Kiểm soát cân nặng, hạn chế rượu bia, bỏ thuốc lá",
                "Quản lý stress"
            ]
        },
        "prognosis": (
            "Là bệnh mạn tính, tiến triển từng đợt, không thể chữa khỏi hoàn "
            "toàn nhưng kiểm soát tốt bằng điều trị phù hợp, phần lớn bệnh "
            "nhân duy trì được chất lượng cuộc sống ổn định."
        ),
        "follow_up": [
            "Tái khám định kỳ đánh giá đáp ứng điều trị, tác dụng phụ thuốc",
            "Tầm soát viêm khớp, hội chứng chuyển hóa định kỳ"
        ],
        "emergency_warning": [
            "Vảy nến thể mủ toàn thân hoặc đỏ da toàn thân kèm sốt cao",
            "Dấu hiệu nhiễm trùng thứ phát lan rộng"
        ]
    },

    # ------------------------------------------------------
    # L20 - Viêm da cơ địa (Atopic dermatitis)
    # ------------------------------------------------------
    "L20": {
        "causes": [
            "Rối loạn hàng rào bảo vệ da (thiếu hụt filaggrin) kết hợp phản ứng viêm dị ứng",
            "Yếu tố cơ địa dị ứng (atopy) di truyền"
        ],
        "risk_factors": [
            "Tiền sử bản thân/gia đình hen suyễn, viêm mũi dị ứng, viêm da cơ địa",
            "Môi trường khô, tiếp xúc chất kích ứng, xà phòng mạnh",
            "Khởi phát sớm ở trẻ nhỏ"
        ],
        "symptoms": [
            "Da khô, ngứa nhiều, đặc biệt về đêm",
            "Mảng đỏ, có thể rỉ dịch hoặc lichen hóa (dày da) ở nếp gấp (khuỷu tay, khoeo chân)",
            "Diễn tiến từng đợt, xen kẽ đợt bùng phát và ổn định"
        ],
        "complications": [
            "Bội nhiễm da do gãi (chốc hóa)",
            "Viêm da tiếp xúc thứ phát do dùng thuốc/mỹ phẩm không phù hợp",
            "Ảnh hưởng giấc ngủ, chất lượng cuộc sống"
        ],
        "treatment": {
            "medication": [
                "Corticosteroid bôi tại chỗ theo bậc tổn thương",
                "Thuốc ức chế calcineurin bôi (tacrolimus, pimecrolimus) cho vùng da nhạy cảm",
                "Thuốc sinh học (anti-IL4/13) hoặc ức chế JAK cho thể nặng"
            ],
            "procedure": [
                "Quang trị liệu UVB cho thể mạn tính lan rộng"
            ],
            "lifestyle": [
                "Dưỡng ẩm da hàng ngày (emollient) ngay cả khi da đang ổn định",
                "Tránh xà phòng có tính tẩy mạnh, tắm nước ấm vừa phải",
                "Xác định và tránh yếu tố khởi phát cá nhân"
            ]
        },
        "prognosis": (
            "Nhiều trường hợp ở trẻ em cải thiện dần theo tuổi; một số kéo dài "
            "đến tuổi trưởng thành. Kiểm soát tốt bằng dưỡng ẩm và điều trị "
            "đúng giai đoạn giúp giảm tần suất và mức độ bùng phát."
        ),
        "follow_up": [
            "Đánh giá lại mức độ tổn thương và điều chỉnh phác đồ mỗi vài tuần khi bùng phát",
            "Theo dõi tác dụng phụ khi dùng corticosteroid kéo dài"
        ],
        "emergency_warning": [
            "Sốt kèm tổn thương da lan rộng, rỉ mủ (nghi ngờ bội nhiễm nặng, eczema herpeticum)",
            "Tổn thương lan nhanh toàn thân"
        ]
    },

    # ------------------------------------------------------
    # L21 - Viêm da tiết bã
    # ------------------------------------------------------
    "L21": {
        "causes": [
            "Phản ứng viêm liên quan đến nấm men Malassezia trên vùng da tiết nhiều bã nhờn",
            "Rối loạn điều hòa miễn dịch tại chỗ"
        ],
        "risk_factors": [
            "Da dầu, stress, thời tiết lạnh khô",
            "Bệnh Parkinson, HIV, một số bệnh thần kinh làm tăng nguy cơ và mức độ nặng"
        ],
        "symptoms": [
            "Mảng đỏ, vảy nhờn vàng nhạt ở da đầu, mặt (rãnh mũi má, lông mày), ngực",
            "Ngứa nhẹ đến trung bình"
        ],
        "complications": [
            "Bội nhiễm da thứ phát khi gãi nhiều",
            "Tái phát mạn tính ảnh hưởng thẩm mỹ"
        ],
        "treatment": {
            "medication": [
                "Thuốc chống nấm bôi tại chỗ (ketoconazole, ciclopirox)",
                "Corticosteroid nhẹ bôi ngắn ngày khi viêm nhiều"
            ],
            "procedure": [],
            "lifestyle": [
                "Gội đầu/rửa mặt bằng dầu gội hoặc sữa rửa mặt có tính chống nấm định kỳ",
                "Tránh sản phẩm chăm sóc da gây bít tắc, nhờn"
            ]
        },
        "prognosis": (
            "Là bệnh mạn tính, dễ tái phát nhưng đáp ứng tốt với điều trị "
            "duy trì, không gây nguy hiểm sức khỏe toàn thân."
        ),
        "follow_up": [
            "Tái khám nếu tổn thương không cải thiện sau 2-4 tuần điều trị"
        ],
        "emergency_warning": []
    },

    # ------------------------------------------------------
    # L24 / L25 - Viêm da tiếp xúc
    # ------------------------------------------------------
    "L24": {
        "causes": [
            "Tổn thương trực tiếp hàng rào da do chất kích ứng (xà phòng, hóa chất, ma sát)"
        ],
        "risk_factors": [
            "Nghề nghiệp tiếp xúc hóa chất, rửa tay thường xuyên",
            "Da khô sẵn có, viêm da cơ địa nền"
        ],
        "symptoms": [
            "Đỏ da, khô, nứt tại vùng tiếp xúc, xuất hiện nhanh sau tiếp xúc",
            "Rát nhiều hơn ngứa (khác với dị ứng)"
        ],
        "complications": [
            "Nứt da sâu, bội nhiễm nếu tiếp xúc kéo dài"
        ],
        "treatment": {
            "medication": [
                "Corticosteroid bôi tại chỗ mức độ nhẹ-trung bình trong đợt viêm cấp"
            ],
            "procedure": [],
            "lifestyle": [
                "Loại bỏ/tránh tiếp xúc tác nhân gây kích ứng",
                "Dùng găng tay bảo hộ, dưỡng ẩm phục hồi hàng rào da"
            ]
        },
        "prognosis": (
            "Thường cải thiện nhanh sau khi loại bỏ tác nhân kích ứng và "
            "chăm sóc da đúng cách."
        ),
        "follow_up": [
            "Tái khám nếu không cải thiện sau khi tránh tiếp xúc 1-2 tuần"
        ],
        "emergency_warning": []
    },

    "L25": {
        "causes": [
            "Phản ứng dị ứng type IV qua trung gian tế bào T với dị nguyên tiếp xúc (kim loại, mỹ phẩm, cao su...)"
        ],
        "risk_factors": [
            "Tiền sử dị ứng tiếp xúc trước đó",
            "Tiếp xúc nghề nghiệp với dị nguyên (nickel, cao su, mỹ phẩm)"
        ],
        "symptoms": [
            "Ngứa nhiều, đỏ da, có thể nổi mụn nước đúng hình dạng vùng tiếp xúc",
            "Xuất hiện 24-72 giờ sau tiếp xúc dị nguyên"
        ],
        "complications": [
            "Lan rộng nếu tiếp tục tiếp xúc dị nguyên",
            "Bội nhiễm da thứ phát"
        ],
        "treatment": {
            "medication": [
                "Corticosteroid bôi tại chỗ, kháng histamin uống giảm ngứa",
                "Corticosteroid uống ngắn ngày cho trường hợp lan rộng nặng"
            ],
            "procedure": [
                "Test áp da (patch test) để xác định dị nguyên"
            ],
            "lifestyle": [
                "Tránh tuyệt đối dị nguyên đã xác định"
            ]
        },
        "prognosis": (
            "Cải thiện tốt khi xác định và tránh được dị nguyên gây bệnh; "
            "có thể tái phát nếu tiếp xúc lại."
        ),
        "follow_up": [
            "Tái khám để làm patch test nếu tái phát nhiều lần không rõ nguyên nhân"
        ],
        "emergency_warning": [
            "Phù nề lan rộng vùng mặt/mắt, khó thở (nghi phản ứng dị ứng nặng)"
        ]
    },

    # ------------------------------------------------------
    # L01 - Chốc lở
    # ------------------------------------------------------
    "L01": {
        "causes": [
            "Nhiễm trùng da nông do vi khuẩn Staphylococcus aureus và/hoặc Streptococcus pyogenes"
        ],
        "risk_factors": [
            "Trẻ em, vệ sinh kém, thời tiết nóng ẩm",
            "Da có vết trầy xước, côn trùng cắn, eczema nền"
        ],
        "symptoms": [
            "Mụn nước/mụn mủ nông, vỡ ra đóng vảy màu vàng mật ong",
            "Thường ở vùng mặt quanh mũi miệng, dễ lây lan tiếp xúc"
        ],
        "complications": [
            "Lan rộng ra vùng da khác do gãi, tiếp xúc",
            "Hiếm gặp: viêm cầu thận sau nhiễm liên cầu"
        ],
        "treatment": {
            "medication": [
                "Kháng sinh bôi tại chỗ (mupirocin, fusidic acid) cho thể khu trú",
                "Kháng sinh uống (cephalosporin, amoxicillin-clavulanate) cho thể lan rộng"
            ],
            "procedure": [],
            "lifestyle": [
                "Vệ sinh da sạch sẽ, rửa nhẹ nhàng loại bỏ vảy",
                "Tránh dùng chung khăn/vật dụng cá nhân để hạn chế lây lan"
            ]
        },
        "prognosis": "Đáp ứng tốt với điều trị kháng sinh, thường khỏi trong 7-10 ngày.",
        "follow_up": [
            "Tái khám nếu không cải thiện sau 3-5 ngày dùng kháng sinh"
        ],
        "emergency_warning": [
            "Sốt cao, sưng nề lan rộng (nghi biến chứng viêm mô tế bào)"
        ]
    },

    # ------------------------------------------------------
    # L03 - Viêm mô tế bào (Cellulitis)
    # ------------------------------------------------------
    "L03": {
        "causes": [
            "Nhiễm trùng mô mềm do vi khuẩn (thường Streptococcus, Staphylococcus) xâm nhập qua vết thương hở"
        ],
        "risk_factors": [
            "Vết thương da, côn trùng cắn, nấm kẽ chân tạo cửa ngõ vi khuẩn",
            "Suy tĩnh mạch, phù bạch huyết, đái tháo đường, suy giảm miễn dịch"
        ],
        "symptoms": [
            "Vùng da sưng, nóng, đỏ, đau, giới hạn không rõ, lan nhanh",
            "Có thể kèm sốt, mệt mỏi, nổi hạch vùng lân cận"
        ],
        "complications": [
            "Áp xe dưới da, nhiễm trùng huyết",
            "Viêm mô tế bào hoại tử (hiếm nhưng nguy hiểm)"
        ],
        "treatment": {
            "medication": [
                "Kháng sinh uống hoặc tiêm tùy mức độ (nhóm beta-lactam, hoặc kháng sinh phủ MRSA nếu nghi ngờ)"
            ],
            "procedure": [
                "Rạch dẫn lưu nếu có áp xe kèm theo"
            ],
            "lifestyle": [
                "Kê cao chi tổn thương, nghỉ ngơi",
                "Điều trị cửa ngõ nhiễm trùng (nấm kẽ chân, vết thương hở)"
            ]
        },
        "prognosis": (
            "Đáp ứng tốt với kháng sinh phù hợp nếu điều trị sớm; có thể "
            "nặng nhanh nếu trì hoãn, đặc biệt ở người có bệnh nền."
        ),
        "follow_up": [
            "Đánh giá lại sau 48-72 giờ điều trị kháng sinh để xác nhận đáp ứng"
        ],
        "emergency_warning": [
            "Sốt cao, lơ mơ, tụt huyết áp (nghi nhiễm trùng huyết)",
            "Đau dữ dội không tương xứng tổn thương, da tím đen (nghi hoại tử)"
        ]
    },

    # ------------------------------------------------------
    # L50 - Mề đay (Urticaria)
    # ------------------------------------------------------
    "L50": {
        "causes": [
            "Giải phóng histamin từ tế bào mast qua cơ chế dị ứng hoặc không dị ứng",
            "Nguyên nhân: thức ăn, thuốc, nhiễm trùng, yếu tố vật lý (lạnh, nóng, áp lực), tự phát"
        ],
        "risk_factors": [
            "Tiền sử dị ứng, cơ địa atopy",
            "Đang dùng thuốc mới (kháng sinh, NSAID)"
        ],
        "symptoms": [
            "Sẩn phù đỏ, ngứa, xuất hiện đột ngột, di chuyển vị trí, mỗi tổn thương tồn tại <24 giờ",
            "Có thể kèm phù mạch (phù môi, mí mắt)"
        ],
        "complications": [
            "Phù mạch đường thở (hiếm nhưng nguy hiểm)",
            "Mề đay mạn tính (>6 tuần) ảnh hưởng chất lượng cuộc sống"
        ],
        "treatment": {
            "medication": [
                "Kháng histamin H1 thế hệ 2 liều chuẩn hoặc tăng liều nếu cần",
                "Corticosteroid uống ngắn ngày cho đợt cấp nặng",
                "Omalizumab cho mề đay mạn tính kháng trị"
            ],
            "procedure": [],
            "lifestyle": [
                "Xác định và tránh yếu tố khởi phát nếu biết rõ",
                "Tránh gãi, mặc đồ rộng thoáng"
            ]
        },
        "prognosis": (
            "Mề đay cấp thường tự giới hạn, khỏi trong vài ngày đến vài tuần. "
            "Mề đay mạn tính có thể kéo dài nhiều tháng-năm nhưng kiểm soát "
            "được bằng thuốc."
        ),
        "follow_up": [
            "Tái khám nếu mề đay kéo dài trên 6 tuần để tìm nguyên nhân/chuyển chuyên khoa dị ứng"
        ],
        "emergency_warning": [
            "Khó thở, khàn giọng, phù lưỡi/họng (nghi sốc phản vệ) — cần cấp cứu ngay"
        ]
    },

    # ------------------------------------------------------
    # B86 - Ghẻ (Scabies)
    # ------------------------------------------------------
    "B86": {
        "causes": [
            "Nhiễm ký sinh trùng Sarcoptes scabiei đào hang dưới da"
        ],
        "risk_factors": [
            "Sống/sinh hoạt tập thể đông người, vệ sinh kém",
            "Tiếp xúc da kề da với người bệnh"
        ],
        "symptoms": [
            "Ngứa dữ dội, tăng nhiều về đêm",
            "Đường hầm ghẻ, sẩn nhỏ ở kẽ ngón tay, cổ tay, vùng sinh dục, nếp gấp cơ thể"
        ],
        "complications": [
            "Bội nhiễm da do gãi (chốc hóa)",
            "Ghẻ Na Uy (thể nặng) ở người suy giảm miễn dịch, dễ lây lan mạnh"
        ],
        "treatment": {
            "medication": [
                "Permethrin 5% bôi toàn thân, để qua đêm, có thể lặp lại sau 1 tuần",
                "Ivermectin uống cho thể nặng hoặc dịch bùng phát tập thể",
                "Kháng histamin giảm ngứa hỗ trợ"
            ],
            "procedure": [],
            "lifestyle": [
                "Giặt đồ dùng cá nhân, chăn ga bằng nước nóng, phơi nắng",
                "Điều trị đồng thời tất cả người tiếp xúc gần để tránh tái nhiễm"
            ]
        },
        "prognosis": "Khỏi hoàn toàn nếu điều trị đúng và điều trị đồng thời người tiếp xúc.",
        "follow_up": [
            "Ngứa có thể kéo dài 2-4 tuần sau điều trị do phản ứng dị ứng còn sót, không phải thất bại điều trị",
            "Tái khám nếu còn tổn thương mới xuất hiện sau 4 tuần"
        ],
        "emergency_warning": []
    },

    # ------------------------------------------------------
    # B02 - Zona (Herpes zoster)
    # ------------------------------------------------------
    "B02": {
        "causes": [
            "Tái hoạt động virus Varicella-zoster tiềm ẩn trong hạch thần kinh sau nhiễm thủy đậu"
        ],
        "risk_factors": [
            "Người lớn tuổi (>50), suy giảm miễn dịch, stress",
            "Tiền sử thủy đậu trước đó"
        ],
        "symptoms": [
            "Đau rát, dị cảm theo dải da (dermatome) trước khi nổi ban 2-3 ngày",
            "Mụn nước tập trung thành chùm trên nền da đỏ, theo một bên cơ thể, không vượt đường giữa"
        ],
        "complications": [
            "Đau thần kinh sau zona (postherpetic neuralgia) kéo dài",
            "Zona mắt gây tổn thương giác mạc nếu không điều trị kịp thời",
            "Bội nhiễm da thứ phát"
        ],
        "treatment": {
            "medication": [
                "Thuốc kháng virus (acyclovir, valacyclovir, famciclovir) trong 72 giờ đầu",
                "Giảm đau (paracetamol, gabapentin/pregabalin nếu đau thần kinh)"
            ],
            "procedure": [],
            "lifestyle": [
                "Giữ tổn thương sạch, khô, tránh cào gãi làm bội nhiễm",
                "Nghỉ ngơi, tránh tiếp xúc người chưa có miễn dịch thủy đậu (trẻ nhỏ, phụ nữ mang thai)"
            ]
        },
        "prognosis": (
            "Đa số hồi phục tốt trong 2-4 tuần nếu điều trị sớm; nguy cơ đau "
            "thần kinh sau zona tăng theo tuổi."
        ),
        "follow_up": [
            "Tái khám nếu đau kéo dài sau khi tổn thương da đã lành (nghi đau thần kinh sau zona)"
        ],
        "emergency_warning": [
            "Zona vùng mắt kèm đỏ mắt, giảm thị lực — cần khám mắt cấp cứu",
            "Zona lan tỏa toàn thân ở người suy giảm miễn dịch"
        ]
    },

    # ------------------------------------------------------
    # B35 - Nhiễm nấm da (Dermatophytosis)
    # ------------------------------------------------------
    "B35": {
        "causes": [
            "Nhiễm nấm da (dermatophyte) như Trichophyton, Microsporum ở lớp sừng da/tóc/móng"
        ],
        "risk_factors": [
            "Môi trường nóng ẩm, ra mồ hôi nhiều, mang giày kín lâu",
            "Tiếp xúc người/động vật nhiễm nấm, dùng chung vật dụng cá nhân"
        ],
        "symptoms": [
            "Mảng đỏ hình vòng nhẫn, bờ rõ, có vảy, ngứa, lan rộng dần ra ngoài",
            "Nấm kẽ chân: bong tróc, nứt, ngứa giữa các ngón chân"
        ],
        "complications": [
            "Bội nhiễm vi khuẩn thứ phát do gãi",
            "Lan rộng, tái phát nếu điều trị không đủ thời gian"
        ],
        "treatment": {
            "medication": [
                "Thuốc chống nấm bôi tại chỗ (clotrimazole, terbinafine) 2-4 tuần",
                "Thuốc chống nấm uống (terbinafine, itraconazole) cho tổn thương lan rộng hoặc nấm móng/tóc"
            ],
            "procedure": [],
            "lifestyle": [
                "Giữ da khô thoáng, thay tất/giày thường xuyên",
                "Không dùng chung khăn, giày dép với người khác"
            ]
        },
        "prognosis": "Đáp ứng tốt với điều trị đúng phác đồ và đủ thời gian, dễ tái phát nếu ngưng thuốc sớm.",
        "follow_up": [
            "Tái khám nếu không cải thiện sau 2-4 tuần điều trị bôi tại chỗ"
        ],
        "emergency_warning": []
    },

    # ------------------------------------------------------
    # L80 - Bạch biến (Vitiligo)
    # ------------------------------------------------------
    "L80": {
        "causes": [
            "Cơ chế tự miễn phá hủy tế bào hắc tố (melanocyte) tại chỗ"
        ],
        "risk_factors": [
            "Tiền sử gia đình mắc bạch biến hoặc bệnh tự miễn khác (tuyến giáp...)",
            "Sang chấn da tại chỗ (hiện tượng Koebner)"
        ],
        "symptoms": [
            "Mảng da mất sắc tố trắng, giới hạn rõ, đối xứng hai bên, thường ở mặt, tay, vùng nếp gấp",
            "Không ngứa, không đau"
        ],
        "complications": [
            "Ảnh hưởng thẩm mỹ, tâm lý",
            "Có thể liên quan bệnh tự miễn khác (tuyến giáp)"
        ],
        "treatment": {
            "medication": [
                "Corticosteroid bôi tại chỗ hoặc ức chế calcineurin cho tổn thương khu trú",
                "Thuốc ức chế JAK bôi/uống cho thể lan rộng (theo chỉ định chuyên khoa)"
            ],
            "procedure": [
                "Quang trị liệu UVB dải hẹp",
                "Ghép tế bào hắc tố cho tổn thương ổn định, khu trú"
            ],
            "lifestyle": [
                "Chống nắng kỹ vùng da mất sắc tố (dễ bắt nắng, cháy nắng)",
                "Hỗ trợ tâm lý nếu ảnh hưởng nhiều đến chất lượng sống"
            ]
        },
        "prognosis": (
            "Diễn tiến khó dự đoán, có thể ổn định hoặc lan rộng theo thời "
            "gian; điều trị giúp cải thiện thẩm mỹ nhưng khó phục hồi hoàn "
            "toàn sắc tố ở tổn thương lâu năm."
        ),
        "follow_up": [
            "Tầm soát chức năng tuyến giáp định kỳ nếu nghi ngờ bệnh tự miễn phối hợp"
        ],
        "emergency_warning": []
    },

    # ------------------------------------------------------
    # L63 - Rụng tóc từng vùng (Alopecia areata)
    # ------------------------------------------------------
    "L63": {
        "causes": [
            "Cơ chế tự miễn tấn công nang tóc gây rụng tóc không sẹo"
        ],
        "risk_factors": [
            "Tiền sử gia đình, bệnh tự miễn khác đi kèm",
            "Stress tâm lý là yếu tố khởi phát ở một số trường hợp"
        ],
        "symptoms": [
            "Mảng rụng tóc tròn, giới hạn rõ, da đầu vùng rụng bình thường không sẹo",
            "Có thể tiến triển thành rụng toàn bộ da đầu hoặc toàn thân (thể nặng)"
        ],
        "complications": [
            "Ảnh hưởng tâm lý, thẩm mỹ đáng kể",
            "Có thể tái phát nhiều đợt"
        ],
        "treatment": {
            "medication": [
                "Corticosteroid tiêm trong tổn thương hoặc bôi tại chỗ cho thể khu trú",
                "Thuốc ức chế JAK uống cho thể lan rộng/nặng (theo chỉ định chuyên khoa)"
            ],
            "procedure": [],
            "lifestyle": [
                "Hỗ trợ tâm lý, tư vấn kỳ vọng điều trị thực tế"
            ]
        },
        "prognosis": (
            "Nhiều trường hợp mọc tóc lại tự nhiên trong vòng 1 năm; một số "
            "tiến triển mạn tính, tái phát nhiều lần, khó tiên lượng."
        ),
        "follow_up": [
            "Tái khám đánh giá đáp ứng điều trị mỗi 2-3 tháng"
        ],
        "emergency_warning": []
    },

    # ------------------------------------------------------
    # L57.0 - Dày sừng ánh sáng (Actinic keratosis)
    # ------------------------------------------------------
    "L57.0": {
        "causes": [
            "Tổn thương tế bào sừng do tích lũy tia UV lâu dài, được xem là tổn thương tiền ung thư"
        ],
        "risk_factors": [
            "Da trắng, tiếp xúc nắng nhiều năm, tuổi cao",
            "Suy giảm miễn dịch"
        ],
        "symptoms": [
            "Mảng sần sùi, khô ráp, màu hồng-nâu, cảm giác như giấy nhám khi sờ",
            "Thường ở vùng da hở: mặt, da đầu hói, mu bàn tay"
        ],
        "complications": [
            "Có thể tiến triển thành ung thư biểu mô tế bào vảy nếu không theo dõi/điều trị"
        ],
        "treatment": {
            "medication": [
                "5-Fluorouracil hoặc imiquimod bôi tại chỗ theo đợt"
            ],
            "procedure": [
                "Áp lạnh nitơ lỏng (cryotherapy)",
                "Liệu pháp quang động (photodynamic therapy) cho tổn thương lan rộng"
            ],
            "lifestyle": [
                "Chống nắng nghiêm ngặt để phòng tổn thương mới"
            ]
        },
        "prognosis": "Đáp ứng tốt với điều trị tại chỗ nếu phát hiện sớm, cần theo dõi định kỳ do nguy cơ tiến triển ác tính.",
        "follow_up": [
            "Khám da định kỳ 6-12 tháng để phát hiện tổn thương mới hoặc dấu hiệu chuyển dạng ác tính"
        ],
        "emergency_warning": [
            "Tổn thương trở nên cứng, loét, chảy máu, phát triển nhanh (nghi chuyển dạng ung thư)"
        ]
    },
}


# ==========================================================
# NỘI DUNG DỰ PHÒNG khi mã bệnh chưa có dữ liệu chi tiết
# ==========================================================

def build_generic_analysis(name_vi, chapter_name=None):
    """
    Trả về khung phân tích tổng quát, trung thực (không bịa số liệu
    y khoa cụ thể) khi chưa có dữ liệu chi tiết riêng cho mã bệnh này.
    """

    ten = name_vi or "bệnh lý này"

    return {
        "causes": [
            f"Nguyên nhân của {ten} cần được đánh giá dựa trên bệnh sử, "
            "triệu chứng lâm sàng cụ thể và có thể cần xét nghiệm/sinh thiết bổ sung."
        ],
        "risk_factors": [
            "Yếu tố nguy cơ phụ thuộc từng trường hợp cụ thể — khai thác "
            "tiền sử cá nhân, gia đình, môi trường và nghề nghiệp của bệnh nhân."
        ],
        "symptoms": [
            "Triệu chứng lâm sàng điển hình cần được xác nhận qua thăm khám "
            "trực tiếp và đối chiếu với hình ảnh tổn thương thực tế."
        ],
        "complications": [
            "Biến chứng có thể xảy ra tùy mức độ và thời gian tiến triển "
            "bệnh — cần theo dõi lâm sàng để đánh giá cụ thể."
        ],
        "treatment": {
            "medication": [],
            "procedure": [],
            "lifestyle": []
        },
        "prognosis": (
            "Tiên lượng phụ thuộc vào giai đoạn phát hiện, mức độ tổn "
            "thương và đáp ứng điều trị của từng bệnh nhân cụ thể."
        ),
        "follow_up": [
            "Tái khám theo chỉ định của bác sĩ điều trị trực tiếp."
        ],
        "emergency_warning": []
    }


def get_analysis(code, name_vi=None, chapter_name=None):
    """
    Lấy dữ liệu phân tích cho 1 mã ICD-10.

    Ưu tiên:
    1. Mã đầy đủ (vd: L57.0)
    2. Mã nhóm 3 ký tự (vd: L57 -> tra theo "L57" nếu có,
       nếu không thì thử tiền tố gần nhất đã khai báo, ví dụ C43.9 -> C43)
    3. Nội dung tổng quát dự phòng
    """

    if not code:
        return build_generic_analysis(name_vi, chapter_name)

    code = str(code).strip().upper()

    if code in ICD10_ANALYSIS_DATA:
        return ICD10_ANALYSIS_DATA[code]

    base_code = code.split(".")[0]

    if base_code in ICD10_ANALYSIS_DATA:
        return ICD10_ANALYSIS_DATA[base_code]

    return build_generic_analysis(name_vi, chapter_name)