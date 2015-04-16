"""
Сетевая составляющая клиента
"""

import sys, socket

HOST = 'localhost'
PORT = 15000

s = socket.socket()
s.connect((HOST, PORT))

while True:
	data = input('type:')
	if not data: break
	s.send(str.encode(data))

	result = s.recv(1024)
	print(result.decode())

s.close()