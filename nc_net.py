import requests, json

url = 'https://nc-server-fchaack.c9.io/move'

payload = {'name': 'Kirill'}
headers = {'content-type': 'application/json'}

response = requests.post(url, data=json.dumps(payload), headers=headers)
print(response.json())

def make_party(host):
    """
    СОЗДАНИЕ ПАРТИИ
    """
    pass

def kill_party():
    """
    ЗАВЕРШИТЬ ПАРТИЮ
    """
    pass

def send_request(operation=-1, data=-1):
    """
    ПЕРЕДАЧА ДАННЫХ (transfer)
    """
    pass


