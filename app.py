#! /usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from flask import request
from flask import jsonify
import requests
import json

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
