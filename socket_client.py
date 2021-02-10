import socket 
import webbrowser as ws

HOST = "localhost"
PORT = 9999

socket_client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

socket_client.connect((HOST,PORT))

while True :

	socket_client.sendall(bytes(input(),'utf-8'))
	data = socket_client.recv(1024)
	ws.open(str(data,'utf-8'))

socket_client.shutdown()