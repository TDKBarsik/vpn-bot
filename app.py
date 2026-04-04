import os
import requests
from flask import Flask, Response

app = Flask(__name__)

# Источник с хорошим выбором VLESS
URL = "https://raw.githubusercontent.com/yebekhe/TelegramV2rayCollector/main/sub/mix/base64"

@app.route('/')
@app.route('/sub')
def get_sub():
    try:
        r = requests.get(URL, timeout=7)
        if r.status_code == 200:
            lines = r.text.splitlines()
            
            # ОСТАВЛЯЕМ ТОЛЬКО VLESS
            vless_only = [l for l in lines if l.startswith('vless://')]
            
            # Берем только первые 25 штук (самые свежие из базы)
            # Это гарантирует мгновенную загрузку в Happ
            optimized_data = "\n".join(vless_only[:25])
            
            return Response(optimized_data, mimetype='text/plain')
    except:
        pass
    
    # Твой личный "эталонный" сервер, если база не ответит
    backup = "vless://0eeb7510-3968-4dc4-9a32-ccea620455f2@free07.anotherboring.top:443?encryption=none&flow=xtls-rprx-vision&security=reality&sni=free07.anotherboring.top&fp=chrome&pbk=3l5cbMRcZBVfarehwBi_MbRHOkewJk3xDNYPtIQ3whM&sid=b20ffdf0010dce16&type=tcp#Zapasnoy_VLESS_Reality"
    return Response(backup, mimetype='text/plain')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
