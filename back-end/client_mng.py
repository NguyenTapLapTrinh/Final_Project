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
import subprocess

BUFFER = 1024
PORT = 5000
IPADRESS = "192.168.1.202"
TIMEOUT  = 1
folder = "temp/"

def get_ip_address():
    global IPADRESS
    # Execute the 'arp -a' command to get the ARP cache entries
    cmd = 'arp -a | findstr "40-1c-83-80-e1-ca" '
    returned_output = subprocess.check_output((cmd),shell=True,stderr=subprocess.STDOUT).decode()
    lines = returned_output.strip().split("\n")
    for line in lines:
        if "40-1c-83-80-e1-ca" in line.lower():
            parse=str(returned_output).split(' ',1)
            ip=parse[1].split(' ')
            IPADRESS = ip[1]
            return ip[1]
    return None

class CMD(enum.Enum):
    ADD = 1
    DEL = 2
    EDITPHOTO = 3
    EDITNAME = 4
def checkResponding(client_socket):
        try:
                client_socket.connect((IPADRESS, PORT))
        except socket.error:
                msg.ShowMsg("Warning","Server not responding")
                return 0
def ReceiveData(client_socket):
        try:
                data = client_socket.recv(BUFFER)
                return data
        except socket.error:
                msg.ShowMsg("Warning","Lost connection with server")
                return 0
def setData(file_path, input_employ):
        frame = cv2.imread(file_path)
        try:
                embeddings = face_recognition.face_encodings(frame)[0]
        except:
                msg.ShowMsg("Info","Person not found!") 
                return

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.settimeout(TIMEOUT)
        check = checkResponding(client_socket)
        if check==0:
                return 0
        Trans = "Send"
        message = Trans + "-" + input_employ
        client_socket.send(message.encode())
        time.sleep(0.01)
        fileExist = ReceiveData(client_socket)
        if fileExist == 0:
                return
        if fileExist == b"Yes":
                msg.ShowMsg("Info","This employee is exitsting!")
        elif fileExist == b"No":
                unidecode_name = unidecode.unidecode(input_employ)
                img_path_temp = folder + unidecode_name + ".jpg" 
                cv2.imwrite(img_path_temp,frame)

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
                # os.remove(img_path_temp)
                # os.remove(pickle_path_temp)
                # os.remove("temp/data.tar")
                msg.ShowMsg("Info","Sucessfully")
        client_socket.close()
        return 1
def deleteData(input_employ):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.settimeout(TIMEOUT)
        check = checkResponding(client_socket)
        if check==0:
                return 0
        Trans = "Remove"
        input_employ = unidecode.unidecode(input_employ)
        message = Trans + "-" + input_employ
        client_socket.send(message.encode())
        fileExist = ReceiveData(client_socket)
        if fileExist == b"False":
                msg.ShowMsg("Info","Not have this employee!")
        else:
            msg.ShowMsg("Info","Sucessfully")    
        client_socket.close()
        return 1
def editPhoto(file_path, input_employ):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.settimeout(TIMEOUT)
        check = checkResponding(client_socket)
        if check==0:
                return 0
        filetosend = open(file_path, "rb")
        Trans = "EditImage"
        message = Trans + "-" + input_employ
        client_socket.send(message.encode())
        fileExist = ReceiveData(client_socket)
        if fileExist==0:
                return
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
        return 1
def editName(input_employ, new_name):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.settimeout(TIMEOUT)
        check = checkResponding(client_socket)
        if check==0:
                return 0
        Trans = "EditName"
        message = Trans + "-" + input_employ + "-" + new_name
        client_socket.send(message.encode())
        time.sleep(0.01)
        fileExist = ReceiveData(client_socket)
        if fileExist == 0:
                return
        print(fileExist)
        if fileExist == b"No":
                msg.ShowMsg("Info","This employee is not existing!")
        elif fileExist == b"Yes":
                print("Done Sending.")
                msg.ShowMsg("Info","Sucessfully")
        client_socket.close()
        return 1
def UpdateCSV():
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.settimeout(TIMEOUT)
        check = checkResponding(client_socket)
        if check==0:
                return 0
        Trans = "UpdateCSV"
        message = Trans + "-" 
        client_socket.send(message.encode())
        time.sleep(0.01)
        filetodown = open("CLIENT/csv_file/now_csv.csv", "wb")
        while True:
                data = ReceiveData(client_socket)
                if data == 0:
                        return
                if data == b"Done":
                        break   
                filetodown.write(data) 
        filetodown.close()
        print("Done Reciving...")
        return 1
def RequestEmployee():
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.settimeout(TIMEOUT)
        check = checkResponding(client_socket)
        if check==0:
                return -1
        Trans = "ListEmployee"
        message = Trans + "-" 
        list_data = ""
        client_socket.send(message.encode())
        time.sleep(0.01)
        list_data = ReceiveData(client_socket)
        if list_data == 0:
                return
        list_data = list_data.decode()
        data_string = list_data.split("-")
        print("Done Reciving Employee...")
        client_socket.close()
        return data_string
def receiveCSV(time_csv):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.settimeout(TIMEOUT)
        check = checkResponding(client_socket)
        if check==0:
                return -1
        Trans = "LoadCSV"
        message = Trans + "-" + time_csv
        client_socket.send(message.encode())
        time.sleep(0.01)
        fileExist = ReceiveData(client_socket)
        if fileExist == 0:
                return
        fileExist = fileExist.decode()
        fileExist = fileExist.split("-")
        time.sleep(0.01)
        if fileExist[0] == "No":
                msg.ShowMsg("Warning","This CSV not exits")
                return 1
        elif fileExist[0] == "Yes":
                filetodown = open("CLIENT/csv_file/current_csv.csv", "wb")
                while True:
                        data = ReceiveData(client_socket)
                        if data == b"Done":
                                break   
                        filetodown.write(data) 
                filetodown.close()
                print("Done Reciving...")
                if fileExist[1] == "Yes":
                        return 1
                else: 
                        return 0