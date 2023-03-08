import socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setblocking(0)
server_socket.settimeout(3)
server_socket.bind(("localhost", 5000))
server_socket.listen(1)
client_socket,a = server_socket.accept()
file_name = client_socket.recv(1024)
filetodown = open("file_name.md", "wb")
while True:
	print("Receiving....")
	data = client_socket.recv(1024)
	if len(data) == 0:
		break
	filetodown.write(data)

	
filetodown.close()

server_socket.shutdown(2)
server_socket.close()
