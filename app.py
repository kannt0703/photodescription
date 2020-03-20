#! /usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask # VKBot
from flask import request # VKBot
from flask import jsonify # VKBot
from flask_sslify import SSLify # VKBot
import requests # VKBot & YandexPars
import random # VKBot
import vk_api # VKBot
import json # VKBot
import os # VKBot & Heroku
from lxml import html # YandexPars

# YandexPars
def get_tags(photo_url):
    yandex_search = "https://yandex.ru/images/search?rpt=imageview&url="+photo_url
    html_url = requests.get(yandex_search)
    tree_html = html.fromstring(html_url.text.encode('UTF-8'))
    tags_tree = tree_html.xpath('//a[contains(@class, "tags__tag")]') # a теги с атрибутом clas равным "..."
    tags = [i.text for i in tags_tree]
    return tags

def get_result(photo_url):
    tags = get_tags(photo_url)
    if tags == []:
        time.sleep(3)
        tags = get_tags(photo_url)
        if tags == []:
            message = "что-то непонятное"
    tags = ", ".join(tags)
    message = "Кажется, на картинке " + tags + "."
    return message

# VKApi
token = str(os.environ.get("TOKEN"))
confirmation_token = str(os.environ.get("CONFIRMATION_TOKEN"))
vk = vk_api.VkApi(token=token, api_version='5.89')

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
                        id = object["peer_id"]
                        photo = attachments[0]["photo"]
                        largest_photo = photo["sizes"][-1]
                        url_photo = largest_photo["url"]
                        vk.method("messages.send", {"peer_id": id, "message": get_result(url_photo), "random_id": random.randint(1, 2147483647)})
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

# SystemDebug
if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
