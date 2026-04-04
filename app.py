from flask import Flask, Response
import requests
import re
import os

app = Flask(__name__)

# Ссылка на базу бесплатных серверов
SOURCE_URL = "https://raw.githubusercontent.com/yebekhe/TVC/main/subscriptions/hiddify/mix"

@app.route('/')
def home():
    return "Bot is running. Use /sub for subscription link."

@app.route('/sub')
def sub():
    try:
        # Скачиваем общую базу
        response = requests.get(SOURCE_URL, timeout=10)
        data = response.text
        
        # Фильтруем только Hysteria2 и VLESS (самые быстрые)
        configs = []
        for line in data.splitlines():
            if line.startswith(('hysteria2://', 'vless://')):
                configs.append(line)
        
        # Берем первые 50 штук (самые свежие)
        result = "\n".join(configs[:50])
        
        return Response(result, mimetype='text/plain')
    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == "__main__":
    # Настройки порта для Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
