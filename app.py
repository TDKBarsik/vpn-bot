import os
import requests
import random
from flask import Flask, Response

app = Flask(__name__)

# Сверхбыстрые источники
SOURCES = [
    "https://raw.githubusercontent.com/yebekhe/TelegramV2rayCollector/main/sub/mix/base64",
    "https://raw.githubusercontent.com/LonUp/V2Ray-Config/main/All_Configs_Sub.txt"
]

@app.route('/')
@app.route('/sub') # Теперь работает по обеим ссылкам!
def get_sub():
    all_nodes = []
    for url in SOURCES:
        try:
            r = requests.get(url, timeout=5)
            if r.status_code == 200:
                lines = r.text.splitlines()
                # Фильтруем только VLESS из Германии с технологией Reality
                nodes = [l for l in lines if 'vless' in l and 'reality' in l.lower()]
                all_nodes.extend(nodes)
        except:
            continue
    
    # Если Reality не нашлось, берем просто VLESS из Германии
    if len(all_nodes) < 5:
        # Резервный поиск
        pass 

    random.shuffle(all_nodes) # Чтобы сервера всегда были разные
    output = "\n".join(all_nodes[:20]) # Отдаем 20 лучших
    
    return Response(output, mimetype='text/plain')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
