import socket
import os


BUFFLEN = 4096 * 4096 # 16KB
class Server:

	def __init__(self,host='localhost',port=2000):
		self.host = host 
		self.port = port 
		try:
			self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
			self.socket.bind((host,port))
			self.socket.listen(4)
			self.running = True
			print(f"Listening on port {port}")
		except Exception as e:
			print(e)


	def handleConnection(self,connection,address):
		print(address[0],"CONNECTED")

		try:
			remote_cwd = connection.recv(BUFFLEN).decode()
			

			while self.running:
				command = input(remote_cwd+'> ')
				if command == '':
					continue

				connection.sendall(command.encode())

				if command == 'exit' or command == 'quit':
					break;

				data = connection.recv(BUFFLEN).decode()

				stdout,remote_cwd = data.split("<-->")
				print(stdout)
		except Exception as e:
			print(e)


	def mainloop(self):
		connection , address = self.socket.accept()
		self.handleConnection(connection,address)

	def __del__(self):
		self.socket.close()

Server().mainloop()