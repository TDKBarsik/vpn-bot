import os
import requests
from flask import Flask, Response

app = Flask(__name__)

# Самый быстрый и стабильный источник
URL = "https://raw.githubusercontent.com/yebekhe/TelegramV2rayCollector/main/sub/mix/base64"

@app.route('/')
def home():
    return "Server is Live"

@app.route('/sub')
def get_sub():
    try:
        # Ставим короткий таймаут, чтобы не висеть долго
        r = requests.get(URL, timeout=5)
        if r.status_code == 200:
            # Берем первые 50 серверов (этого за глаза для скорости)
            lines = r.text.splitlines()
            short_list = "\n".join(lines[:50])
            return Response(short_list, mimetype='text/plain')
    except:
        pass
    
    # Резервный сервер, если основной источник тормозит
    backup = "vless://002446f2-7067-4a0b-932d-205169a84495@104.18.2.146:443?path=%2F&security=tls&encryption=none&type=ws#Backup"
    return Response(backup, mimetype='text/plain')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
