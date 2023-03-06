import os.path
import pickle
import cv2
import face_recognition
import time



if __name__ == "__main__":
    name = "SonTung"

    frame = cv2.imread('Img/data_test/ST.jpg')
    try:
        embeddings = face_recognition.face_encodings(frame)[0]
    except:
       print("Cant detect human face !\nAre you a human ???")
    else:
        with open(os.path.join('./db', '{}.pickle'.format(name)), 'wb') as file:
            pickle.dump(embeddings, file)
        





