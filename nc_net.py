import sys, socket

HOST = 'localhost'
PORT = 4444


class Client:

    def __init__(self):
        self.settings = HOST, PORT
        self.socket = socket.socket()
        self.socket.connect(self.settings)

    def send(self, data):
        self.socket.send(data)

    def get_response(self):
        return self.socket.recv(128)

    def stop(self):
        self.socket.close()



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

def transfer(operation=-1, data=-1):
    """
    ПЕРЕДАЧА ДАННЫХ
    """
    pass


def main():
    client = Client()
    while True:
        data = input('type->>')
        if not data: break
        client.send(data)
        print(client.get_response())


if __name__ == '__main__':
    main()