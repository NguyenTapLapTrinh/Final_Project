import sys
sys.path.append("./back-end")
sys.path.append("./front-end")
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap
import cv2
import numpy as np
from time import *
import os
import datetime
import face_recognition
import numpy as np
import report
import texttospeed as ts
import util
from worker import *

def face_detect(frame):
    face_locations = face_recognition.face_locations(frame)
    face_locations = np.array(face_locations)
    face_locations.astype(int)
    return face_locations


# Load Yolo
net = cv2.dnn.readNet("weight/yolov4_training_last.weights", "weight/yolov4_testing.cfg")
classes = []
classes_vn = ["Mũ bảo hiểm", "Áo bảo hộ", "Găng tay bảo hộ"]
with open("coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]

layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
colors = np.random.uniform(0, 255, size=(len(classes), 3))
#FPS
start_time = time()
display_time = 2
fc = 0
FPS = 0
frame = cv2.imread("Img/data_test/033.jpg")
frame = cv2.resize(frame,(416,416))
#cap = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_COMPLEX_SMALL

months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

STT = 1
if os.path.exists("report"):
    pass
else:
    os.mkdir("report")

app = QtWidgets.QApplication(sys.argv)
Form = QtWidgets.QWidget()
ui = Ui_Form()
ui.setupUi(Form)
Form.show()
sys.exit(app.exec_())

while True:
    #_, frame = cap.read()
    height, width, channels = frame.shape
    # Detecting objects
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)

    net.setInput(blob)
    outs = net.forward(output_layers)
    fc+=1
    TIME = time() - start_time
    if (TIME) >= display_time :
        FPS = fc / (TIME)
        fc = 0
        start_time = time()

    fps_disp = "FPS: " + str(FPS)[:3]
    time_now = datetime.datetime.now().time()
    date_now = datetime.date.today()

    # Format time as string
    time_str = time_now.strftime("%H:%M:%S")
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
        report.create_report(file_path)

    # Add FPS count on frame
    image = cv2.putText(frame, fps_disp, (10, 25),
        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = face_detect(img)
    for face_loc in face_locations:
        y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]
        frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 200), 4)

    class_ids = []
    confidences = []
    boxes = []
    empty = [0,1,2]

    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.8:
                # Object detected
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                # Rectangle coordinates
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.8, 0.6)
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            confidence = confidences[i]
            color = colors[class_ids[i]]
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            cv2.putText(frame, label + " " + str(round(confidence, 2)),
                        (x, y-10), font, 1, color, 3)   

    for i in class_ids:
        try:
            empty.remove(i)
        except:
            continue

    report.write_report(file_path,str(STT),"Ngô Trung Nguyên",time_str,empty)
    STT += 1

    string = "có đầy đủ bảo hộ"
    leng = len(empty)
    if leng > 0:
        string = "Không có "
        for i in empty:
            string = string + classes_vn[i] + " "
            if leng > 1:
                string += "và "
                leng -= 1

    ts.start_sound(string,"Ngô Trung Nguyên ")  
    cv2.imshow("Image", frame)    
    report.edit_report(file_path,"Ngô Trung Nguyên",time_str,[2])

    key = cv2.waitKey(0)
    if key == 27:
        break

frame.release()
cv2.destroyAllWindows()
