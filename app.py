#! /usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from flask import request
from flask import jsonify
from flask_sslify import SSLify
import requests
import json
import os

#Flask
app = Flask(__name__)
sslify = SSLify(app)

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        data = json.loads(request.data)
        if data["type"] == "confirmation":
            return "88feaf44"
    return '<h1>Bot.py working now!</h1>'
#-Flask

if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
#! /usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from flask import request
from flask import jsonify
from flask_sslify import SSLify
import requests
import random
import json
import os

#Flask
app = Flask(__name__)
sslify = SSLify(app)

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        data = json.loads(request.data)
        if data["type"] == "confirmation":
            return "88feaf44"
        elif data["type"] == "message_new":
            object = data["object"]
            id = object["peer_id"]
            body = object["text"]
            if body.lower() == "привет":
                    vk.method("messages.send", {"peer_id": id, "message": "Привет!", "random_id": random.randint(1, 2147483647)})
            elif body.lower() == "тест":
                    vk.method("messages.send", {"peer_id": id, "message": "Тест!", "random_id": random.randint(1, 2147483647)})
            else:
                vk.method("messages.send", {"peer_id": id, "message": "Не понял тебя!", "random_id": random.randint(1, 2147483647)})
    return '<h1>VKBot working now!</h1>'
#-Flask

if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
