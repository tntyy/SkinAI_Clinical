import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

api_key = os.getenv("XAI_API_KEY")

print("XAI KEY EXISTS:", bool(api_key))
print(
    "XAI KEY PREFIX:",
    api_key[:8] if api_key else None
)


class GrokService:

    _client = None

    # ======================================================
    # GET XAI CLIENT
    # ======================================================

    @classmethod
    def get_client(cls):

        if cls._client is None:

            api_key = os.getenv("XAI_API_KEY")

            if not api_key:
                raise RuntimeError(
                    "Chưa cấu hình XAI_API_KEY trong .env"
                )

            cls._client = OpenAI(
                api_key=api_key,
                base_url="https://api.x.ai/v1"
            )

        return cls._client

    # ======================================================
    # CHAT
    # ======================================================

    @classmethod
    def chat(cls, message, context):

        client = cls.get_client()

        system_prompt = f"""
Bạn là SkinAI Assistant,
trợ lý AI hỗ trợ bác sĩ trong hệ thống SkinAI Clinical.

Bạn phải trả lời bằng tiếng Việt.

QUY TẮC:

- Chỉ sử dụng dữ liệu được cung cấp trong CONTEXT.
- Không tự bịa thêm dữ liệu bệnh nhân.
- Không tự khẳng định chẩn đoán cuối cùng.
- Kết quả AI chỉ mang tính hỗ trợ bác sĩ.
- Luôn phân biệt "dự đoán của AI"
  và "chẩn đoán lâm sàng".
- Nếu dữ liệu không đủ, phải nói rõ dữ liệu hiện tại
  không đủ để kết luận.
- Trả lời ngắn gọn, rõ ràng, phù hợp với bác sĩ.

==================================================
CONTEXT
==================================================

Bệnh dự đoán:
{context.get("disease")}

Class AI:
{context.get("prediction")}

Confidence:
{context.get("confidence")}

ICD-10:
{context.get("icd10")}

Mức nguy cơ:
{context.get("risk")}

Tổng quan:
{context.get("overview")}

Triệu chứng:
{context.get("symptoms")}

Điều trị:
{context.get("treatment")}

Phòng ngừa:
{context.get("prevention")}

Theo dõi:
{context.get("follow_up")}

Heatmap / Grad-CAM:
Có: {context.get("heatmap")}

Heatmap path:
{context.get("heatmap_path")}

Overlay path:
{context.get("overlay_path")}

==================================================
"""

        response = client.responses.create(

            model=os.getenv(
                "XAI_MODEL",
                "grok-4.5"
            ),

            input=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": message
                }
            ]
        )

        return response.output_text

