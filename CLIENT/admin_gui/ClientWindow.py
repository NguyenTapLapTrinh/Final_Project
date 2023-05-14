# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Client__Window.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
import sys
sys.path.append("./back-end")
sys.path.append("./front-end")
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QModelIndex, QTimer
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QColor, QStandardItemModel, QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableView,  QStyledItemDelegate, QHeaderView, QAbstractItemView
import csv
from datetime import datetime
from admin import *
from edit import *
from editline import *
from list_name import *
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
import image_main
import datetime
now = datetime.datetime.now()
timer = QtCore.QTimer()
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
        global timer
        timer.stop()
        if request == client_mng.CMD.ADD: 
                client_mng.setData(self.ui_1.file_path,input_employ)
        elif request == client_mng.CMD.DEL:
                client_mng.deleteData(input_employ)
        timer.start()
    def addEmploy(self):
        input_employ = self.ui_1.input_name.text()
        if input_employ == "" or self.ui_1.file_path=="":
                msg.ShowMsg("Info","Please check again!")
                return 
        else:
                #input_employ = input_employ.replace(" ","_")
                self.EditInfo(input_employ, client_mng.CMD.ADD)
class List_UI(QDialog):
    def __init__(self, parent=None):
        super(List_UI, self).__init__(parent)
        self.ui_4 = Ui_Form_4()
        self.ui_4.setupUi_4(self)
        self.ui_4.close_btn.clicked.connect(self.close)
        self.ui_4.rm_btn.clicked.connect(self.removeEmploy)
        self.array_employee = []
    def load_employee(self):
        global timer
        timer.stop()
        self.ui_4.listWidget.clear() 
        self.array_employee = client_mng.RequestEmployee()
        if self.array_employee == -1:
            return -1
        for item in self.array_employee:
            font = QFont()
            font.setPointSize(12)
            font.setBold(True)
            if item == '':
                 break
            item = QListWidgetItem(str(item))
            item.setFont(font)
            self.ui_4.listWidget.addItem(item)
        timer.start()
    def removeEmploy(self):
         global timer
         current_row = self.ui_4.listWidget.currentRow()
         nameDelete = self.ui_4.listWidget.item(current_row).text()
         if current_row>=0:
            body = "Are you sure to remove "+ nameDelete
            choose = msg.ShowChoose("Remove Employee",body, "Yes", "No")
            if choose ==1:
                timer.stop()
                check = client_mng.deleteData(nameDelete)
                timer.start()
            else:
                 return
         else: 
            return
         if check == 0:
            return
         self.load_employee()
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
        global timer
        if request == client_mng.CMD.EDITPHOTO:
                timer.stop()
                client_mng.editPhoto(self.ui_2.file_path, input_employ)
                timer.start()
