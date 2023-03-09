import os.path
import pickle
import cv2
import face_recognition
import time
from PyQt5.QtWidgets import  QWidget, QLabel, QApplication
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
import socket

if __name__ == "__main__":
    name = "Nguyen"
    frame = cv2.imread("Nguyen.jpg") 
    while True:
        # _, frame = cap.read()
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(0)
        if key == 27:
            break
    try:
        embeddings = face_recognition.face_encodings(frame)[0]
    except:
       print("Cant detect human face !\nAre you a human ???")
    else:
        cv2.imwrite("Nguyen.jpg",frame)
    with open("Nguyen.pickle", 'wb') as file:
        data_string = pickle.dump(embeddings, file)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("localhost", 5000))
    #file_name = input("Enter file name: ")
    file_name = "Nguyen.jpg"
    filetosend = open(file_name, "rb")
    file_pickle = "Nguyen.pickle"
    client_socket.send(file_name.encode())
    time.sleep(1)
    data1 = filetosend.read(1024)
    while data1:
        print("Sending Image...")
        client_socket.send(data1)
        data1 = filetosend.read(1024)
    filetosend.close()
    string = "Done"
    client_socket.send(string.encode())
    for i in embeddings:
        data_string = str(i)
        print(data_string)
        client_socket.send(data_string.encode())
        time.sleep(0.1)
    print("Done Sending.")
    client_socket.close()





