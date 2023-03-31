from multiprocessing import freeze_support
import cv2
import time
import numpy as np
import concurrent.futures
import threading

fps = 0

cam = cv2.VideoCapture("ss.mov")
detector = cv2.CascadeClassifier("clf.xml")
g_frame = None

modelFile = "res10_300x300_ssd_iter_140000.caffemodel"
configFile = "deploy.prototxt.txt"
net = cv2.dnn.readNetFromCaffe(configFile, modelFile)

conf_threshold = 0.5

def get_frame(text : str = ""):
    _,frame = cam.read()
    cv2.putText(frame,text,(0,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2,cv2.LINE_AA)
    return frame

def resize(data : list):
    return cv2.resize(data[0],data[1],fy=data[2][1],fx=data[2][0])

def gray(frame):
    return cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

def run_face_detection(params : list) -> list:
    frame,model = params
    if model == "hc":
        return detector.detectMultiScale(frame,1.3,5)
    elif model == "cvdnn":
        blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300), [104, 117, 123], False, False)
        net.setInput(blob)
        detections = net.forward()
        faces = []
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > conf_threshold:
                x1 = int(detections[0, 0, i, 3] * frame.shape[1])
                y1 = int(detections[0, 0, i, 4] * frame.shape[0])
                x2 = int(detections[0, 0, i, 5] * frame.shape[1])
                y2 = int(detections[0, 0, i, 6] * frame.shape[0])
                faces.append([x1,y1,x2-x1,y2-y1])
        return faces
    return []

def process_frame(frame):
    g_frame = gray(frame)
    faces = run_face_detection([g_frame,"hc"])
    for x,y,w,h in faces:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
    return frame
    

def frame_generator(text : str = ""):
    while True:
        frame = get_frame(str(fps))
        yield frame

def process_on_thread():
    pass

if __name__ == '__main__':
    pass