import sys
sys.path.append("./back-end")
sys.path.append("./front-end")
from PyQt5 import QtCore, QtGui, QtWidgets
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

def button():
    global number
    time_now = datetime.datetime.now().time()
    Form_1.progressBar.setProperty("value", 10)
    sleep(0.5)
    time_str = time_now.strftime("%H:%M:%S")
    Form_1.progressBar.setProperty("value", 30)
    sleep(0.5)
    empty = yolo.objectDetect()
    Form_1.progressBar.setProperty("value", 60)
    sleep(0.5)
    note = report.write_report(file_path,str(number),"Ngô Trung Nguyên",time_str,empty)
    number +=1
    string = "có đầy đủ bảo hộ"
    leng = len(empty)
    Form_1.progressBar.setProperty("value", 80)
    sleep(0.5)
    if leng > 0:
        string = "Không có "
        for i in empty:
            string = string + classes_vn[i] + " "
            if leng > 1:
                string += "và "
                leng -= 1
    Form_1.progressBar.setProperty("value", 100)
    sleep(0.5)
    ts.start_sound(string,"Ngô Trung Nguyên ")
    Form_2.updateResult(note)
    Form_2.setName("Ngô Trung Nguyên")
    Form_2.setTime(time_str)
    Form_2.setDate(date_str)
    Form_2.updateHelmet(0)
    Form_2.updateVest(0)
    Form_2.updateGlove(0)
    for i in empty:
        if i == 0:
            Form_2.updateHelmet(1)
        elif i == 1:
            Form_2.updateVest(1)
        elif i == 2:
            Form_2.updateGlove(1)
    widget_2.show()
    Form_1.progressBar.setProperty("value", 0)

if os.path.exists("report"):
    pass
else:
    os.mkdir("report")

cap = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_COMPLEX_SMALL

#FPS
start_time = time()
display_time = 2
fc = 0
FPS = 0

#Show Gui
app = QtWidgets.QApplication(sys.argv)
widget_1 = QtWidgets.QWidget()
Form_1 = worker.Ui_Form()
Form_1.setupUi(widget_1)
Form_1.ButtonActivation(button)
widget_1.show()

widget_2 = QtWidgets.QWidget()
Form_2 = info.Ui_Form()
Form_2.setupUi(widget_2)
Form_2.ButtonActivation(closeWidget)



while True:
    _, frame = cap.read()
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
    #report.edit_report(file_path,"Ngô Trung Nguyên",time_str,[2])

    key = cv2.waitKey(1)
    if key == 27:
        break

frame.release()
cv2.destroyAllWindows()
