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



def make_party(data):
    """
    СОЗДАНИЕ ПАРТИИ
    """
    pass

def kill_party(data):
    """
    ЗАВЕРШИТЬ ПАРТИЮ
    """
    pass

def transfer(data):
    """
    ПЕРЕДАЧА ДАННЫХ
    Функция отправляет данные на сервер, где они обрабатываются. Затем возвращается ответ
    nc_net.transfer() -> nc_server_net -> nc_server_logic.recieve() -> nc_server_net -> nc_net.transfer()
    """

    # временный код для локального тестирования
    import nc_server_logic
    nc_server_logic.recieve(data)


def main():
    client = Client()
    while True:
        data = input('type->>')
        if not data: break
        client.send(data)
        print(client.get_response())


if __name__ == '__main__':
    main()