# -*- coding: utf-8 -*-
import time
import requests, json

#  Настройки
URL = 'https://nc-server-fchaack.c9.io'
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

def get_url():
    return URL


# Данные о клиенте
client_id = None
battle_id = None

def get_data_about_client():
    return {'id': client_id, 'battle': battle_id}


# Функции для передачи данныx
def request(url, payload={}):
    if payload:
        payload = json.dumps(payload)
        response = requests.post(url, headers=headers, data=payload)
    else:
        response = requests.post(url, headers=headers)

    return response.json



def connect_to_server():
    """
    Соединяемся с сервером.
    update -> client_id
    """
    url = get_url() + '/connect'
    response = request(url, payload=get_data_about_client())
    global client_id
    client_id = response.json()['id']


def get_enemy():
    """
    Отправляем серверу наши данные для поиска соперника.
    update -> battle_id
    """
    url = get_url() + '/enemy'
    data = get_data_about_client()
    while True:
        time.sleep(0.1)
        response = request(url, payload=data)
        if response: return response


def send_request(data):
    """
    Отправить запрос серверу.
    data = {key: value, ...}
    return -> {'message': value}
    """
    url = get_url() + '/req'
    response = request(url, payload=data.update(get_data_about_client())
    return response


def get_response(time=1):
    """
    time - время ожидания ответа в минутах
    Получить ответ сервера.
    return -> {'message': value, key: value, ...}
    """
    time *= 600
    wait = 0.1
    url = get_url() + '/res'
    for i in range(time):
        time.sleep(wait)
        response = request(url)
        if response: return response
