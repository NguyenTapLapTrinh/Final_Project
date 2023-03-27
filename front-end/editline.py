from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class Ui_Dialog_1(object):
    def setupUi_3(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(360, 120)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(50, 70, 200,30))
        self.label.setObjectName("label")

        self.line = QtWidgets.QLineEdit(Dialog)
        self.line .setGeometry(QtCore.QRect(30, 20, 300, 30))
        self.line.setStyleSheet("font-size: 16px;\n""font-weight:600")
        self.line .setObjectName("line")

        self.loadbtn = QtWidgets.QPushButton(Dialog)
        self.loadbtn .setGeometry(QtCore.QRect(230, 60, 100,30))
        self.loadbtn .setObjectName("newlabel")

        self.retranslateUi_1(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi_1(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Enter Name Dialog"))
        self.label.setText("")
        self.loadbtn.setText("Yes")
        self.line.setPlaceholderText("Enter Name")