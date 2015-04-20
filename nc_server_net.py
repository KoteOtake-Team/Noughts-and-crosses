import sys, socket


HOST = ''
PORT = 4444

class Server:

	def __init__(self):
		self.settings = HOST, PORT
		self.socket = socket.socket()
		self.socket.bind(self.settings)

	def _handle_data(self, data):
		return data + '- Hey! maaaan! thats cool'

	def start(self):
		self.socket.listen(2)
		self.conn, self.addr = self.socket.accept()
		print('connected->>', self.addr)
		while True:
			data = self.conn.recv(128)
			if not data: break
			print('from ',self.addr,'get:',data)
			self.conn.send(self._handle_data(data))

	def stop(self):
		self.conn.close()


def main():
	server = Server()
	server.start()
	server.stop()


if __name__ == '__main__':
	main()