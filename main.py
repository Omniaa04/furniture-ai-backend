# from fastapi import FastAPI, UploadFile, File, Form
# from fastapi.middleware.cors import CORSMiddleware
# from huggingface_hub import InferenceClient
# import base64

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# client = InferenceClient(
#     api_key="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",
#     timeout=60
# )

# SYSTEM_PROMPT = """You are a furniture expert assistant.
# - If user writes in Arabic, respond in Arabic
# - If user writes in English, respond in English
# - Keep answers SHORT (max 5 lines)
# - Mention: furniture type, material, care tip"""

# @app.post("/analyze")
# async def analyze_furniture(
#     text: str = Form(default=""),
#     image: UploadFile = File(default=None)
# ):
#     try:
#         messages_content = []

#         if image:
#             image_data = await image.read()
#             b64 = base64.b64encode(image_data).decode()
#             messages_content.append({
#                 "type": "image_url",
#                 "image_url": {"url": f"data:image/jpeg;base64,{b64}"}
#             })

#         messages_content.append({
#             "type": "text",
#             "text": text if text else "Identify this furniture and give me key info."
#         })

#         response = client.chat.completions.create(
#             model="Qwen/Qwen2.5-VL-7B-Instruct",
#             messages=[
#                 {"role": "system", "content": SYSTEM_PROMPT},
#                 {"role": "user", "content": messages_content}
#             ],
#             max_tokens=150
#         )

#         return {"success": True, "response": response.choices[0].message.content}

#     except Exception as e:
#         return {"success": False, "error": str(e)}

# @app.get("/")
# def root():
#     return {"message": "Furniture AI API is running! 🛋️"}

from flask import Flask, request, jsonify
from flask_cors import CORS
from huggingface_hub import InferenceClient
import base64

app = Flask(__name__)
CORS(app)

client = InferenceClient(
    api_key="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",
    timeout=60
)

SYSTEM_PROMPT = """You are a furniture expert assistant.
- If user writes in Arabic, respond in Arabic
- If user writes in English, respond in English
- Keep answers SHORT (max 5 lines)
- Mention: furniture type, material, care tip"""

@app.route("/analyze", methods=["POST"])
def analyze_furniture():
    try:
        messages_content = []

        if 'image' in request.files:
            image = request.files['image']
            image_data = image.read()
            b64 = base64.b64encode(image_data).decode()
            messages_content.append({
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{b64}"}
            })

        text = request.form.get('text', '')
        messages_content.append({
            "type": "text",
            "text": text if text else "Identify this furniture and give me key info."
        })

        response = client.chat.completions.create(
            model="Qwen/Qwen2.5-VL-7B-Instruct",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": messages_content}
            ],
            max_tokens=150
        )

        return jsonify({"success": True, "response": response.choices[0].message.content})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route("/")
def root():
    return jsonify({"message": "Furniture AI API is running!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)