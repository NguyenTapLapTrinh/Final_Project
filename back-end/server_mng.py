import socket
import unidecode
import os
import text
import time
from define import Socket, Time, Platform


def createSocket(ip_adress,port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #server_socket.setblocking(1)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    ip = ip_adress
    print(ip + "     "+ str(port))
    server_socket.bind((ip, port))
    return server_socket

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
            data = client_socket.recv(Socket.BUFFER.value)
            if data == b"Done":
                break   
            filetodown.write(data) 
        filetodown.close()
        print("Done Reciving...")
        text.writeLine(full_name,check_name)
        if  Platform.SYSTEM.value == 'Linux':
            cmd = "tar -xvf temp/data.tar"
            os.system(cmd)
            img_path = 'temp/"{}"'.format(check_name + ".jpg")
            pickle_path = 'temp/"{}"'.format(check_name + ".pickle")
            os.system("cp " + img_path + " Img/worker_img")
            os.system("cp " + pickle_path + " db")
            os.system("rm temp/*")
        else:
            cmd = "tar -xvzf temp/data.tar"
            os.system(cmd)
            img_path = '\'.\\temp\\{}\''.format(check_name + ".jpg")
            pickle_path = './temp/"{}"'.format(check_name + ".pickle")
            # print(img_path)


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
            data = client_socket.recv(Socket.BUFFER.value)
            if data == b"Done":
                break   
            filetodown.write(data) 
        filetodown.close()
        print("Done Reciving...")
    else:
        client_socket.send(b"No")

def sendCSV(client_socket, file_path):           
    filetosend = open(file_path, "rb")
    data1 = filetosend.read(Socket.BUFFER.value)
    while data1:
            client_socket.send(data1)
            data1 = filetosend.read(Socket.BUFFER.value)
    filetosend.close()
    time.sleep(Time.TIME_SLEEP_500MS.value)
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
        time.sleep(Time.TIME_SLEEP_10MS.value)
        filetosend = open("report/report_"+ time_csv + ".csv", "rb")
        data1 = filetosend.read(Socket.BUFFER.value)
        while data1:
            client_socket.send(data1)
            time.sleep(Time.TIME_SLEEP_10MS.value)
            data1 = filetosend.read(Socket.BUFFER.value)
        filetosend.close()
        time.sleep(Time.TIME_SLEEP_500MS.value)
        string = "Done"
        client_socket.send(string.encode())
        client_socket.close()
        print("Done...")
    else:
        client_socket.send(b"No")

def mainServer(file_path,server_socket):
    server_socket.listen(Socket.WAITLIST.value)
    client_socket,a = server_socket.accept()
    message = client_socket.recv(Socket.BUFFER.value)
    message = message.decode()
    request = message.split("-")

    if request[0] == "Send":
        setData(client_socket,request[1])
    elif request[0] == "Remove":
        deleteData(client_socket,request[1])
    elif request[0] == "EditImage":
        editPhoto(client_socket,request[1])
    elif request[0] == "EditName":
        editName(client_socket,request[1],request[2])
    elif request[0] == "UpdateCSV":
        sendCSV(client_socket, file_path)
    elif request[0] == "LoadCSV":
        sendCurrentCSV(client_socket,request[1]+ "-" +request[2]+ "-" +request[3], file_path)
    elif request[0] == "ListEmployee":
        sendEmployee(client_socket)


