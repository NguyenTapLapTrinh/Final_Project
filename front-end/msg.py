from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QIcon
def ShowMsg(title,testMsg):
    dlg = QMessageBox()
    dlg.setIcon(QMessageBox.Information)
    dlg.setText(testMsg + "              ")
    dlg.setWindowTitle(title)
    dlg.setStandardButtons(QMessageBox.Ok)
    dlg.exec()
def ShowChoose(title, body, textYes, textNo):
    icon_path = "Img/Icon/camera.png"
    icon = QIcon(icon_path)
    msg = QMessageBox()
    msg.setIconPixmap(icon.pixmap(64, 64))
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