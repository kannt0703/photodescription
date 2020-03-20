#! /usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from flask import request
from flask import jsonify
import requests
import json
from flask_sslify import SSLify


app = Flask(__name__)
sslify = SSLify(app)

#Flask
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        r = request.get_json()
    elif request.method == 'GET':
        return '<h1>VKBot working now!</h1>'
#-Flask

if __name__ == '__main__':
    app.run()
