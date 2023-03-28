# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


import sys
sys.path.append("./back-end")
sys.path.append("./front-end")
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QModelIndex, QTimer
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QColor, QStandardItemModel, QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableView,  QStyledItemDelegate, QHeaderView, QAbstractItemView
import csv
from datetime import datetime
from admin import *
from edit import *
from editline import *
import client_mng
import msg
import os
import socket
from tkinter import filedialog
import face_recognition
import cv2
import socket
import time
import threading
sys.setrecursionlimit(5000)
now = datetime.now()
# edit table
choose = 0
class CenteredHeaderView(QHeaderView):
    def __init__(self, orientation, parent=None):
        super().__init__(orientation, parent)
        self.setDefaultAlignment(Qt.AlignCenter)
class CenteredItemDelegate(QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)
        option.displayAlignment = Qt.AlignCenter
class Widget_1(QDialog):
    def __init__(self, parent=None):
        super(Widget_1, self).__init__(parent)
        self.edit = Ui_Dialog_1()
        self.edit.setupUi_3(self)
        self.edit.loadbtn.clicked.connect(self.create)
        self.name = ""
        self.old_name = ""
    def create(self):
        self.name =  self.edit.line.text()
        self.edit.line.clear()
        if self.name == "":
                msg.ShowMsg("Info","Please check again!")
        else:
                client_mng.editName(self.old_name, self.name)
                self.close()
class Widget_2(QDialog):
    def __init__(self, parent=None):
        super(Widget_2, self).__init__(parent)
        self.edit = Ui_Dialog_1()
        self.edit.setupUi_3(self)
        self.edit.loadbtn.clicked.connect(self.create)
        self.name = ""
        self.old_name = ""
    def create(self):
        self.name =  self.edit.line.text()
        self.edit.line.clear()
        if self.name == "":
                msg.ShowMsg("Info","Please check again!")
        else:
                client_mng.deleteData(self.name)
                self.close()                    
class Admin_UI(QDialog):
    def __init__(self, parent=None):
        super(Admin_UI, self).__init__(parent)
        self.ui_1 = Ui_Form_1()
        self.ui_1.setupUi_1(self)
        self.ui_1.add_photo.clicked.connect(self.addImage)
        self.ui_1.add_employ.clicked.connect(self.addEmploy)
        self.ui_1.close_btn.clicked.connect(self.close)
        self.ui_1.file_path=""
    def addImage(self):
        self.ui_1.file_path = filedialog.askopenfilename(title="Chọn ảnh", filetypes=(("JPEG files", "*.jpg"), ("PNG files", "*.png"), ("All files", "*.*")))
        if self.ui_1.file_path == "":
              return
        img = cv2.imread(self.ui_1.file_path)
        Image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        ConvertToQTFormat = QImage(Image.data, Image.shape[1], Image.shape[0], QImage.Format_RGB888)
        Pic = ConvertToQTFormat.scaled(591, 531)
        self.ui_1.photo.setPixmap(QPixmap.fromImage(Pic))

    def EditInfo(self, input_employ, request):
        if request == client_mng.CMD.ADD:
                client_mng.setData(self.ui_1.file_path,input_employ)

        elif request == client_mng.CMD.DEL:
                client_mng.deleteData(input_employ)

    def addEmploy(self):
        input_employ = self.ui_1.input_name.text()
        if input_employ == "" or self.ui_1.file_path=="":
                msg.ShowMsg("Info","Please check again!")
                return 
        else:
                #input_employ = input_employ.replace(" ","_")
                self.EditInfo(input_employ, client_mng.CMD.ADD)
