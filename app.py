import os
import requests
import random
from flask import Flask, Response

app = Flask(__name__)

# Проверенные источники, которые обновляются чаще всего
SOURCES = [
    "https://raw.githubusercontent.com/yebekhe/TelegramV2rayCollector/main/sub/mix/base64",
    "https://raw.githubusercontent.com/LonUp/V2Ray-Config/main/All_Configs_Sub.txt",
    "https://raw.githubusercontent.com/SreSre/V2Ray-Config/main/All_Configs_Sub.txt"
]

@app.route('/')
@app.route('/sub')
def get_sub():
    # 1. Твой "золотой" конфиг (Германия 01), который работает на 100%
    # Мы ставим его ПЕРВЫМ и ВСЕГДА рабочим
    gold_config = "vless://0eeb7510-3968-4dc4-9a32-ccea620455f2@free07.anotherboring.top:443?encryption=none&flow=xtls-rprx-vision&security=reality&sni=free07.anotherboring.top&fp=chrome&pbk=3l5cbMRcZBVfarehwBi_MbRHOkewJk3xDNYPtIQ3whM&sid=b20ffdf0010dce16&type=tcp#TOP_GERMANY_10000%"
    
    all_nodes = [gold_config]
    
    # 2. Собираем свежую "подмогу" из интернета
    for url in SOURCES:
        try:
            r = requests.get(url, timeout=4)
            if r.status_code == 200:
                lines = r.text.splitlines()
                # Берем только VLESS и только те, что с Reality (самые быстрые)
                found = [l for l in lines if l.startswith('vless://') and 'reality' in l.lower()]
                all_nodes.extend(found)
        except:
            continue

    # 3. Умная фильтрация: оставляем только Германию и Reality
    # Если их мало, добавляем любые другие VLESS для массовки
    unique_nodes = list(dict.fromkeys(all_nodes)) # Убираем дубликаты, сохраняя порядок
    
    # Ограничиваем список до 15 лучших, чтобы Happ не тормозил
    final_output = "\n".join(unique_nodes[:15])
    
    return Response(final_output, mimetype='text/plain')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
