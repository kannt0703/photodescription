#! /usr/bin/env python
# -*- coding: utf-8 -*-


############## Modules
from flask_sslify import SSLify
from flask import Flask
from flask import request
from flask import jsonify
import requests
import json
import time
import random
import queue
import os
import vk_api
from threading import Thread
import multiprocessing

import yandexparse
##############


############## VKApi
token = str(os.environ.get("T18ed8d98c2467d4d9638f49a9c1fe8"))
confirmation_token = str(os.environ.get("CT18ed8d98c2467d4d9638f49a9c1fe8"))
vk = vk_api.VkApi(token=token, api_version='5.89')
##############


############## Functions
def message(data='', id=''):
    data=str(data)[:1000]
    vk.method("messages.send", {"peer_id": id, "message": data, "random_id": random.randint(1, 2147483647)})
    if len(data) >= 1000:
        cutmessage = "Ответ отображен не полностью: максимальное значение 1000 символов"
        vk.method("messages.send", {"peer_id": id, "message": cutmessage, "random_id": random.randint(1, 2147483647)})

def photo(data='', id=''):
    url=str(data)
    parse=yandexparse.get_tags(url)
    tags=parse[0]
    text=parse[1]
    if tags == []:
        result="Кажется, на картинке что-то непонятное."
    else:
        result="Кажется, на картинке " + ", ".join(tags) + "."
    message(result, id)
    if text != '':
        result="Распознан следующий текст:\n" + text
        message(result, id)
##############


############## Manage
queue = queue.Queue()

class Task(object):
    def __init__(self, func='', data='', id=''):
        self.func = func
        self.data = data
        self.id = id

def distribution():
    while not queue.empty():
        task = queue.get()
        Thread(target=task.func, args=(task.data, task.id,),daemon=True).start()

def new_task(func, data='', id=''):
    task = Task(func, data, id)
    queue.put(task)
    Thread(target=distribution, daemon=True).start()
##############


############## Flask
app = Flask(__name__)
sslify = SSLify(app)

@app.route('/', methods=['POST', 'GET'])
def index():
    try:
        if request.method == 'POST':
            requestdata = json.loads(request.data)
            if requestdata["type"] == "confirmation":
                return confirmation_token
            object = requestdata["object"]
            id = object["peer_id"]
            attachments = object["attachments"]
            text = object["text"]
            if attachments != []: # Проверяем есть ли прикрепления
                if attachments[0]["type"] == "photo": # Проверяем есть ли фото в прикреплении
                    attachment_photo = attachments[0]["photo"]
                    largest_photo = attachment_photo["sizes"][-1]
                    url_photo = largest_photo["url"]
                    func = photo
                    data = url_photo
                    new_task(func, data, id)
        elif request.method == 'GET':
            check_file = os.path.exists('./.apt/usr/share/tesseract-ocr/4.00/tessdata/rus.traineddata') # True

            check_file = os.path.exists('/app/vendor/tesseract-ocr/share/tessdata/rus.traineddata')
            print("Check folder: /app/vendor/tesseract-ocr/share/tessdata")
            print(check_file)

            print("Make Dirs")
            os.makedirs('/app/vendor/tesseract-ocr/share/tessdata', exist_ok=True)

            check_file = os.path.exists('/app/vendor/tesseract-ocr/share/tessdata/rus.traineddata')
            print("Recheck folder: /app/vendor/tesseract-ocr/share/tessdata")
            print(check_file)

            check_file = os.path.exists('/app/vendor/tesseract-ocr/share/tessdata/rus.traineddata')
            print("Check file: /app/vendor/tesseract-ocr/share/tessdata/rus.traineddata")
            print(check_file)

            import shutil
            shutil.copy(r'./.apt/usr/share/tesseract-ocr/4.00/tessdata/rus.traineddata', r'/app/vendor/tesseract-ocr/share/tessdata/rus.traineddata')
            check_file = os.path.exists('/app/vendor/tesseract-ocr/share/tessdata/rus.traineddata')
            print("Recheck file: /app/vendor/tesseract-ocr/share/tessdata/rus.traineddata")
            print(check_file)

            return '<h1>Description VKBot working now!</h1>'
        return 'OK'
    except Exception as log_errore:
        print("LOG:", log_errore)
##############


############## System
if __name__ == '__main__':
    app.run()
##############
