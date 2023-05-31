# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'worker.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
import sys
sys.path.append("./back-end")
sys.path.append("./front-end")
sys.path.append("./admin_gui")

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtCore import Qt, QModelIndex, QTimer
from time import sleep
import camera

class Ui_Form(object):
    video =  camera.Video()
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1024, 600)
        Form.setStyleSheet("")
        self.camera = QtWidgets.QLabel(Form)
        self.camera.setGeometry(QtCore.QRect(140, 0, 731, 551))
        self.camera.setStyleSheet("border: 2px solid black;\n"
"")
        self.camera.setText("")
        self.camera.setObjectName("camera")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(910, 380, 81, 71))
        self.pushButton.setStyleSheet("font-size: 18px;\n"
"font-weight: 600;\n"
"color: white;\n"
"border-radius: 10px;\n"
"image: url(Img/Icon/camera.png);\n"
"")
        self.pushButton.setText("")
        self.pushButton.setObjectName("pushButton")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(900, 80, 91, 91))
        self.label_2.setPixmap(QPixmap("Img/Icon/safety.png"))
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(890, 160, 121, 181))
        self.label_3.setStyleSheet("background: none;\n"
"color: white;\n"
"font-size: 18px;")
        self.label_3.setObjectName("label_3")
        self.label_left = QtWidgets.QLabel(Form)
        self.label_left.setGeometry(QtCore.QRect(0, 0, 161, 551))
        self.label_left.setStyleSheet("background-color: qlineargradient(spread:repeat, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(221, 151, 37, 255), stop:1 rgba(255, 255, 255, 255));\n"
"")
        self.label_left.setText("")
        self.label_left.setObjectName("label_left")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(870, 0, 161, 551))
        self.label_4.setStyleSheet("background-color: qlineargradient(spread:repeat, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(221, 151, 37, 255), stop:1 rgba(255, 255, 255, 255));\n"
"")
        self.label_4.setText("")
        self.label_4.setObjectName("label_4")
        self.left = QtWidgets.QLabel(Form)
        self.left.setGeometry(QtCore.QRect(0, 0, 161, 551))
        self.left.setStyleSheet("background-color: qlineargradient(spread:repeat, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(221, 151, 37, 255), stop:1 rgba(255, 255, 255, 255));\n"
"")
        self.left.setText("")
        self.left.setObjectName("left")
        # self.progressBar = QtWidgets.QProgressBar(Form)
        # self.progressBar.setGeometry(QtCore.QRect(200, 560, 631, 23))
        # self.progressBar.setProperty("value", 0)
        # self.progressBar.setObjectName("progressBar")
        # self.label_5 = QtWidgets.QLabel(Form)
        # self.label_5.setGeometry(QtCore.QRect(10, 560, 181, 20))
        # self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(Form)
        self.label_6.setGeometry(QtCore.QRect(900, 460, 121, 20))
        self.label_6.setObjectName("label_6")
        self.close_btn= QtWidgets.QPushButton(Form)
        self.close_btn.setGeometry(QtCore.QRect(950, 20, 31, 31))
        self.close_btn.setStyleSheet("\n"
"font-size: 16px;\n"
"font-weight: 500;\n"
"color: white;\n"
"background-color: red;\n"
"")
        self.close_btn.setObjectName("close_btn")
        # Căn chỉnh QLabel vào giữa QWidget
        self.label_4.raise_()
        self.camera.raise_()
        self.pushButton.raise_()
        self.label_2.raise_()
        self.label_3.raise_()
        # self.progressBar.raise_()
        #self.label_5.raise_()
        self.label_6.raise_()
        self.close_btn.raise_()
        self.video.ImageUpdate.connect(self.ImageUpdateShot)
        self.video.start()
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
    def ImageUpdateShot(self, Image):
        self.camera.setPixmap(QPixmap.fromImage(Image))
    def ButtonActivation(self,function):
        self.pushButton.clicked.connect(function)
    def ButtonClose(self, function):
        self.close_btn.clicked.connect(function)
    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Checking worker System"))
        Form.setWindowIcon(QIcon("Img/Icon/worker.png"))
        self.label_3.setText(_translate("Form", "<html><head/><body><p align=\"center\"><span style=\" font-size:10pt; font-weight:600;\">CHECKING </span></p><p align=\"center\"><span style=\" font-size:10pt; font-weight:600;\">ATTENDANCE</span></p><p align=\"center\"><span style=\" font-size:10pt; font-weight:600;\">WIDGET</span></p><p align=\"center\"><span style=\" font-size:9pt;\">Cre: Nguyen-Hieu</span></p></body></html>"))
        #self.label_5.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:9pt; font-weight:600;\">IMAGES PROCESSING</span></p></body></html>"))
        self.label_6.setText(_translate("Form", "<html><head/><body><p><span style=\" font-weight:600;\">CAPTURE IMAGE</span></p></body></html>"))
        self.close_btn.setText(_translate("Form", "X"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