class Edit_UI(QDialog):
    def __init__(self, parent=None):
        super(Edit_UI, self).__init__(parent)
        self.ui_2 = Ui_Form_2()
        self.ui_2.setupUi_2(self)
        self.ui_2.add_photo.clicked.connect(self.addImage)
        self.ui_2.edit_photo.clicked.connect(self.editPhoto)
        self.ui_2.edit_name.clicked.connect(self.editName)
        self.ui_2.close_btn.clicked.connect(self.close)
        self.ui_2.input_employ = ""
        self.ui_2.file_path = ""
        self.ui_2.new_name = ""
        self.ui_2.selection = 0
        self.ui_2.edit = Widget_1()
    def addImage(self):
        self.ui_2.file_path = filedialog.askopenfilename(title="Chọn ảnh", filetypes=(("JPEG files", "*.jpg"), ("PNG files", "*.png"), ("All files", "*.*")))
        if self.ui_2.file_path == "":
                return
        img = cv2.imread(self.ui_2.file_path)
        Image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        ConvertToQTFormat = QImage(Image.data, Image.shape[1], Image.shape[0], QImage.Format_RGB888)
        Pic = ConvertToQTFormat.scaled(591, 531)
        self.ui_2.photo.setPixmap(QPixmap.fromImage(Pic))
    def editPhoto(self):
        self.ui_2.input_employ = self.ui_2.input_name.text()
        if self.ui_2.input_employ == "" or self.ui_2.file_path=="":
                msg.ShowMsg("Info","Please check again!")
                return 
        else:
                #input_employ = input_employ.replace(" ","_")
                self.UpdateInfo(self.ui_2.input_employ, client_mng.CMD.EDITPHOTO)
    def editName(self):
        self.ui_2.input_employ = self.ui_2.input_name.text()
        if self.ui_2.input_employ == "":
                msg.ShowMsg("Info","Please check again!")
                return 
        else:
                self.ui_2.edit.old_name = self.ui_2.input_employ
                self.ui_2.edit.show()
    def UpdateInfo(self, input_employ, request):
        if request == client_mng.CMD.EDITPHOTO:
                client_mng.editPhoto(self.ui_2.file_path, input_employ)
        # elif request == mng.CMD.EDITNAME:
        #         mng.editName(input_employ, self.new_name)
