import os
import requests
from flask import Flask, Response

app = Flask(__name__)

# Ссылка на базу
URL = "https://raw.githubusercontent.com/yebekhe/TelegramV2rayCollector/main/sub/mix/base64"

@app.route('/')
def home():
    return "Server is live"

@app.route('/sub')
def get_sub():
    try:
        # Увеличил время ожидания до 20 секунд
        r = requests.get(URL, timeout=20)
        if r.status_code == 200:
            return Response(r.text, mimetype='text/plain')
        return "Source error", 500
    except:
        return "Connection error", 500

if __name__ == "__main__":
    # ЭТО САМАЯ ВАЖНАЯ ЧАСТЬ ДЛЯ RENDER:
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
