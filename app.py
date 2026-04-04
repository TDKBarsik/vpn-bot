import os
import requests
from flask import Flask, Response

app = Flask(__name__)

# Основной источник
URL = "https://raw.githubusercontent.com/yebekhe/TelegramV2rayCollector/main/sub/mix/base64"

@app.route('/')
def home():
    return "Server is live"

@app.route('/sub')
def get_sub():
    try:
        # Пробуем скачать базу (ждем не больше 10 секунд)
        r = requests.get(URL, timeout=10)
        if r.status_code == 200 and len(r.text) > 10:
            return Response(r.text, mimetype='text/plain')
    except:
        pass
    
    # ПЛАН Б: Если база не качается, выдаем этот запасной рабочий ключ
    backup = "vless://002446f2-7067-4a0b-932d-205169a84495@104.18.2.146:443?path=%2F&security=tls&encryption=none&type=ws#Zapasnoy_Server"
    return Response(backup, mimetype='text/plain')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
