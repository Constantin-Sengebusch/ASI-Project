#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask
from flask import request
from flask import Response
import requests
import main_script as ms
import json
import os

curr_path = os. getcwd()

with open(f'{curr_path}/config_credentials.json', 'r') as f:
    config_credentials = json.load(f)

TOKEN = config_credentials['telegram']
app = Flask(__name__)
 
def parse_message(message):
    print("message-->",message)
    chat_id = message['message']['chat']['id']
    txt = message['message']['text']
    print("chat_id-->", chat_id)
    print("txt-->", txt)
    return chat_id,txt
 
def tel_send_message(chat_id, text):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    payload = {
                'chat_id': chat_id,
                'text': text
                }
   
    r = requests.post(url,json=payload)
    return r
 
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        msg = request.get_json()
        print(msg)
	
        chat_id,txt = parse_message(msg)

        tel_send_message(chat_id, ms.mainScript(txt))
       
        return Response('ok', status=200)
    else:
        return "<h1>Welcome!</h1>"
 
if __name__ == '__main__':
   app.run(debug=True)