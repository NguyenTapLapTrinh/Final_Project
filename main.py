import sys
sys.path.append("./back-end")
sys.path.append("./front-end")
sys.path.append("./admin_gui")
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import cv2
from time import *
import os
import datetime
import report
import texttospeed as ts
import util
import worker
import camera
import yolo_detection
import info
import threading
import pickle
import socket
import admin
import unidecode
import text
import mng
classes_vn = ["Mũ bảo hiểm", "Áo bảo hộ", "Găng tay bảo hộ"]
classes = []
number = 1

with open("coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]

months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

yolo = yolo_detection.Yolo(classes)
yolo.loadWeight("weight/yolov4_training_last.weights","weight/yolov4_testing.cfg")

def closeWidget():
    widget_2.close()

def updateWidget(note,name,unicode_name,time,date,empty):
    Form_2.updateResult(note)
    Form_2.updateName(unicode_name)
    Form_2.updateTime(time)
    Form_2.updateDate(date)
    Form_2.updateHelmet(0)
    Form_2.updateVest(0)
    Form_2.updateGlove(0)
    Form_2.updateWorkerPhoto(name)
    for i in empty:
        if i == 0:
            Form_2.updateHelmet(1)
        elif i == 1:
            Form_2.updateVest(1)
        elif i == 2:
            Form_2.updateGlove(1)

def button():
    global number
    time_now = datetime.datetime.now().time()
    time_str = time_now.strftime("%H:%M:%S")
    frame_process = yolo.getFrame()
    empty = yolo.objectDetect()
    try:
        name = util.recognize(frame_process, './db')
    except:
        print("False")
        return
    if name == "no_persons_found":
        dlg = QMessageBox()
        dlg.setIcon(QMessageBox.Warning)
        dlg.setText("No person found!   ")
        dlg.setWindowTitle("            Info          ")
        dlg.setStandardButtons(QMessageBox.Ok)
        dlg.exec()
        return
    full_name = text.findFullName(name)
    find,note = report.edit_report(file_path,full_name,time_str,empty)
    if not find: 
        note = report.write_report(file_path,str(number),full_name,time_str,empty)
    number +=1
    string = "có đầy đủ bảo hộ"
    leng = len(empty)
    if leng > 0:
        string = "Không có "
        for i in empty:
            string = string + classes_vn[i] + " "
            if leng > 1:
                string += "và "
                leng -= 1
    updateWidget(note,name,full_name,time_str,date_str,empty)
    widget_2.show()
    ts.start_sound(string,full_name+" ")    
#Thread
def ThreadServer():
    while True:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #server_socket.setblocking(1)
        
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(("localhost", 5000))
        server_socket.listen(1)
        client_socket,a = server_socket.accept()
        #server_socket.settimeout(3)
        request_data = client_socket.recv(1024)
        request = request_data.decode()
        print(request)
        if request == "Send":
            check_name = client_socket.recv(1024)
            check_name = check_name.decode()
            check_name = unidecode.unidecode(check_name)
            check_img = "Img/worker_img/" + check_name
            existFile = os.path.exists(check_img + ".jpg")
            print(existFile)
            if existFile:
                client_socket.send(b"Yes")
            else:
                client_socket.send(b"No")
                file_name = client_socket.recv(1024)
                file_name = file_name.decode()
                unidecode_name = unidecode.unidecode(file_name)
                file_img = "Img/worker_img/" + unidecode_name
                filetodown = open(file_img + ".jpg", "wb")
                print("Receiving Image....")
                while True:
                    data = client_socket.recv(1024)
                    if data == b"Done":
                        break   
                    filetodown.write(data) 
                filetodown.close()
                list_data = []
                print("Receiving Pickle...")
                data = client_socket.recv(4096)
                data = data.decode()
                data = data.split("_")
                data.remove('')
                for i in data:
                    i = float(i)
                    list_data.append(i)
                print(list_data)
                with open("db/" + unidecode_name +".pickle", "wb") as file:
                    pickle.dump(list_data, file)
                text.writeLine(file_name,unidecode_name)
                print("Done Reciving...")
            
        #server_socket.shutdown(2)
        elif request == "Remove":
            file_name = client_socket.recv(1024)
            file_remove = file_name.decode()
            file_img = "Img/worker_img/" + file_remove
            existFile = os.path.exists(file_img + ".jpg")
            if not existFile:
                client_socket.send(b"False")
            else:
                client_socket.send(b"True")
                text.deleteUser(file_remove)
                os.remove("db/" + file_remove + ".pickle")
                sleep(0.01)
                os.remove("Img/worker_img/" + file_remove + ".jpg")
        elif request == "EditImage":
            check_name = client_socket.recv(1024)
            check_name = check_name.decode()
            check_name = unidecode.unidecode(check_name)
            check_img = "Img/worker_img/" + check_name
            existFile = os.path.exists(check_img + ".jpg")
            print(existFile)
            if existFile:
                client_socket.send(b"Yes")
                file_name = client_socket.recv(1024)
                file_name = file_name.decode()
                unidecode_name = unidecode.unidecode(file_name)
                file_img = "Img/worker_img/" + unidecode_name
                filetodown = open(file_img + ".jpg", "wb")
                print("Receiving Image....")
                while True:
                    data = client_socket.recv(1024)
                    if data == b"Done":
                        break   
                    filetodown.write(data) 
                filetodown.close()
                print("Done Reciving...")
            else:
                client_socket.send(b"No")
        elif request == "EditName":
            check_name = client_socket.recv(1024)
            check_name = check_name.decode()
            check_name = unidecode.unidecode(check_name)
            check_img = "Img/worker_img/" + check_name
            existFile = os.path.exists(check_img + ".jpg")
            print(existFile)
            if existFile:
                client_socket.send(b"Yes")
                new_name = client_socket.recv(1024)
                new_name = new_name.decode()
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
                print(check_name + " " +new_name + " " +unidecode_name)
                text.editUser(check_name, new_name, unidecode_name)
            else:
                client_socket.send(b"No")
        server_socket.close()
if os.path.exists("report"):
    pass
else:
    os.mkdir("report")

db_dir = './db'
if not os.path.exists(db_dir):
    os.mkdir(db_dir)

if os.path.exists("./db/name.txt"):
    pass
else:
     with open("db/name.txt", "wb") as file:
        pass

cap = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_COMPLEX_SMALL

#FPS
start_time = time()
display_time = 2
fc = 0
FPS = 0

thread = threading.Thread(target=ThreadServer)
thread.start()

#Show Gui
app = QtWidgets.QApplication(sys.argv)
widget_1 = QtWidgets.QWidget()
Form_1 = worker.Ui_Form()
Form_1.setupUi(widget_1)
Form_1.ButtonActivation(button)
widget_1.show()

widget_2 = QtWidgets.QWidget()
widget_3 = QtWidgets.QWidget()
Form_2 = info.Ui_Form()
Form_2.setupUi(widget_2)
Form_3 = admin.Ui_Form()
Form_3.setupUi(widget_3)
Form_2.ButtonActivation(closeWidget)

text.editUser("Son Tung","Nguyễn Thanh Tùng","Nguyen Thanh Tung")
while True:
    _, frame = cap.read()
    #frame = cv2.imread("Img/data_test/SonTung.jpg")
    height, width, channels = frame.shape
 
    yolo.setVar(frame,width,height)

    fc+=1
    TIME = time() - start_time
    if (TIME) >= display_time :
        FPS = fc / (TIME)
        fc = 0
        start_time = time()

    fps_disp = "FPS: " + str(FPS)[:3]   
    date_now = datetime.date.today()

    # Format time as string
    date_str = date_now.strftime("%B-%d-%Y")
    date_temp = date_str.split("-")
    tmp = str(months.index(date_temp[0]) + 1)
    if len(tmp) < 2:
        tmp = '0' + tmp
        
    date_str = date_str.replace(date_temp[0],tmp)
    file_path = "report/report_" + date_str+ ".csv"

    # Check if the file exists
    if os.path.exists(file_path):
        pass
    else:
        number = 1
        report.create_report(file_path)

    # Add FPS count on frame
    image = cv2.putText(frame, fps_disp, (10, 25),
        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    
    face_locations = util.face_detect(image)
    for face_loc in face_locations:
        y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]
        frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 200), 4)

    video = camera.Video()
    video.ImageUpdate.connect(Form_1.ImageUpdateShot)
    video.process(frame)
    
    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