class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1023, 682)
        Form.setStyleSheet("")
        self.tableView = QtWidgets.QTableView(Form)
        self.tableView.setGeometry(QtCore.QRect(0, 290, 1024, 391))
        self.tableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableView.setEditTriggers(QTableView.NoEditTriggers)
        # Thiết lập tiêu đề cột căn giữa
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableView.horizontalHeader().setDefaultAlignment(Qt.AlignCenter)
        self.tableView.setHorizontalHeader(CenteredHeaderView(Qt.Horizontal, self.tableView))
        self.tableView.resizeRowsToContents()
        self.tableView.resizeColumnsToContents()

        # # Thiết lập nội dung ô căn giữa
        self.tableView.setItemDelegate(CenteredItemDelegate())
        self.tableView.verticalHeader().setVisible(False)
        self.tableView.horizontalHeader().setVisible(False)
        self.tableView.setObjectName("tableView")
        self.time = QtWidgets.QLineEdit(Form)
        self.time.setGeometry(QtCore.QRect(120, 250, 281, 31))
        self.time.setText("")
        self.time.setObjectName("time")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(10, 260, 111, 16))
        self.label.setStyleSheet("font-size: 18px;\n"
"font-weight: 600;")
        self.label.setObjectName("label")
        self.load_csv = QtWidgets.QPushButton(Form)
        self.load_csv.setGeometry(QtCore.QRect(410, 250, 101, 31))
        self.load_csv.setStyleSheet("border-radius: 10px;\n"
"font-size: 16px;\n"
"font-weight: 500;\n"
"color: white;\n"
"background-color: gray;\n"
"")
        self.load_csv.setObjectName("load_csv")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(360, 20, 441, 31))
        self.label_2.setStyleSheet("font: 26px;\n"
"font-weight: 500;\n"
"color: white;")
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(310, 10, 41, 41))
        self.label_3.setStyleSheet("image: url(Img/Icon/management.png);")
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(0, 0, 1021, 291))
        self.label_4.setStyleSheet("background-color: #1feddc;")
        self.label_4.setText("")
        self.label_4.setObjectName("label_4")
        self.add_employ = QtWidgets.QPushButton(Form)
        self.add_employ.setGeometry(QtCore.QRect(220, 110, 181, 81))
        self.add_employ.setStyleSheet("font-size: 16px;\n"
"font-weight: 500;\n"
"color: white;\n"
"background-color: #34ed1f;\n"
"")
        self.add_employ.setObjectName("add_employ")
        self.update_employ = QtWidgets.QPushButton(Form)
        self.update_employ.setGeometry(QtCore.QRect(430, 110, 181, 81))
        self.update_employ.setStyleSheet("\n"
"font-size: 16px;\n"
"font-weight: 500;\n"
"color: white;\n"
"background-color: #1f22ed;\n"
"")
        self.update_employ.setObjectName("update_employ")
        self.remove_employ = QtWidgets.QPushButton(Form)
        self.remove_employ.setGeometry(QtCore.QRect(640, 110, 181, 81))
        self.remove_employ.setStyleSheet("\n"
"font-size: 16px;\n"
"font-weight: 500;\n"
"color: white;\n"
"background-color: #f0ca0c;\n"
"")
        self.remove_employ.setObjectName("remove_employ")
        self.close_btn= QtWidgets.QPushButton(Form)
        self.close_btn.setGeometry(QtCore.QRect(950, 20, 41, 31))
        self.close_btn.setStyleSheet("\n"
"font-size: 16px;\n"
"font-weight: 500;\n"
"color: white;\n"
"background-color: red;\n"
"")
        self.close_btn.setObjectName("close_btn")
        self.label_4.raise_()
        self.tableView.raise_()
        self.time.raise_()
        self.label.raise_()
        self.load_csv.raise_()
        self.label_2.raise_()
        self.label_3.raise_()
        self.add_employ.raise_()
        self.update_employ.raise_()
        self.remove_employ.raise_()
        self.close_btn.raise_()
        self.ui_1 = Admin_UI()
        self.ui_2 = Edit_UI()
        self.ui_3 = Widget_2()
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.DisplayNewestCSV)
        self.timer.start(10000)
        self.load_csv.clicked.connect(self.loadCSV)
        self.add_employ.clicked.connect(self.openAdd)
        self.update_employ.clicked.connect(self.openEdit)
        self.remove_employ.clicked.connect(self.openRM)
        self.close_btn.clicked.connect(QCoreApplication.instance().quit)
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Enter time:"))
        self.load_csv.setText(_translate("Form", "Load CSV"))
        self.label_2.setText(_translate("Form", "WORKER MANAGER APPLICATION "))
        self.add_employ.setText(_translate("Form", "ADD EMPLOYEE"))
        self.update_employ.setText(_translate("Form", "UPDATE EMPLOYEE"))
        self.remove_employ.setText(_translate("Form", "REMOVE EMPLOYEE"))
        self.close_btn.setText(_translate("Form", "X"))

    def loadCSV(self):
        self.model = QStandardItemModel()
        time = self.time.text()
        day = now.day
        month = now.month
        year = now.year
        if time=="":
           if day < 10:
                time = str(month) + "-0" + str(day) + "-" + str(year)
           elif month < 10:
                time = "0" +str(month) + "-" + str(day) + "-" + str(year)
           else:
                time = "0" +str(month) + "-" + str(day) + "-" + str(year)
        # Đọc dữ liệu từ file csv và thêm vào model
        with open('report/report_' + time + '.csv', newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row_data in reader:
                row = []
                for item_data in row_data:
                    item = QStandardItem(item_data)
                    row.append(item)
                self.model.appendRow(row)
        for i in range(self.model.columnCount()):
            for j in range(self.model.rowCount()):
                item = self.model.item(j, i)
                if item is not None:
                    font = QFont()
                    font.setBold(True)
                    item.setFont(font)
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableView.resizeColumnsToContents()
        self.tableView.setModel(self.model)
        
    def DisplayNewestCSV(self):
        client_mng.UpdateCSV()
        self.model = QStandardItemModel()
        # Đọc dữ liệu từ file csv và thêm vào model
        with open('CLIENT/admin_gui/csv_file/now_csv.csv', newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row_data in reader:
                row = []
                for item_data in row_data:
                    item = QStandardItem(item_data)
                    row.append(item)
                self.model.appendRow(row)
        for i in range(self.model.columnCount()):
            for j in range(self.model.rowCount()):
                item = self.model.item(j, i)
                if item is not None:
                    font = QFont()
                    font.setBold(True)
                    item.setFont(font)
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableView.resizeColumnsToContents()
        self.tableView.setModel(self.model)

    def openAdd(self):
         self.ui_1.show()
    def openEdit(self):
         self.ui_2.show()
    def openRM(self):
         self.ui_3.show()
        

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
