#! /usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from flask import request
from flask import jsonify
from flask_sslify import SSLify
import requests
import random
import vk_api
import json
import os


# VkApi
token = str(os.environ.get("TOKEN"))
confirmation_token = str(os.environ.get("CONFIRMATION_TOKEN"))
vk = vk_api.VkApi(token=token, api_version='5.89')
# -VkApi
# Flask
app = Flask(__name__)
sslify = SSLify(app)

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        data = json.loads(request.data)
        if data["type"] == "confirmation": # подтверждение CallBack
            return confirmation_token
        elif data["type"] == "message_new":
            try:
                object = data["object"]
                attachments = object["attachments"]
                if attachments != []: # Проверяем есть ли прикрепления
                    if attachments[0]["type"] == "photo": # Проверяем есть ли фото в прикреплении
                        print("1")
                        id = object["peer_id"]
                        print("2")
                        photo = attachments[0]["photo"]
                        print("3")
                        largest_photo = photo["sizes"][-1]
                        print("4")
                        url_photo = largest_photo["url"]
                        print("5")
                        vk.method("messages.send", {"peer_id": id, "message": url_photo, "random_id": random.randint(1, 2147483647)})
                # ----- Обработка команд -----
                # body = object["text"]
                # if body.lower() == "привет":
                #     vk.method("messages.send", {"peer_id": id, "message": "Привет!", "random_id": random.randint(1, 2147483647)})
                # ----------------------------
            except Exception as log_errore:
                print("LOG:", log_errore) # Лог ошибок
    elif request.method == 'GET':
        return '<h1>VKBot working now!</h1>'
    return 'OK'
# -Flask

if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
