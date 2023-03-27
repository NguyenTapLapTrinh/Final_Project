import enum
import face_recognition
import socket
import cv2
import time
import sys
import unidecode
import os
import pickle
sys.path.append("./front-end")
import msg 

BUFFER = 1024
PORT = 5000
IPADRESS = "127.0.0.1"
folder = "temp/"

class CMD(enum.Enum):
    ADD = 1
    DEL = 2
    EDITPHOTO = 3
    EDITNAME = 4


def setData(file_path,input_employ):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((IPADRESS, PORT))
        Trans = "Send"
        message = Trans + "-" + input_employ
        client_socket.send(message.encode())
        time.sleep(0.01)
        fileExist = client_socket.recv(BUFFER)
        if fileExist == b"Yes":
                msg.ShowMsg("Info","This employee is exitsting!")
        elif fileExist == b"No":
                frame = cv2.imread(file_path)

                unidecode_name = unidecode.unidecode(input_employ)
                img_path_temp = folder + unidecode_name + ".jpg" 
                cv2.imwrite(img_path_temp,frame)

                embeddings = face_recognition.face_encodings(frame)[0]
                pickle_path_temp = folder + unidecode_name +".pickle"

                with open(pickle_path_temp, "wb") as file:
                        pickle.dump(embeddings, file)
                cmd = 'tar -czf temp/data.tar "{}" "{}"'.format(img_path_temp,pickle_path_temp)
                os.system(cmd)

                filetosend = open("temp/data.tar", "rb")
                data1 = filetosend.read(BUFFER)
                while data1:
                        client_socket.send(data1)
                        time.sleep(0.01)
                        data1 = filetosend.read(BUFFER)
                filetosend.close()
                time.sleep(0.5)
                string = "Done"
                client_socket.send(string.encode())
                os.remove(img_path_temp)
                os.remove(pickle_path_temp)
                os.remove("temp/data.tar")
                msg.ShowMsg("Info","Sucessfully")
        client_socket.close()

def deleteData(input_employ):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((IPADRESS, PORT))
        Trans = "Remove"
        input_employ = unidecode.unidecode(input_employ)
        message = Trans + "-" + input_employ
        client_socket.send(message.encode())
        fileExist = client_socket.recv(BUFFER)
        if fileExist == b"False":
                msg.ShowMsg("Info","Not have this employee!")
        else:
            msg.ShowMsg("Info","Sucessfully")    
        client_socket.close()

def editPhoto(file_path, input_employ):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((IPADRESS, PORT))
        filetosend = open(file_path, "rb")
        Trans = "EditImage"
        message = Trans + "-" + input_employ
        client_socket.send(message.encode())
        fileExist = client_socket.recv(BUFFER)
        if fileExist == b"No":
                msg.ShowMsg("Info","This employee is not existing!")
        elif fileExist == b"Yes":
                data1 = filetosend.read(BUFFER)
                while data1:
                        client_socket.send(data1)
                        time.sleep(0.01)
                        data1 = filetosend.read(BUFFER)
                filetosend.close()
                string = "Done"
                client_socket.send(string.encode())
                time.sleep(0.01)
                msg.ShowMsg("Info","Sucessfully")
        client_socket.close()
        
def editName(input_employ, new_name):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((IPADRESS, PORT))
        Trans = "EditName"
        message = Trans + "-" + input_employ + "-" + new_name
        client_socket.send(message.encode())
        time.sleep(0.01)
        fileExist = client_socket.recv(BUFFER)
        print(fileExist)
        if fileExist == b"No":
                msg.ShowMsg("Info","This employee is not existing!")
        elif fileExist == b"Yes":
                print("Done Sending.")
                msg.ShowMsg("Info","Sucessfully")
        client_socket.close()
        