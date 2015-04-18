"""
Сетевая составляющая клиента
"""

import sys, socket

HOST = 'localhost'
PORT = 15000



def transfer(**kwargs):
    """
    ПЕРЕДАЧА ДАННЫХ
    Функцию использует nc_logic для передачи ЛЮБЫХ данных на сервер
    Возращает:
    булево значение:
    -True - в случае удачи
    -False - в случае провала в передаче данных
    """
    return True

s = socket.socket()
s.connect((HOST, PORT))

while True:
	data = input('type:')
	if not data: break
	s.send(str.encode(data))

	result = s.recv(1024)
	print(result.decode())

s.close()