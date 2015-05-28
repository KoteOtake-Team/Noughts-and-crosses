import json
import requests
from time import sleep


class Client:

    URL = 'https://nc-server-fchaack.c9.io'
    HTTP_HEADERS = {'Content-type': 'application/json', 'Accept': 'text/plain'}

    def __init__(self):
        self.id = None
        self.room_id = None
        self.turn = None

    def __request(self, action, payload=dict()):
        url = self.URL + action
        h = self.HTTP_HEADERS

        if payload:
            payload = json.dumps(payload)
            response = requests.post(url, headers=h, data=payload)
        else:
            response = requests.post(url, headers=h)

        return response.json.json()  # get json object then get data

    def get_data_about_client(self):
        return {
            'id': self.id,
            'battle': self.room_id,
            'turn': self.turn,
        }

    def connect_to_server(self):
        """
        Connect with server
        update -> client_id
        :return True if success else False
        """
        action = '/connect'
        payload = self.get_data_about_client()

        response = self.__request(action, payload=payload)
        result = response['id']

        if result:
            self.id = result
            return True
        else:
            return False

    def close_connection(self):
        self.id = None
        self.room_id = None
        self.turn = None

    def get_enemy(self):
        """
        Search the Enemy!
        update -> battle_id
        :return True if success else False
        """
        if self.id:
            action = '/enemy'
            payload = self.get_data_about_client()

            while True:
                sleep(0.1)
                response = self.__request(action, payload=payload)

                if response['room_id'] and response['turn']:
                    self.room_id = response['room_id']
                    self.turn = int(response['turn'])
                    return True
        else:
            return False

    def send_request(self, string):
        """
        Send request to server.
        :return True if success else False
        """
        if self.id and self.room_id:
            action = "/%s/req" % self.room_id
            payload = {
                'client_id': self.id,
                'data': string,
            }

            self.__request(action, payload=payload)

            return True
        else:
            return False

    def get_response(self, time=1):
        """
        Get response from server.
        :return string or False if something failure
        """
        if self.id and self.room_id:
            action = "/%s/res" % self.room_id
            time *= 600  # changing time for sleep

            for _ in range(time):
                sleep(0.1)
                response = self.__request(action)
                if response:
                    return response['data']
            self.room_id = None
            self.turn = None

            return False

        else:
            return False


if __name__ == '__main__':
    # 1)create a new instance of client!
    kirill = Client()

    # 2)connect to server!
    kirill.connect_to_server()
    # after 2 step we get user id
    print(kirill.get_data_about_client())

    # 3)search the human or enemy or Nikita's cats
    kirill.get_enemy()
    # after 3 step we get room's id and your turn!!!!
    print(kirill.get_data_about_client())

    # 5) Now our action dependent on turn
    if kirill.turn == 0:
        # Sending request
        kirill.send_request('Hey MAAAAN!!!!')
        print(kirill.get_response())
    else:
        print(kirill.get_response())
        kirill.send_request('Hey MAAAAN!!!!')

    # 6) after game
        kirill.close_connection()
