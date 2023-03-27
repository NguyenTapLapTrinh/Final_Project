import socket
import unidecode
import os
import text

BUFFER = 1024
PORT = 5000
IPADRESS = "127.0.0.1"
folder = "temp/"

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
        cmd = "tar -xvf temp/data.tar"
        os.system(cmd)
        img_path = 'temp/"{}"'.format(check_name + ".jpg")
        pickle_path = 'temp/"{}"'.format(check_name + ".pickle")
        os.system("cp " + img_path + " Img/worker_img")
        os.system("cp " + pickle_path + " db/")
        os.system("rm temp/*")

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