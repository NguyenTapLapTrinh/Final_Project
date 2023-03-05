from PyQt5.QtWidgets import  QWidget, QLabel, QApplication
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
import cv2

class Video(QThread):
    ImageUpdate = pyqtSignal(QImage)
    def process(self,frame):    
        Image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        ConvertToQTFormat = QImage(Image.data, Image.shape[1], Image.shape[0], QImage.Format_RGB888)
        Pic = ConvertToQTFormat.scaled(731, 551, Qt.KeepAspectRatio)
        self.ImageUpdate.emit(Pic)

    def Stop(self):
        self.quit()


