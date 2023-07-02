import sys
sys.path.append("./back-end")
sys.path.append("./front-end")
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QTimer, Qt, QEventLoop
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QCoreApplication
from PyQt5.QtGui import QMovie, QPixmap, QIcon
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
from time import *
import os
import datetime
import report
import util
import worker
import info
import threading
import text
import server_mng
import unidecode
import msg
from multiprocessing import Process, Pipe
import init
from define import Time, Item, Socket

# global variable
timer = QtCore.QTimer()
timerActive = False
yolo = ''
waitBox = ''

def closeWidget():
    widget_2.close()

def closeMain():
    Form_1.video.block = True
    # os.system('killall -9 python3.8')
    widget_1.close()

def updateWidget(note,name,unicode_name,time,date,emptyList):
    Form_2.updateResult(note)
    Form_2.updateName(name)
    Form_2.updateTime(time)
    Form_2.updateDate(date)
    Form_2.updateHelmet(False)
    Form_2.updateVest(False)
    Form_2.updateGlove(False)
    Form_2.updateWorkerPhoto(unicode_name)
    for item in emptyList:
        if item == Item.HELMET.value:
            Form_2.updateHelmet(True)
        elif item == Item.VEST.value:
            Form_2.updateVest(True)
        elif item == Item.GLOVE.value:
            Form_2.updateGlove(True)

#Hàm xử lí hình ảnh
def processImage():
    global yolo
    global timerActive
    global waitBox  
    if not timerActive:
        return
    timer.stop()
    waitBox.close()
    Form_1.video.block = True
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
        msg.ShowMsg("Warning","No person found!")
        timerActive = False
        Form_1.video.block = False
        return
    if name == "no_persons_found":
        msg.ShowMsg("Warning","No person found!")
        timerActive = False
        Form_1.video.block = False
        return
    full_name = text.findFullName(name)
    find = False
    try:
        find,note = report.edit_report(file_path,full_name,time_str,empty)
    except:
        pass
    if not find: 
        note = report.write_report(file_path,full_name,time_str,empty)

    unicode_name = unidecode.unidecode(full_name)
    updateWidget(note,full_name,unicode_name,time_str,date_str,empty)
    timerActive = False
    Form_1.video.block = False
    widget_2.show()     

#Họp thoại tạm dừng
def waitingCapture():
    global waitBox
    global timerActive
    if not timerActive:
        timerActive = True
        waitBox = QMessageBox()
        icon_path = "Img/Icon/info.png"
        icon = QIcon(icon_path)
        waitBox.setWindowIcon(icon)
        waitBox.setIcon(QMessageBox.Information)
        waitBox.setWindowTitle("Warning")
        waitBox.setText("Wait 5 seconds")
        waitBox.show()
        timer.timeout.connect(processImage)
        timer.start(Time.TIME_SLEEP_5S.value)

def ThreadServer():
    server_socket = server_mng.createSocket(Socket.IPADRESS.value,Socket.PORT.value)
    while True:
        try:
            if (Form_1.video.file_path == ""):
                continue
        except:
            pass
        else:
            server_mng.mainServer(Form_1.video.file_path,server_socket)

class Server(QThread):
        def run(self):
            server_socket = server_mng.createSocket(Socket.IPADRESS.value,Socket.PORT.value)
            while True:
                try:
                    if (Form_1.video.file_path == ""):
                        continue
                except:
                    pass
                else:
                    server_mng.mainServer(Form_1.video.file_path,server_socket)
        def stop(self):
                self.quit()

class UpdateServer(QThread):
        def run(self):
            server_socket = server_mng.createSocket(Socket.IPADRESS.value,Socket.UPDATE_PORT.value)
            while True:
                try:
                    if (Form_1.video.file_path == ""):
                        continue
                except:
                    pass
                else:
                    server_mng.mainUpdateServer(Form_1.video.file_path,server_socket)
        def stop(self):
                self.quit()

if __name__ == "__main__":
    init.ServerInit()
    yolo = init.YoloInit()

    # Start Thread Server
    # thread = threading.Thread(target=ThreadServer)
    # thread.start()
    server = Server()
    server.start()

    updateserver = UpdateServer()
    updateserver.start()
    #Show Gui
    app = QtWidgets.QApplication(sys.argv)
    widget_1 = QtWidgets.QWidget()
    Form_1 = worker.Ui_Form()
    Form_1.setupUi(widget_1)
    Form_1.ButtonActivation(waitingCapture)
    Form_1.ButtonClose(closeMain)


    widget_2 = QtWidgets.QWidget()
    Form_2 = info.Ui_Form()
    Form_2.setupUi(widget_2)
    Form_2.ButtonActivation(closeWidget)

    widget_1.show()

    sys.exit(app.exec_())