class Ui_Form(object):
    global timer
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1022, 703)
        Form.setStyleSheet("background-color: #bed9bd\n"
"")
        self.tableView = QtWidgets.QTableView(Form)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.tableView.setFont(font)
        self.tableView.setGeometry(QtCore.QRect(10, 180, 811, 511))
        self.tableView.setStyleSheet("border: 2px solid black;\n"
"background-color: #fff;")
        self.tableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableView.setEditTriggers(QTableView.NoEditTriggers)
        self.tableView.horizontalHeader().setDefaultAlignment(Qt.AlignCenter)
        self.tableView.setHorizontalHeader(CenteredHeaderView(Qt.Horizontal, self.tableView))
        self.tableView.resizeRowsToContents()
        self.tableView.resizeColumnsToContents()
        self.tableView.setItemDelegate(CenteredItemDelegate())
        self.tableView.verticalHeader().setVisible(False)
        self.tableView.horizontalHeader().setVisible(False)
        self.tableView.setObjectName("tableView")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(310, 140, 121, 31))
        self.label.setStyleSheet("font-size: 16px;\n"
"font-weight: 500;\n"
"background-color: #8ffbff;")
        self.label.setObjectName("label")
        self.timeCSV = QtWidgets.QLabel(Form)
        self.timeCSV.setGeometry(QtCore.QRect(70, 140, 221, 31))
        self.timeCSV.setStyleSheet("font-size: 16px;\n"
"font-weight: 500;\n"
"border: 1px solid black;\n"
"padding: 4px 2px;\n"
"background-color: #fff;")
        self.timeCSV.setText("")
        self.timeCSV.setObjectName("timeCSV")
        self.timeEdit = QtWidgets.QLineEdit(Form)
        self.timeEdit.setGeometry(QtCore.QRect(430, 140, 291, 31))
        self.timeEdit.setStyleSheet("font-size: 16px;\n"
"font-weight: 500;\n"
"border-radius: 6px;\n"
"background-color: #fff;")
        self.timeEdit.setText("")
        self.timeEdit.setObjectName("timeEdit")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(20, 140, 41, 31))
        self.label_2.setStyleSheet("image: url(:/calendar/schedule.png);\n"
"font-size: 16px;\n"
"font-weight: 500;\n"
"background-color: #8ffbff;")
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.loadCSV = QtWidgets.QPushButton(Form)
        self.loadCSV.setGeometry(QtCore.QRect(730, 140, 91, 31))
        self.loadCSV.setStyleSheet("font-size: 14px;\n"
"font-weight: 500;\n"
"background-color: #5af745;\n"
"color: #fff;")
        self.loadCSV.setObjectName("loadCSV")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(0, 80, 841, 621))
        self.label_3.setStyleSheet("background-color: #8ffbff;\n"
"color: red;")
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(20, 90, 311, 21))
        self.label_4.setStyleSheet("font-size: 20px;\n"
"font-weight: 600;\n"
"color: red;\n"
"background-color: #8ffbff;")
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setGeometry(QtCore.QRect(310, 20, 501, 41))
        self.label_5.setStyleSheet("font-size: 24px;\n"
"font-weight: 600;\n"
"color: #fff;")
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(Form)
        self.label_6.setGeometry(QtCore.QRect(220, 10, 91, 61))
        self.label_6.setStyleSheet("image: url(:/icon/helmet-icon.png);")
        self.label_6.setText("")
        self.label_6.setObjectName("label_6")
        self.listEmploy = QtWidgets.QPushButton(Form)
        self.listEmploy.setGeometry(QtCore.QRect(910, 160, 71, 71))
        self.listEmploy.setToolTip("")
        self.listEmploy.setStyleSheet("background-color: #cc66ff;\n"
"border-radius: 20px;\n"
"border: 2px solid #fff;")
        self.listEmploy.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icon/checklist.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.listEmploy.setIcon(icon)
        self.listEmploy.setIconSize(QtCore.QSize(55, 55))
        self.listEmploy.setObjectName("listEmploy")
        self.label_7 = QtWidgets.QLabel(Form)
        self.label_7.setGeometry(QtCore.QRect(850, 80, 171, 631))
        self.label_7.setStyleSheet("background-color: #575cff;\n"
"border-top-left-radius: 50px;")
        self.label_7.setText("")
        self.label_7.setObjectName("label_7")
        self.closeBtn = QtWidgets.QPushButton(Form)
        self.closeBtn.setGeometry(QtCore.QRect(900, 660, 91, 31))
        self.closeBtn.setStyleSheet("color: #fff;\n"
"background-color: red;\n"
"font: 16px;\n"
"font-weight: 600;")
        self.closeBtn.setObjectName("closeBtn")
        self.addEmploy = QtWidgets.QPushButton(Form)
        self.addEmploy.setGeometry(QtCore.QRect(910, 300, 71, 71))
        self.addEmploy.setStyleSheet("background-color: #b7f01a;\n"
"border-radius: 20px;\n"
"border: 2px solid #fff;")
        self.addEmploy.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icon/add.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon1.addPixmap(QtGui.QPixmap(":/icon/add.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.addEmploy.setIcon(icon1)
        self.addEmploy.setIconSize(QtCore.QSize(55, 55))
        self.addEmploy.setObjectName("addEmploy")
        self.updateEmploy = QtWidgets.QPushButton(Form)
        self.updateEmploy.setGeometry(QtCore.QRect(910, 440, 71, 71))
        self.updateEmploy.setStyleSheet("background-color:#f7983e;\n"
"border-radius: 20px;\n"
"border: 2px solid #fff;")
        self.updateEmploy.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icon/setting.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.updateEmploy.setIcon(icon2)
        self.updateEmploy.setIconSize(QtCore.QSize(55, 55))
        self.updateEmploy.setObjectName("updateEmploy")
        self.label_8 = QtWidgets.QLabel(Form)
        self.label_8.setGeometry(QtCore.QRect(920, 100, 61, 20))
        self.label_8.setStyleSheet("background-color: #575cff;\n"
"color: yellow;\n"
"font-size: 20px;\n"
"font-weight: 500;")
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(Form)
        self.label_9.setGeometry(QtCore.QRect(890, 240, 111, 20))
        self.label_9.setStyleSheet("color: white;\n"
"font-size: 14px;\n"
"font-weight: 500;\n"
"background-color: #575cff;")
        self.label_9.setObjectName("label_9")
        self.label_10 = QtWidgets.QLabel(Form)
        self.label_10.setGeometry(QtCore.QRect(890, 380, 111, 20))
        self.label_10.setStyleSheet("background-color: #575cff;\n"
"color: white;\n"
"font-size: 14px;\n"
"font-weight: 500;")
        self.label_10.setObjectName("label_10")
        self.label_11 = QtWidgets.QLabel(Form)
        self.label_11.setGeometry(QtCore.QRect(890, 520, 100, 20))
        self.label_11.setStyleSheet("color: white;\n"
"font-size: 14px;\n"
"font-weight: 500;\n"
"background-color: #575cff;")
        self.label_11.setObjectName("label_11")
        self.label_7.raise_()
        self.label_3.raise_()
        self.tableView.raise_()
        self.label.raise_()
        self.timeCSV.raise_()
        self.timeEdit.raise_()
        self.label_2.raise_()
        self.loadCSV.raise_()
        self.label_4.raise_()
        self.label_5.raise_()
        self.label_6.raise_()
        self.listEmploy.raise_()
        self.closeBtn.raise_()
        self.addEmploy.raise_()
        self.updateEmploy.raise_()
        self.label_8.raise_()
        self.label_9.raise_()
        self.label_10.raise_()
        self.label_11.raise_()
        self.current_date = now.strftime("%d-%m-%Y")
        self.ui_1 = Admin_UI()
        self.ui_2 = Edit_UI()
        self.ui_4 = List_UI()
        self.lock = 0
        self.DisplayNewestCSV()
        timer.timeout.connect(self.DisplayNewestCSV)
        timer.start(10000)
        self.array_employ = []
        self.ui_4 = List_UI()
        self.timeCSV.setText(self.current_date)
        self.closeBtn.clicked.connect(QCoreApplication.instance().quit)
        self.listEmploy.clicked.connect(self.loadEmploy)
        self.loadCSV.clicked.connect(self.load_CSV)
        self.addEmploy.clicked.connect(self.openAdd)
        self.updateEmploy.clicked.connect(self.openEdit)
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Worker Manager"))
        Form.setWindowIcon(QIcon("./Img/Icon/icon.png"))
        self.label.setText(_translate("Form", "Change Time:"))
        self.loadCSV.setText(_translate("Form", "LOAD"))
        self.closeBtn.setText(_translate("Form", "EXIT"))
        self.label_4.setText(_translate("Form", "CHECKING WORKER PRESENT"))
        self.label_5.setText(_translate("Form", "WORKER MANAGERMENT APPLICATION"))
        self.label_8.setText(_translate("Form", "MENU"))
        self.label_9.setText(_translate("Form", "LIST EMPLOYEE"))
        self.label_10.setText(_translate("Form", "ADD EMPLOYEE"))
        self.label_11.setText(_translate("Form", "UPDATE INFO"))
    def loadEmploy(self):
        timer.stop()
        check = self.ui_4.load_employee()
        if check == -1:
             return
        self.ui_4.show()
    def load_CSV(self):
        time_str = self.timeEdit.text()
        time_array = time_str.split("-")
        print(time_array)
        current_date = now.strftime("%d-%m-%Y")
        current_time_array = current_date.split("-")
        print(current_time_array)
        if int(time_array[2]) > int(current_time_array[2]):
             msg.ShowMsg("Warning","Not suitable time!")
             return
        elif int(time_array[1]) > int(current_time_array[1]):
             msg.ShowMsg("Warning","Not suitable time!")
             return 
        elif int(time_array[1]) == int(current_time_array[1]) and int(time_array[0]) > int(current_time_array[0]):
             msg.ShowMsg("Warning","Not suitable time!")
             return 
        if time_str =="":
             msg.ShowMsg("Info","Please check again!")
             return
        stop_timer = client_mng.receiveCSV(str(time_array[1] + "-" + time_array[0] + "-" + time_array[2]))
        if stop_timer == -1:
            return
        if stop_timer == 1:
            timer.stop()
        else:
            timer.stop()
            timer.start()
        self.model = QStandardItemModel()
        # Đọc dữ liệu từ file csv và thêm vào model
        if os.path.exists("CLIENT/admin_gui/csv_file/current_csv.csv"):
            self.timeCSV.setText(self.timeEdit.text())    
            with open("CLIENT/admin_gui/csv_file/current_csv.csv", encoding= 'utf8',newline='') as csvfile:
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
            os.remove("CLIENT/admin_gui/csv_file/current_csv.csv")
    def DisplayNewestCSV(self):
        self.lock = 1
        check = client_mng.UpdateCSV()
        if check == 0:
             return
        self.model = QStandardItemModel()
        # Đọc dữ liệu từ file csv và thêm vào model
        with open('CLIENT/admin_gui/csv_file/now_csv.csv', newline='', encoding='utf8') as csvfile:
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
        os.remove("CLIENT/admin_gui/csv_file/now_csv.csv")
        self.lock = 0
    def openAdd(self):
        if self.lock == 1:
              msg.ShowMsg("Warning","Server is busy, try again!")
              return
        self.ui_1.show()
    def openEdit(self):
        if self.lock == 1:
              msg.ShowMsg("Warning","Server is busy, try again!")
              return
        self.ui_2.show()
#     def openRM(self):
#         if self.lock == 1:
#               msg.ShowMsg("Warning","Server is busy, try again!")
#               return
#         self.ui_3.show()

if __name__ == "__main__":
    import sys
    Fail = 1
    number = 0
    while(Fail):
        result = client_mng.get_ip_address()
        if result == None:
            number += 1
            if number > 3:
                msg.ShowMsg("Warning","Server not found")
                exit(0)
            msg.ShowMsg("Warning",f"Server not found, try again!\nTry reconnect {number} attempt!")
        else:
            Fail = 0
             
             
    
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
