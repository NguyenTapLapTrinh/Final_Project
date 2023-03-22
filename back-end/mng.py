import enum
import face_recognition
import socket
import cv2
import time
import sys
import unidecode
sys.path.append("./front-end")
import msg 
class CMD(enum.Enum):
    ADD = 1
    DEL = 2
    EDITPHOTO = 3
    EDITNAME = 4


def sendNewData(file_path,input_employ):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(("192.168.2.103", 5000))
        frame = cv2.imread(file_path)
        embeddings = face_recognition.face_encodings(frame)[0]
        filetosend = open(file_path, "rb")
        Trans = "Send"
        client_socket.send(Trans.encode())
        time.sleep(0.01)
        client_socket.send(input_employ.encode())
        time.sleep(0.01)
        fileExist = client_socket.recv(1024)
        print(fileExist)
        if fileExist == b"Yes":
                msg.ShowMsg("Info","This employee is exitsting!")
        elif fileExist == b"No":
                client_socket.send(input_employ.encode())
                data1 = filetosend.read(1024)
                while data1:
                        client_socket.send(data1)
                        time.sleep(0.01)
                        data1 = filetosend.read(1024)
                filetosend.close()
                string = "Done"
                client_socket.send(string.encode())
                time.sleep(0.01)
                data_string = ""
                for i in embeddings:
                        data_string = data_string + str(i) + "_"
                print(embeddings)
                client_socket.send(data_string.encode())
                time.sleep(0.01)
                print("Done Sending.")
                msg.ShowMsg("Info","Sucessfully")
        client_socket.close()

def deleteData(input_employ):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(("localhost", 5000))
        Trans = "Remove"
        client_socket.send(Trans.encode())
        time.sleep(0.01)
        input_employ = unidecode.unidecode(input_employ)
        client_socket.send(input_employ.encode())
        fileExist = client_socket.recv(1024)
        if fileExist == b"False":
                msg.ShowMsg("Info","Not have this employee!")
                return
        client_socket.send(input_employ.encode())
        client_socket.close()
def editPhoto(file_path, input_employ):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(("localhost", 5000))
        filetosend = open(file_path, "rb")
        Trans = "EditImage"
        client_socket.send(Trans.encode())
        time.sleep(0.01)
        client_socket.send(input_employ.encode())
        time.sleep(0.01)
        fileExist = client_socket.recv(1024)
        print(fileExist)
        if fileExist == b"No":
                msg.ShowMsg("Info","This employee is not existing!")
                return
        elif fileExist == b"Yes":
                client_socket.send(input_employ.encode())
                data1 = filetosend.read(1024)
                while data1:
                        client_socket.send(data1)
                        time.sleep(0.01)
                        data1 = filetosend.read(1024)
                filetosend.close()
                string = "Done"
                client_socket.send(string.encode())
                time.sleep(0.01)
                print("Done Sending.")
                msg.ShowMsg("Info","Sucessfully")
        client_socket.close()
def editName(input_employ, new_name):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(("localhost", 5000))
        Trans = "EditName"
        client_socket.send(Trans.encode())
        time.sleep(0.01)
        client_socket.send(input_employ.encode())
        time.sleep(0.01)
        fileExist = client_socket.recv(1024)
        print(fileExist)
        if fileExist == b"No":
                msg.ShowMsg("Info","This employee is not existing!")
                return
        elif fileExist == b"Yes":
                client_socket.send(new_name.encode())
                time.sleep(0.01)
                print("Done Sending.")
                msg.ShowMsg("Info","Sucessfully")
        client_socket.close()
        