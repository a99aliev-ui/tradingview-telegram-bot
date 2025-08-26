import os
import requests
from flask import Flask, request

app = Flask(__name__)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")  # Bot tokenini Railwayda Environmentda qo‘shamiz
CHAT_ID = os.getenv("CHAT_ID")  # O'zingizning chat_id raqamingiz

def send_telegram_message(message: str):
    """Telegram'ga signal yuboradi"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print("Xatolik:", e)

@app.route("/signal", methods=["POST"])
def signal():
    data = request.json
    message = f"📊 Yangi signal:\n\n{data}"
    send_telegram_message(message)
    return {"status": "ok"}

@app.route("/")
def home():
    return "Bot ishlayapti ✅"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
