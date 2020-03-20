#! /usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask # VKApi
from flask import request # VKApi
from flask import jsonify # VKApi
from flask_sslify import SSLify # VKApi
import requests # VKApi & YandexPars
import random # VKApi
import vk_api # VKApi
import json # VKApi
import os # VKApi & Heroku
from lxml import html # YandexPars
import time # YandexPars

# YandexPars
def get_tags(photo_url):
    yandex_search = "https://yandex.ru/images/search?source=collections&rpt=imageview&rdrnd="+str(random.randint(100000, 999999))+"&redircnt="+str(random.randint(1000000000, 9999999999))+".1&url="+photo_url
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
    html_url = requests.get(yandex_search, headers={'User-Agent':user_agent}) # загрузить страницу запроса
    tree_html = html.fromstring(html_url.text.encode('UTF-8')) # получить html страницы запроса
    tags_tree = tree_html.xpath('//a[contains(@class, "tags__tag")]') # a теги с атрибутом clas равным "..."
    tags = [i.text for i in tags_tree] # преобразовать в текст найденные теги
    return tags

def get_result(photo_url):
    tags = get_tags(photo_url)
    if tags == []: # перепроверка, если нет тегов
        time.sleep(random.randint(7, 10))
        tags = get_tags(photo_url)
        if tags == []: # если второй раз нет тегов
            return "Кажется, на картинке что-то непонятное."
    tags = ", ".join(tags) # формирование списка тегов
    message = "Кажется, на картинке " + tags + "." # формирование сообщения
    return message

# VKApi
token = str(os.environ.get("TOKEN")) # токен ВК сообщества-бота
confirmation_token = str(os.environ.get("CONFIRMATION_TOKEN")) # код подтверждения CallBack ВК
vk = vk_api.VkApi(token=token, api_version='5.89') # иницилизация ВК Api с токеном и версией Api

# Flask
app = Flask(__name__) # иницилизация Сервера через Flask
sslify = SSLify(app) # защита Сервера через SSL

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST': # Ответ, если POST запрос (новое событие CallBack - сообщение)
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
    elif request.method == 'GET': # Ответ, если GET запрос (загрузка страницы)
        return '<h1>VKBot working now!</h1>'
    return 'OK' # Постоянный ответ сервера

# SystemDebug
if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
