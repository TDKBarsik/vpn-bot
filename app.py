import os
import requests
from flask import Flask, Response

app = Flask(__name__)

# Добавили еще больше источников для выбора
SOURCES = [
    "https://raw.githubusercontent.com/yebekhe/TelegramV2rayCollector/main/sub/mix/base64",
    "https://raw.githubusercontent.com/LonUp/V2Ray-Config/main/All_Configs_Sub.txt",
    "https://raw.githubusercontent.com/SreSre/V2Ray-Config/main/All_Configs_Sub.txt"
]

@app.route('/')
@app.route('/sub')
def get_sub():
    all_vless = []
    
    for url in SOURCES:
        try:
            r = requests.get(url, timeout=5)
            if r.status_code == 200:
                lines = r.text.splitlines()
                for line in lines:
                    if line.startswith('vless://'):
                        low = line.lower()
                        # Ищем Германию ИЛИ просто Reality (даже если страна другая, они быстрые)
                        is_germany = any(x in low for x in ['germany', 'de-', ' de', '🇩🇪'])
                        is_reality = 'reality' in low
                        
                        if is_germany or is_reality:
                            all_vless.append(line)
        except:
            continue

    # Убираем дубликаты и перемешиваем, чтобы список обновлялся
    import random
    unique_vless = list(set(all_vless))
    random.shuffle(unique_vless)
    
    # Отдаем 20 штук. Теперь их точно будет много!
    output = "\n".join(unique_vless[:20])
    
    # Твой эталонный конфиг в самом конце списка
    backup = "vless://0eeb7510-3968-4dc4-9a32-ccea620455f2@free07.anotherboring.top:443?encryption=none&flow=xtls-rprx-vision&security=reality&sni=free07.anotherboring.top&fp=chrome&pbk=3l5cbMRcZBVfarehwBi_MbRHOkewJk3xDNYPtIQ3whM&sid=b20ffdf0010dce16&type=tcp#ETALON_GERMANY"
    
    final_res = output + "\n" + backup
    return Response(final_res, mimetype='text/plain')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
