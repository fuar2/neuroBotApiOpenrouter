from flask import Flask, request, jsonify, render_template
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

# Получаем ключ из .env
openrouter_key = os.getenv("OPENROUTER_API_KEY")
if not openrouter_key:
    raise ValueError("Не найден OPENROUTER_API_KEY в переменных окружения")


client = OpenAI(
    api_key=openrouter_key,
    base_url="https://openrouter.ai/api/v1",
    
    default_headers={
        "HTTP-Referer": "http://localhost:5000",
        "X-Title": "MyChatApp"
    }
)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "")

    if user_message.strip() == "":
        return jsonify({"reply": ""})

    response = client.chat.completions.create(
        model="google/gemma-3-27b-it:free",
        messages=[
            {"role": "system", "content": "Ты консультант мебельного магазина. Помогай выбрать мебель, рассказывай о преимуществах и сравнивай варианты."},
            {"role": "user", "content": user_message}
        ]
    )

    reply = response.choices[0].message.content
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(port=5000, debug=True)
