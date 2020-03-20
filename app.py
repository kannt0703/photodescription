#! /usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, request, json

import vk_api
import random

vk = vk_api.VkApi(token="dafd425228fbc59657b126eaba4c2530f4781af8a9ccbb53639c7a0dbc09db5670daf8cd8529297223658")

app = Flask(__name__)

@app.route('/', methods = ["POST"])
def main():
    data = json.loads(request.data)
    if data["type"] == "confirmation":
        return "88feaf44"
    elif data["type"] == "message_new":
        object = data["object"]
        id = object["peer_id"]
        body = object["text"]
        if body.lower() == "привет":
                vk.method("messages.send", {"peer_id": id, "message": "Привет!", "random_id": random.randint(1, 2147483647)})
        elif body.lower() == "я не подписан на канал it things":
                vk.method("messages.send", {"peer_id": id, "message": "Казнить грешника!", "random_id": random.randint(1, 2147483647)})
        else:
            vk.method("messages.send", {"peer_id": id, "message": "Не понял тебя!", "random_id": random.randint(1, 2147483647)})
    return "ok"

if __name__ == '__main__':
    app.run()
