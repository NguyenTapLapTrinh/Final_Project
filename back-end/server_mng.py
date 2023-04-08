import socket
import unidecode
import os
import text
from datetime import datetime
import time
import pickle
BUFFER = 1024
PORT = 5000
IPADRESS = "127.0.0.1"
folder = "temp/"
now = datetime.now()
def setData(client_socket,check_name):
    full_name = check_name
    check_name = unidecode.unidecode(check_name)
    check_img = "Img/worker_img/" + check_name
    existFile = os.path.exists(check_img + ".jpg")
    print(existFile)
    if existFile:
        client_socket.send(b"Yes")
    else:
        client_socket.send(b"No")
        filetodown = open("temp/data.tar", "wb")
        print("Receiving file....")
        while True:
            data = client_socket.recv(BUFFER)
            if data == b"Done":
                break   
            filetodown.write(data) 
        filetodown.close()
        print("Done Reciving...")
        text.writeLine(full_name,check_name)
        #cmd = "tar -xvf temp/data.tar"
        cmd = "tar -xvzf temp/data.tar"
        os.system(cmd)
        # Linux
        # img_path = 'temp/"{}"'.format(check_name + ".jpg")
        # pickle_path = 'temp/"{}"'.format(check_name + ".pickle")
        #Window
        # img_path = '\'.\\temp\\{}\''.format(check_name + ".jpg")
        # pickle_path = './temp/"{}"'.format(check_name + ".pickle")
        # print(img_path)
        # os.system("copy " + img_path + " Img\worker_img")
        # time.sleep(0.5)
        # os.system("copy " + pickle_path + " db/")
        # time.sleep(0.5)
        # os.system("del temp/*")

def deleteData(client_socket,file_name):
    file_remove = file_name
    file_img = "Img/worker_img/" + file_remove
    existFile = os.path.exists(file_img + ".jpg")
    if not existFile:
        client_socket.send(b"False")
    else:
        client_socket.send(b"True")
        text.deleteUser(file_remove)
        os.remove("db/" + file_remove + ".pickle")
        os.remove("Img/worker_img/" + file_remove + ".jpg")

def editName(client_socket,check_name,new_name):
    check_name = unidecode.unidecode(check_name)
    check_img = "Img/worker_img/" + check_name
    existFile = os.path.exists(check_img + ".jpg")
    print(existFile)
    if existFile:
        client_socket.send(b"Yes")
        unidecode_name = unidecode.unidecode(new_name)
        imgPath = "Img/worker_img/"
        picklePath = "db/"
        #Chuyen ten img
        old_name = check_name + ".jpg"
        new_img_name = unidecode_name + ".jpg"
        os.rename(os.path.join(imgPath, old_name), os.path.join(imgPath, new_img_name))
        #Chuyen ten pickle
        old_pickle = check_name + ".pickle"
        new_pickle_name = unidecode_name + ".pickle"
        os.rename(os.path.join(picklePath, old_pickle), os.path.join(picklePath, new_pickle_name))
        text.editUser(check_name, new_name, unidecode_name)
    else:
        client_socket.send(b"No")

def editPhoto(client_socket,check_name):
    check_name = unidecode.unidecode(check_name)
    check_img = "Img/worker_img/" + check_name
    existFile = os.path.exists(check_img + ".jpg")
    print(existFile)
    if existFile:
        client_socket.send(b"Yes")
        unidecode_name = check_name
        file_img = "Img/worker_img/" + unidecode_name
        filetodown = open(file_img + ".jpg", "wb")
        print("Receiving Image....")
        while True:
            data = client_socket.recv(BUFFER)
            if data == b"Done":
                break   
            filetodown.write(data) 
        filetodown.close()
        print("Done Reciving...")
    else:
        client_socket.send(b"No")

def sendCSV(client_socket, file_path):            
    filetosend = open(file_path, "rb")
    data1 = filetosend.read(BUFFER)
    while data1:
            client_socket.send(data1)
            time.sleep(0.01)
            data1 = filetosend.read(BUFFER)
    filetosend.close()
    time.sleep(0.5)
    string = "Done"
    client_socket.send(string.encode())
    client_socket.close()
def sendEmployee(client_socket):
    list_employee = ""    
    with open("db/name.txt", "rb") as file:
        line = file.readlines()
        for i in line:
            i = i.decode()
            i = i.split("_")
            list_employee  = list_employee +str(i[0]) + "-"
    client_socket.send(list_employee.encode())
    client_socket.close()
def sendCurrentCSV(client_socket,time_csv, file_path):
    existFile = os.path.exists("report/report_"+ time_csv + ".csv")
    if existFile:
        msg = "Yes-No"
        check_file = "report/report_"+ time_csv + ".csv"
        if file_path != check_file:
            msg = "Yes-Yes"
        client_socket.send(msg.encode())
        time.sleep(0.01)
        filetosend = open("report/report_"+ time_csv + ".csv", "rb")
        data1 = filetosend.read(BUFFER)
        while data1:
            client_socket.send(data1)
            time.sleep(0.01)
            data1 = filetosend.read(BUFFER)
        filetosend.close()
        time.sleep(0.5)
        string = "Done"
        client_socket.send(string.encode())
        client_socket.close()
        print("Done...")
    else:
        client_socket.send(b"No")