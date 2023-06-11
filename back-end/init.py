import yolo_detection
import os

classes_vn = ["Mũ bảo hiểm", "Áo bảo hộ", "Găng tay bảo hộ"]
classes = []

def ServerInit():
    l_directory = ['db','temp','report']
    s_file = "db/name.txt"

    for directory in l_directory:
        if not os.path.exists(directory):
            os.mkdir(directory)

    if not os.path.exists(s_file):
        with open(s_file, "wb") as file:
            pass


def YoloInit():
    with open("coco.names", "r") as f:
        classes = [line.strip() for line in f.readlines()]

    yolo = yolo_detection.Yolo(classes)
    yolo.loadWeight("weight/yolov4_training_last.weights","weight/yolov4_testing.cfg")

    return yolo