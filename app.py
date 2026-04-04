import os
import requests
from flask import Flask, Response

app = Flask(__name__)

# Источник конфигов
URL = "https://raw.githubusercontent.com/yebekhe/TelegramV2rayCollector/main/sub/mix/base64"

@app.route('/')
@app.route('/sub')
def get_sub():
    try:
        r = requests.get(URL, timeout=10)
        if r.status_code == 200:
            lines = r.text.splitlines()
            
            # Фильтруем: только VLESS и только Германия
            germany_vless = []
            for line in lines:
                if line.startswith('vless://'):
                    # Проверяем наличие меток Германии в названии (после знака #)
                    lower_line = line.lower()
                    if any(mark in lower_line for mark in ['germany', ' de', 'de-', '🇩🇪']):
                        germany_vless.append(line)
            
            # Если нашли немецкие сервера, отдаем их (не больше 30 для скорости)
            if germany_vless:
                return Response("\n".join(germany_vless[:30]), mimetype='text/plain')
    except:
        pass
    
    # Твой личный быстрый немецкий сервер на случай, если база пуста
    backup = "vless://0eeb7510-3968-4dc4-9a32-ccea620455f2@free07.anotherboring.top:443?encryption=none&flow=xtls-rprx-vision&security=reality&sni=free07.anotherboring.top&fp=chrome&pbk=3l5cbMRcZBVfarehwBi_MbRHOkewJk3xDNYPtIQ3whM&sid=b20ffdf0010dce16&type=tcp#Zapasnoy_Germany_Fast"
    return Response(backup, mimetype='text/plain')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
