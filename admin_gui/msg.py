from PyQt5.QtWidgets import QMessageBox

def ShowMsg(title,testMsg):
    dlg = QMessageBox()
    dlg.setIcon(QMessageBox.Information)
    dlg.setText(testMsg + "              ")
    dlg.setWindowTitle(title)
    dlg.setStandardButtons(QMessageBox.Ok)
    dlg.exec()