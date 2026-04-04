import os
import requests
from flask import Flask, Response

app = Flask(__name__)

# Источники, где больше всего свежих VLESS/REALITY (Германия)
SOURCES = [
    "https://raw.githubusercontent.com/yebekhe/TelegramV2rayCollector/main/sub/mix/base64",
    "https://raw.githubusercontent.com/LonUp/V2Ray-Config/main/All_Configs_Sub.txt",
    "https://raw.githubusercontent.com/SreSre/V2Ray-Config/main/All_Configs_Sub.txt"
]

@app.route('/')
@app.route('/sub')
def get_sub():
    vless_germany = []
    
    for url in SOURCES:
        try:
            # Таймаут 5 сек, чтобы не тормозило загрузку
            r = requests.get(url, timeout=5)
            if r.status_code == 200:
                lines = r.text.splitlines()
                for line in lines:
                    # Ищем только VLESS
                    if line.startswith('vless://'):
                        low = line.lower()
                        # Фильтр по Германии
                        if any(x in low for x in ['germany', 'de-', ' de', '🇩🇪', 'frankfurt']):
                            vless_germany.append(line)
        except:
            continue

    # Убираем дубликаты
    unique_vless = list(set(vless_germany))
    
    # Если база нашла сервера - отдаем топ-20 самых свежих
    if unique_vless:
        return Response("\n".join(unique_vless[:20]), mimetype='text/plain')
    
    # Твой личный "эталонный" конфиг как резерв
    backup = "vless://0eeb7510-3968-4dc4-9a32-ccea620455f2@free07.anotherboring.top:443?encryption=none&flow=xtls-rprx-vision&security=reality&sni=free07.anotherboring.top&fp=chrome&pbk=3l5cbMRcZBVfarehwBi_MbRHOkewJk3xDNYPtIQ3whM&sid=b20ffdf0010dce16&type=tcp#Zapasnoy_DE_Reality"
    return Response(backup, mimetype='text/plain')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
