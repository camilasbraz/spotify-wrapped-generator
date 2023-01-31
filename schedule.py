from flask import Flask
from threading import Thread
import webview


app = Flask('')

@app.route('/')
def home():
    return "Program is online/active, all thanks to UpTimeRobot!"


def run():
    app.run(host = '0.0.0.0', port = 8080)

def schedule():
    t = Thread(target = run)
    t.start()
    webview.create_window('Window #1', width=800, height=600)