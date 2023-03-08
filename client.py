import socket
import time
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("localhost", 5000))
#file_name = input("Enter file name: ")
file_name = "README.md"
filetosend = open(file_name, "rb")
client_socket.send(file_name)
time.sleep(1)
data = filetosend.read(1024)
while data:
    print("Sending...")
    client_socket.send(data)
    data = filetosend.read(1024)
filetosend.close()
print("Done Sending.")
client_socket.close()