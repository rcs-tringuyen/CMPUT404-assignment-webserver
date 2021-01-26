#  coding: utf-8 
import socketserver
import os

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
	
	def handle(self):
		
		self.data = self.request.recv(1024).strip()
		#print ("Got a request of: %s\n" % self.data)

		headers = self.data.decode("utf-8").split(' ')

		method = headers[0]
		path = headers[1]

		if method == 'GET':
			try:
				path_rel = os.path.abspath(os.getcwd())+'/www'+os.path.normpath(path)
				if os.path.isdir(path_rel):
					if path[-1] != '/':
						response = f'HTTP/1.1 301 Moved Permanently\r\nContent-Type: text/html\r\nLocation: {path}/\r\n\n\n'
						self.request.sendall(bytearray(response, 'utf-8'))
				elif not(os.path.isfile(path_rel)):
					message = """
					<html>
					<head><title>404 Not Found</title></head>
					<body><h1>404 Not Found</h1><p>The page you're looking for does not exist.</p></body>
					</html>"""

					response = f'HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\nContent-Length: {len(message)}\r\n\r\n\r\n{message}'
					self.request.sendall(bytearray(response, 'utf-8'))



				if path.endswith('/'):
					index = open(f'./www{path}/index.html', 'r')
					index_r = index.read()
					response = f'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Lengt: {len(index_r)}\r\n\r\n{index_r}'
					self.request.sendall(bytearray(response, 'utf-8'))

				if path.endswith('.html') or path.endswith('.css'):
					file = open(f'./www{path}','r')
					file_r = file.read()
					file_extension = path[path.rfind('.')+1:len(path)]
					response = f'HTTP/1.1 200 OK\r\nContent-Type: text/{file_extension}\r\nContent-Length: {len(file_r)}\r\n\r\n{file_r}'
					self.request.sendall(bytearray(response, 'utf-8'))

			except Exception as e:
				#file not found
				if e.errno == 2:
					message = """
					<html>
					<head><title>404 Not Found</title></head>
					<body><h1>404 Not Found</h1><p>The page you're looking for does not exist.</p></body>
					</html>"""

					response = f'HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\nContent-Length: {len(message)}\r\n\r\n\r\n{message}'
					self.request.sendall(bytearray(response, 'utf-8'))

				else:
					print(e)

		elif method != 'GET':
			message = """
			<html>
			<head><title>405 Method Not Allowed</title></head>
			<body><h1>405 Method Not Allowed</h1><p>Method Not Allowed</p></body>
			</html>"""

			response = f'HTTP/1.1 405 Method Not Allowed\r\nContent-Type: text/html\r\nContent-Length= {len(message)}\r\n\r\n{message}'
			self.request.sendall(bytearray(response, 'utf-8'))

if __name__ == "__main__":
	HOST, PORT = "localhost", 8080

	socketserver.TCPServer.allow_reuse_address = True
	# Create the server, binding to localhost on port 8080
	server = socketserver.TCPServer((HOST, PORT), MyWebServer)

	# Activate the server; this will keep running until you
	# interrupt the program with Ctrl-C
	server.serve_forever()
