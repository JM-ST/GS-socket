import socket


HOST = "localhost"
PORT = 9999

socket_server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)


socket_server.bind((HOST,PORT))


socket_server.listen() 


while True :

	print("waiting for connection")

	connection, client_adress =  socket_server.accept() 

	try:
		print(client_adress)

		while True :

			data = connection.recv(1024)

			if data :
				print("Respond to",client_adress)
				connection.sendall(bytes("google.com/search?q=",'utf-8')+data)
		
		connection.close()

	finally:
		connection.close()
		print("close")


