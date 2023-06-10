import numpy as np
import cv2

class Yolo():
    def __init__(self,classes):
        self.classes = classes

    def setVar(self,frame,width,height):
        self.frame = frame
        self.width = width
        self.height = height

    def loadWeight(self,weight,cfg):
        self.net = cv2.dnn.readNet(weight, cfg)
        layer_names = self.net.getLayerNames()
        self.output_layers = [layer_names[i - 1] for i in self.net.getUnconnectedOutLayers()]

    def objectDetect(self):
        blob = cv2.dnn.blobFromImage(self.frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)

        self.net.setInput(blob)
        outs = self.net.forward(self.output_layers)
        class_ids = []
        confidences = []
        boxes = []
        empty = [0,1,2]

        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.8:
                    # Object detected
                    center_x = int(detection[0] * self.width)
                    center_y = int(detection[1] * self.height)
                    w = int(detection[2] * self.width)
                    h = int(detection[3] * self.height)

                    # Rectangle coordinates
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)

                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id) 

        for i in class_ids:
            try:
                empty.remove(i)
            except:
                continue
        
        return empty
    
    def getFrame(self):
        return self.frame