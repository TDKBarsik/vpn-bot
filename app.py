from flask import Flask, Response
import requests
import socket
from urllib.parse import urlparse

app = Flask(__name__)

SOURCE_URL = "https://raw.githubusercontent.com/MatinGhanbari/v2ray-configs/main/subscriptions/filtered/subs/hysteria2.txt"

def check_server(host, port):
    try:
        sock = socket.create_connection((host, port), timeout=2)
        sock.close()
        return True
    except:
        return False

def parse_link(link):
    try:
        parsed = urlparse(link)
        return parsed.hostname, parsed.port
    except:
        return None, None

@app.route("/")
def home():
    return "OK"

@app.route("/sub")
def sub():
    data = requests.get(SOURCE_URL).text.splitlines()
    working = []

    for line in data[:120]:
        host, port = parse_link(line)
        if host and port and check_server(host, port):
            working.append(line)

    return Response("\n".join(working[:50]), mimetype="text/plain")
