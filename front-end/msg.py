from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QIcon
def ShowMsg(title,testMsg):
    if title == "Warning":
         icon_path = "Img/Icon/cross.png"
    elif title == 'Info':
         icon_path = "Img/Icon/info.png"
    icon = QIcon(icon_path)
    dlg = QMessageBox()
    dlg.setWindowIcon(icon)
    dlg.setIcon(QMessageBox.Information)
    dlg.setText(testMsg + "              ")
    dlg.setWindowTitle(title)
    dlg.setStandardButtons(QMessageBox.Ok)
    dlg.exec()
def ShowChoose(title, body, textYes, textNo, type = 'trash'):
    if type == 'refresh':
          icon_path = "Img/Icon/refresh.png"
    else:
         icon_path = "Img/Icon/trash.png"
    icon = QIcon(icon_path)
    msg = QMessageBox()
    msg.setWindowIcon(icon)
    msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    buttonY = msg.button(QMessageBox.Yes)
    buttonY.setText(textYes)
    buttonN = msg.button(QMessageBox.No)
    buttonN.setText(textNo)
    msg.setIcon(QMessageBox.Question)
    msg.setWindowTitle(title)
    msg.setText(body)
    msg.exec_()
    button = msg.clickedButton()
    sb = msg.standardButton(button)
    if sb == QMessageBox.Yes:
            return 1
    else: 
            return 2