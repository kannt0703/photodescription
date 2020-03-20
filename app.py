#! /usr/bin/env python
# -*- coding: utf-8 -*-

from tabulate import tabulate
from flask import Flask
from flask import request
from flask import jsonify
import requests
import json
import io
app = Flask(__name__)
sslify = SSLify(app)

#Flask
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        r = request.get_json()
        return jsonify(r)
    return '<h1>Bot.py working now!</h1>'
#-Flask

if __name__ == '__main__':
    app.run()
