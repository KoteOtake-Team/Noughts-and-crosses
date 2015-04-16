"""
Сетевая составляющая сервера
"""

import sys, socket

HOST = ''
PORT = 15000

def handler(data):
	return str.encode('Hero: %s' % data)


def main():
	s = socket.socket()
	s.bind((HOST, PORT))
	s.listen(2)
	
	conn, addr = s.accept()
	print('connected:', addr)

	while True:
		data = conn.recv(1024)

		print(data.decode())
		if not data: break
		conn.send( handler(data.decode()) )
	conn.close()


if __name__ == '__main__':
	main()