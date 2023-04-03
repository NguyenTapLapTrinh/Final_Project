import sys
sys.path.append("./back-end")
sys.path.append("./front-end")
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from time import *
import os
import datetime
import report
#import texttospeed as ts
import util
import worker
import yolo_detection
import info
import threading
import socket
import text
import server_mng
import unidecode


classes_vn = ["Mũ bảo hiểm", "Áo bảo hộ", "Găng tay bảo hộ"]
classes = []

with open("coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]

yolo = yolo_detection.Yolo(classes)
yolo.loadWeight("weight/yolov4_training_last.weights","weight/yolov4_testing.cfg")

def closeWidget():
    Form_1.video.block = 0
    widget_2.close()
def closeMain():
    Form_1.video.block = 1
    widget_1.closeEvent()
def updateWidget(note,name,unicode_name,time,date,empty):
    Form_2.updateResult(note)
    Form_2.updateName(name)
    Form_2.updateTime(time)
    Form_2.updateDate(date)
    Form_2.updateHelmet(0)
    Form_2.updateVest(0)
    Form_2.updateGlove(0)
    Form_2.updateWorkerPhoto(unicode_name)
    for i in empty:
        if i == 0:
            Form_2.updateHelmet(1)
        elif i == 1:
            Form_2.updateVest(1)
        elif i == 2:
            Form_2.updateGlove(1)

def processImage():
    Form_1.video.block = 1
    file_path = Form_1.video.file_path
    date_str = Form_1.video.date_str
    time_now = datetime.datetime.now().time()
    time_str = time_now.strftime("%H:%M:%S")
    frame = Form_1.video.frame
    height = Form_1.video.height
    width = Form_1.video.width
    yolo.setVar(frame,height,width)
    empty = yolo.objectDetect()
    try:
        name = util.recognize(frame, './db')
    except:
        dlg = QMessageBox()
        dlg.setIcon(QMessageBox.Warning)
        dlg.setText("No person found!   ")
        dlg.setWindowTitle("            Info          ")
        dlg.setStandardButtons(QMessageBox.Ok)
        dlg.exec()
        Form_1.video.block = 0
        return
    if name == "no_persons_found":
        dlg = QMessageBox()
        dlg.setIcon(QMessageBox.Warning)
        dlg.setText("No person found!   ")
        dlg.setWindowTitle("            Info          ")
        dlg.setStandardButtons(QMessageBox.Ok)
        dlg.exec()
        Form_1.video.block = 0
        return
    print(name)
    full_name = text.findFullName(name)
    print("OK")
    print(full_name)
    find =0
    try:
        find,note = report.edit_report(file_path,full_name,time_str,empty)
    except:
        pass
    if not find: 
        note = report.write_report(file_path,full_name,time_str,empty)
    string = "có đầy đủ bảo hộ"
    leng = len(empty)
    if leng > 0:
        string = "Không có "
        for i in empty:
            string = string + classes_vn[i] + " "
            if leng > 1:
                string += "và "
                leng -= 1
    unicode_name = unidecode.unidecode(full_name)
    updateWidget(note,full_name,unicode_name,time_str,date_str,empty)
    widget_2.show()  
    #ts.start_sound(string,full_name+" ")    

#Thread
def ThreadServer():
    sleep(2)
    while True:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #server_socket.setblocking(1)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(("localhost", 5000))
        server_socket.listen(1)
        client_socket,a = server_socket.accept()
        #server_socket.settimeout(3)
        message = client_socket.recv(1024)
        message = message.decode()
        request = message.split("-")
        if request[0] == "Send":
            server_mng.setData(client_socket,request[1])
        elif request[0] == "Remove":
            server_mng.deleteData(client_socket,request[1])
        elif request[0] == "EditImage":
            server_mng.editPhoto(client_socket,request[1])
        elif request[0] == "EditName":
            server_mng.editName(client_socket,request[1],request[2])
        elif request[0] == "UpdateCSV":
            server_mng.sendCSV(client_socket, Form_1.video.file_path)
        elif request[0] == "LoadCSV":
            server_mng.sendCurrentCSV(client_socket,request[1]+ "-" +request[2]+ "-" +request[3], Form_1.video.file_path)
        elif request[0] == "ListEmployee":
            server_mng.sendEmployee(client_socket)
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
if os.path.exists("temp"):
    pass
else:
    os.mkdir("temp")
thread = threading.Thread(target=ThreadServer)
thread.start()

#Show Gui
app = QtWidgets.QApplication(sys.argv)
widget_1 = QtWidgets.QWidget()
Form_1 = worker.Ui_Form()
Form_1.setupUi(widget_1)
Form_1.ButtonActivation(processImage)
Form_1.ButtonClose(closeMain)
widget_1.show()

widget_2 = QtWidgets.QWidget()
Form_2 = info.Ui_Form()
Form_2.setupUi(widget_2)
Form_2.ButtonActivation(closeWidget)
sys.exit(app.exec_())

