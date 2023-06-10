from PyQt5.QtWidgets import  QWidget, QLabel, QApplication
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
import datetime
import time
import cv2
import util
import report
import os

# months = ["Tháng 1", "Tháng 2", "Tháng 3", "Tháng 4", "Tháng 5", "Tháng 6", "Tháng 7"
#           , "Tháng 8", "Tháng 9", "Tháng 10", "Tháng 11", "Tháng 12"]
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
          'August', 'September', 'October', 'November', 'December']
class Video(QThread):
    ImageUpdate = pyqtSignal(QImage)
    frame = 0
    height = 0
    width = 0
    date_str = ""
    file_path = ""
    block = False
    def run(self):
            font = cv2.FONT_HERSHEY_COMPLEX_SMALL
            #FPS
            start_time = time.time()
            display_time = 2
            fc = 0
            FPS = 0
            while True:
                _, frame = self.cap.read()
                try: 
                    height, width, channels = frame.shape
                except:
                    self.cap = cv2.VideoCapture("Img/loading/loading.mp4")
                    _, frame = self.cap.read()
                    height, width, channels = frame.shape
                if not self.block:
                    self.frame = frame
                    self.width = width
                    self.height = height

                    fc += 1
                    TIME = time.time() - start_time
                    if (TIME) >= display_time :
                        FPS = fc / (TIME)
                        fc = 0
                        start_time = time.time()

                    fps_disp = "FPS: " + str(FPS)[:3]   
                    date_now = datetime.date.today()

                    # Format time as string
                    date_str = date_now.strftime("%B-%d-%Y")
                    date_temp = date_str.split("-")
                    tmp = str(months.index(date_temp[0]) + 1)
                    if len(tmp) < 2:
                        tmp = '0' + tmp
                        
                    date_str = date_str.replace(date_temp[0],tmp)
                    self.date_str = date_str
                    file_path = "report/report_" + date_str+ ".csv"
                    self.file_path = file_path

                    # Check if the file exists
                    if not os.path.exists(file_path):
                        report.create_report(file_path)

                    # Add FPS count on frame
                    image = cv2.putText(frame, fps_disp, (10, 25),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                    
                    face_locations = util.face_detect(image)
                    for face_loc in face_locations:
                        y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]
                        frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 200), 4)
                self.process(frame)

    def process(self,frame):   
        Image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        ConvertToQTFormat = QImage(Image.data, Image.shape[1], Image.shape[0], QImage.Format_RGB888)
        Pic = ConvertToQTFormat.scaled(731, 551)
        self.ImageUpdate.emit(Pic)

    def Stop(self):
        self.quit()


