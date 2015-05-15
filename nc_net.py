import time
import requests, json

url = 'https://nc-server-fchaack.c9.io'
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

my_key = ''
enemy_key = ''


def simple_test(req_f):
    def test(args, act=''):
        print('action:', act)
        print('request:',args)
        return req_f(args)
    return test

@simple_test
def send_request(data, act=''):
    """
    data must be dictionary
    """
    global url

    url_with_act = url + act
    print(url + act)
    payload = json.dumps(data)
    response = requests.post(url_with_act, headers=headers, data=payload)
    return response.json()


def start():
    global my_key,  enemy_key

    connect = send_request({'message': 'I want to connect'})
    if connect['key']:
        my_key = connect['key']

    while True:
        get_enemy = send_request({'message': 'give me Enemy!'}, act='/search_enemy')
        print(get_enemy)
        if get_enemy:
            enemy_key = get_enemy['enemy_key']
            break
        time.sleep(1)



if __name__ == '__main__':
    start()
    print(key)
    print()

