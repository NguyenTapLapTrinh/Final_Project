import os.path
import pickle
import cv2
import face_recognition
import time
from PyQt5.QtWidgets import  QWidget, QLabel, QApplication
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap


if __name__ == "__main__":
    name = "Nguyen"
    cap = cv2.VideoCapture(0) 
    while True:
        _, frame = cap.read()
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1)
        if key == 27:
            break
    try:
        embeddings = face_recognition.face_encodings(frame)[0]
    except:
       print("Cant detect human face !\nAre you a human ???")
    else:
        cv2.imwrite("./Img/worker_img/Nguyen.jpg",frame)
        with open(os.path.join('./db', '{}.pickle'.format(name)), 'wb') as file:
            pickle.dump(embeddings, file)
        





