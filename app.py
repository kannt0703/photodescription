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
from threading import Thread # Thread
from queue import Queue # FIFO

# VKApi
token = str(os.environ.get("TOKEN")) # токен ВК сообщества-бота
confirmation_token = str(os.environ.get("CONFIRMATION_TOKEN")) # код подтверждения CallBack ВК
vk = vk_api.VkApi(token=token, api_version='5.89') # иницилизация ВК Api с токеном и версией Api

# FIFO
queue = Queue() #очередь

# Thread
def completequeue():
    while True:
        try:
            id, url_photo = queue.get()
            vk.method("messages.send", {"peer_id": id, "message": get_result(url_photo), "random_id": random.randint(1, 2147483647)})
        except Exception as log_errore:
            print("LOG_completequeue:", log_errore) # Лог ошибок функции completequeue
complete_queue = Thread(target=completequeue)
complete_queue.start()

#ProxyParse
def get_proxy():
    proxy_site = "http://spys.one/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
        }
    html_url = requests.get(proxy_site, headers=headers)
    tree_html = html.fromstring(html_url.text.encode('UTF-8'))
    tr_elements = tree_html.xpath('//tr[contains(@class, "spy1x")]')
    #Create empty list
    col=[]
    i=0
    #For each row, store each first element (header) and an empty list
    for t in tr_elements[0]:
        i+=1
        name=t.text_content()
        col.append((name,[]))
    #Since out first row is the header, data is stored on the second row onwards
    for j in range(1,len(tr_elements)):
        #T is our j'th row
        T=tr_elements[j]
        #If row is not of size 10, the //tr data is not from our table
        if len(T)!=6:
            break
        #i is the index of our column
        i=0
        #Iterate through each element of the row
        for t in T.iterchildren():
            data=t.text_content()
            #Check if row is empty
            if i>0:
            #Convert any numerical value to integers
                try:
                    data=int(data)
                except:
                    pass
            #Append the data to the empty list of the i'th column
            col[i][1].append(data)
            #Increment i for the next column
            i+=1
    Dict={title:column for (title,column) in col}
    return Dict['IP адрес и порт']

# YandexPars
def get_tags(photo_url):
    yandex_search = "https://yandex.ru/images/search?source=collections&rpt=imageview&rdrnd="+str(random.randint(100000, 999999))+"&redircnt="+str(random.randint(1000000000, 9999999999))+".1&url="+photo_url
    headers = {
        'device-memory': '8',
        'dpr': '1',
        'viewport-width': '1920',
        'rtt': '50',
        'downlink': '2.25',
        'ect': '4g',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
        'Sec-Fetch-Dest': 'document',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-Mode': 'navigate'
        }
    list_of_proxy=get_proxy()
    proxies = { 'http' : 'http://'+list_of_proxy[random.randint(0, len(list_of_proxy)-1)] }
    html_url = requests.get(yandex_search, headers=headers, proxies=proxies) # загрузить страницу запроса
    tree_html = html.fromstring(html_url.text.encode('UTF-8')) # получить html страницы запроса
    tags_tree = tree_html.xpath('//a[contains(@class, "tags__tag")]') # a теги с атрибутом clas равным "..."
    tags = [i.text for i in tags_tree] # преобразовать в текст найденные теги
    return tags

def get_result(photo_url):
    tags = get_tags(photo_url)
    if tags == []: # перепроверка, если нет тегов
        time.sleep(random.randint(1, 2))
        tags = get_tags(photo_url)
        if tags == []: # если второй раз нет тегов
            return "Кажется, на картинке что-то непонятное."
    tags = ", ".join(tags) # формирование списка тегов
    message = "Кажется, на картинке " + tags + "." # формирование сообщения
    return message

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
                        data = (id, url_photo)
                        queue.put(data)
                # ----- Обработка команд -----
                # body = object["text"]
                # if body.lower() == "привет":
                #     vk.method("messages.send", {"peer_id": id, "message": "Привет!", "random_id": random.randint(1, 2147483647)})
                # ----------------------------
            except Exception as log_errore:
                print("LOG_index:", log_errore) # Лог ошибок функции index
    elif request.method == 'GET': # Ответ, если GET запрос (загрузка страницы)
        return '<h1>VKBot working now!</h1>'
    return 'OK' # Постоянный ответ сервера

# Thread
#complete_queue.join()

# FIFO
#queue.join()

# SystemDebug
if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
