# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'info.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap
import pathlib

#import images_2

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1024, 600)
        self.photo = QtWidgets.QLabel(Form)
        self.photo.setGeometry(QtCore.QRect(70, 90, 291, 361))
        self.photo.setStyleSheet("border: 1px solid black;")
        self.photo.setText("")
        self.photo.setObjectName("photo")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(20, 510, 81, 31))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(410, 20, 261, 31))
        self.label_3.setObjectName("label_3")
        self.name = QtWidgets.QLabel(Form)
        self.name.setGeometry(QtCore.QRect(100, 506, 321, 41))
        self.name.setObjectName("name")
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setGeometry(QtCore.QRect(440, 80, 541, 421))
        self.label_5.setStyleSheet("background-color: rgb(0, 170, 255);")
        self.label_5.setText("")
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(Form)
        self.label_6.setGeometry(QtCore.QRect(450, 85, 91, 41))
        self.label_6.setObjectName("label_6")
        self.day = QtWidgets.QLabel(Form)
        self.day.setGeometry(QtCore.QRect(540, 90, 211, 31))
        self.day.setStyleSheet("font-size: 24px;\n"
"font-weight: 600")
        self.day.setObjectName("day")
        self.label_8 = QtWidgets.QLabel(Form)
        self.label_8.setGeometry(QtCore.QRect(450, 125, 91, 61))
        self.label_8.setObjectName("label_8")
        self.time = QtWidgets.QLabel(Form)
        self.time.setGeometry(QtCore.QRect(550, 138, 111, 31))
        self.time.setStyleSheet("\n"
"font-size: 24px;\n"
"font-weight: 600;")
        self.time.setObjectName("time")
        self.label_11 = QtWidgets.QLabel(Form)
        self.label_11.setGeometry(QtCore.QRect(450, 230, 521, 261))
        self.label_11.setStyleSheet("border-radius: 10px;\n"
"background-color: rgb(0, 255, 255);")
        self.label_11.setText("")
        self.label_11.setObjectName("label_11")
        self.label_12 = QtWidgets.QLabel(Form)
        self.label_12.setGeometry(QtCore.QRect(460, 240, 171, 31))
        self.label_12.setObjectName("label_12")
        self.vest = QtWidgets.QLabel(Form)
        self.vest.setGeometry(QtCore.QRect(690, 300, 81, 61))
        self.vest.setStyleSheet("image: url(Img/Icon/vest.png);")
        self.vest.setObjectName("vest")
        
        self.label_15 = QtWidgets.QLabel(Form)
        self.label_15.setGeometry(QtCore.QRect(360, 0, 51, 61))
        self.label_15.setStyleSheet("image: url(Img/Icon/construction-worker.png);")
        self.label_15.setText("")
        self.label_15.setObjectName("label_15")
        self.label_16 = QtWidgets.QLabel(Form)
        self.label_16.setGeometry(QtCore.QRect(470, 420, 91, 41))
        self.label_16.setObjectName("label_16")
        self.label_17 = QtWidgets.QLabel(Form)
        self.label_17.setGeometry(QtCore.QRect(550, 420, 241, 41))
        self.label_17.setStyleSheet("font-size: 20px;\n"
"font-weight: 600")
        self.label_17.setObjectName("label_17")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(650, 520, 171, 61))
        self.pushButton.setStyleSheet("background-color: green;\n"
"color: white;\n"
"font-size: 24px;\n"
"font-weight: 600;\n"
"border-radius: 10px;")
        self.pushButton.setObjectName("pushButton")
        self.helmet = QtWidgets.QLabel(Form)
        self.helmet.setGeometry(QtCore.QRect(570, 300, 81, 61))
        self.helmet.setStyleSheet("image: url(Img/Icon/helmet.png);\n""background: none;")
        self.helmet.setObjectName("helmet")
        self.glove = QtWidgets.QLabel(Form)
        self.glove.setGeometry(QtCore.QRect(800, 300, 91, 61))
        self.glove.setStyleSheet("image: url(Img/Icon/gloves.png);")
        self.glove.setObjectName("glove")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(180, 460, 131, 16))
        self.label.setStyleSheet("font-size: 20px;\n"
"font-weight: 600")
        self.label.setObjectName("label")
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
    def ButtonActivation(self,function):
        self.pushButton.clicked.connect(function)

    def setName(self,name):
        self.name.setText(name)

    def setTime(self,time):
        self.time.setText(time)

    def setDate(self,day):
        self.day.setText(day)

    def updateHelmet(self,isempty):
        color = "green"
        if isempty == 1:
            color = "red"
        self.helmet.setStyleSheet("image: url(Img/Icon/helmet.png);\n""background: "+ color+ ";")

    def updateVest(self,isempty):
        color = "green"
        if isempty == 1:
            color = "red"
        self.vest.setStyleSheet("image: url(Img/Icon/vest.png);\n""background: "+ color+ ";")

    def updateGlove(self,isempty):
        color = "green"
        if isempty == 1:
            color = "red"
        self.glove.setStyleSheet("image: url(Img/Icon/gloves.png);\n""background: "+ color+ ";")

    def updateResult(self,note):
        self.label_17.setText(note)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_2.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:12pt; font-weight:600;\">Name:</span></p></body></html>"))
        self.label_3.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:12pt; font-weight:600;\">WORKER INFORMATION</span></p></body></html>"))
        self.label_6.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:12pt; font-weight:600;\">DAY IN:</span></p></body></html>"))
        self.label_8.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:12pt; font-weight:600;\">TIME IN:</span></p></body></html>"))
        self.label_12.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:10pt; font-weight:600;\">SAFETY STATUS</span></p></body></html>"))
        self.label_16.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:10pt; font-weight:600;\">RESULT:</span></p></body></html>"))
        self.pushButton.setText(_translate("Form", "OK"))
        self.label.setText(_translate("Form", "PHOTO"))




if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
