# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'admin.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

import sys
sys.path.append("./back-end")
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QMessageBox,QApplication, QMainWindow, QPushButton
from PyQt5.QtCore import QCoreApplication
import os
import subprocess
import glob
import socket
from tkinter import filedialog
import face_recognition
import pickle
import cv2
import socket
import time
class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(838, 534)
        self.photo = QtWidgets.QLabel(Form)
        self.photo.setGeometry(QtCore.QRect(5, 0, 491, 531))
        self.photo.setStyleSheet("border: 2px solid black;\n""image: url(./Img/Icon/Unknown_person.jpg);")
        self.photo.setText("")
        self.photo.setObjectName("photo")
        self.add_employ = QtWidgets.QPushButton(Form)
        self.add_employ.setGeometry(QtCore.QRect(530, 350, 271, 41))
        self.add_employ.setStyleSheet("background-color: #05f26c;\n"
"border-radius: 10px;\n"
"border: 1px solid black;\n"
"color: #fff;\n"
"font-size: 20px;")
        self.add_employ.setObjectName("add_employ")
        self.add_photo = QtWidgets.QPushButton(Form)
        self.add_photo.setGeometry(QtCore.QRect(530, 300, 271, 41))
        self.add_photo.setStyleSheet("background-color: #1270e3;\n"
"border-radius: 10px;\n"
"border: 1px solid black;\n"
"color: #fff;\n"
"font-size: 20px;")
        self.add_photo.setObjectName("add_photo")
        self.input_name = QtWidgets.QLineEdit(Form)
        self.input_name.setGeometry(QtCore.QRect(510, 240, 311, 41))
        self.input_name.setStyleSheet("font-size: 18px;\n""font-weight:600")
        self.input_name.setText("")
        self.input_name.setObjectName("input_name")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(510, 210, 191, 20))
        self.label_2.setStyleSheet("font-size: 18px;\n"
"font-weight: 600;")
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(550, 150, 281, 51))
        self.label_3.setStyleSheet("font-size: 18px;\n"
"font-weight: 600;")
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(580, 20, 201, 121))
        self.label_4.setStyleSheet("image: url(./Img/Icon/work_management.png);")
        self.label_4.setText("")
        self.label_4.setObjectName("label_4")
        self.remove_employ = QtWidgets.QPushButton(Form)
        self.remove_employ.setGeometry(QtCore.QRect(530, 400, 271, 41))
        self.remove_employ.setStyleSheet("background-color: #f230ec;\n"
"border-radius: 10px;\n"
"border: 1px solid black;\n"
"color: #fff;\n"
"font-size: 20px;")
        self.remove_employ.setObjectName("remove_employ")
        self.close_btn = QtWidgets.QPushButton(Form)
        self.close_btn.setGeometry(QtCore.QRect(530, 450, 271, 41))
        self.close_btn.setStyleSheet("background-color: red;\n"
"border-radius: 10px;\n"
"border: 1px solid black;\n"
"color: #fff;\n"
"font-size: 20px;")
        self.close_btn.setObjectName("close_btn")
        self.add_photo.clicked.connect(self.addImage)
        self.add_employ.clicked.connect(self.addEmploy)
        self.remove_employ.clicked.connect(self.rmEmploy)
        self.close_btn.clicked.connect(QCoreApplication.instance().quit)
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        self.file_path=""
    def addImage(self):
        self.file_path = filedialog.askopenfilename(title="Chọn ảnh", filetypes=(("JPEG files", "*.jpg"), ("PNG files", "*.png"), ("All files", "*.*")))
        self.photo.setStyleSheet("border: 2px solid black;\n""image: url(" + self.file_path + ");")
    def addEmploy(self):
        input_employ = self.input_name.text()
        if input_employ == "" or self.file_path=="":
                self.dlg = QMessageBox()
                self.dlg.setIcon(QMessageBox.Warning)
                self.dlg.setText("Please check again!              ")
                self.dlg.setWindowTitle("Info")
                self.dlg.setStandardButtons(QMessageBox.Ok)
                self.dlg.exec()
                return 
        else:
                name_file = input_employ + ".jpg"
                new_file_path = os.path.join(os.path.dirname(self.file_path), name_file)
                os.rename(self.file_path, new_file_path)
                frame = cv2.imread(new_file_path)
                embeddings = face_recognition.face_encodings(frame)[0]
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.connect(("localhost", 5000))
                file_name = new_file_path
                filetosend = open(file_name, "rb")
                client_socket.send(file_name.encode())
                time.sleep(1)
                data1 = filetosend.read(1024)
                while data1:
                        print("Sending Image...")
                        client_socket.send(data1)
                        time.sleep(0.1)
                        data1 = filetosend.read(1024)
                filetosend.close()
                string = "Done"
                client_socket.send(string.encode())
                time.sleep(0.1)
                for i in embeddings:
                        data_string = str(i)
                        print(data_string)
                        client_socket.send(data_string.encode())
                        time.sleep(0.1)
                print("Done Sending.")
                client_socket.close()
    def rmEmploy(self):
        input_employ = self.input_name.text()
        if input_employ == "":
                self.dlg = QMessageBox()
                self.dlg.setIcon(QMessageBox.Error)
                self.dlg.setText("Please check again!              ")
                self.dlg.setWindowTitle("Info")
                self.dlg.setStandardButtons(QMessageBox.Ok)
                self.dlg.exec()
                return
        check=0
        check_path = "Img/worker_img/"
        files = os.listdir(check_path)
        for file in files:
                if file.endswith(".jpg"):
                        file_name = os.path.splitext(file)[0]
                        if input_employ == file_name:
                             check=1
        if check==1:
                file_path = "Img/worker_img/" + input_employ +".jpg"
                pickle_path = "db/" + input_employ +".pickle"
                os.remove(file_path)
                os.remove(pickle_path)
                self.dlg = QMessageBox()
                self.dlg.setIcon(QMessageBox.Information)
                self.dlg.setText(input_employ + "has been deleted              ")
                self.dlg.setWindowTitle("Info")
                self.dlg.setStandardButtons(QMessageBox.Ok)
                self.dlg.exec() 
        else: 
                self.dlg = QMessageBox()
                self.dlg.setIcon(QMessageBox.Warning)
                self.dlg.setText("Not have this employee!              ")
                self.dlg.setWindowTitle("Info")
                self.dlg.setStandardButtons(QMessageBox.Ok)
                self.dlg.exec()
                return  
    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Employee Management"))
        Form.setWindowIcon(QIcon("./Img/Icon/officer.png"))
        self.add_employ.setText(_translate("Form", "Add Employee"))
        self.add_photo.setText(_translate("Form", "Add Photo"))
        self.label_2.setText(_translate("Form", "Employee Name"))
        self.label_3.setToolTip(_translate("Form", "<html><head/><body><p><span style=\" font-size:20pt;\">UPDATE </span></p><p><span style=\" font-size:20pt;\">EMPLOYEE INFO</span></p></body></html>"))
        self.label_3.setText(_translate("Form", "EMPLOYEE MANAGEMENT"))
        self.remove_employ.setText(_translate("Form", "Remove Employee"))
        self.close_btn.setText(_translate("Form", "Close"))

            


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
