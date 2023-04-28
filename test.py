from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import time

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('GIF Example')

        self.label = QLabel(self)
        self.movie = QMovie("Img/loading/loading.gif")
        self.label.setMovie(self.movie)

        # tạo một nút để kích hoạt hàm
        self.button = QPushButton('Run Function', self)
        self.button.move(50, 100)
        self.button.clicked.connect(self.runFunction)

        self.show()

    def runFunction(self):
        # tạo một thread riêng để chạy gif
        self.thread = QThread()
        self.worker = Worker()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.thread.start()

        # thực hiện các công việc trong hàm
        time.sleep(5)

        # kết thúc thread và dừng gif
        self.worker.stop()
        self.thread.quit()
        self.thread.wait()
        self.label.setPixmap(QPixmap())

class Worker(QObject):
    finished = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.is_running = True

    def run(self):
        self.movie = QMovie("loading.gif")
        self.movie.start()
        while self.is_running:
            self.label.setMovie(self.movie)
        self.movie.stop()
        self.finished.emit()

    def stop(self):
        self.is_running = False