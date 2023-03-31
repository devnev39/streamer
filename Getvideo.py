import cv2
import threading
class GetVideo:
    def __init__(self,file : str = '0'):
        self.cap = cv2.VideoCapture(0 if file == '0' else file)
        self.stopVideo = False
        (self.ret,self.frame) = self.cap.read()
        self.detector = cv2.CascadeClassifier('clf.xml')
        modelFile = "res10_300x300_ssd_iter_140000.caffemodel"
        configFile = "deploy.prototxt.txt"
        self.net = cv2.dnn.readNetFromCaffe(configFile, modelFile)
        self.conf_threshold = 0.5
        self.frame_layer = None

    
    def gray_scale(self):
        self.frame_layer = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)

    def run_face_detection(self,model : str) -> list:
        if model == "hc":
            self.gray_scale()
            return self.detector.detectMultiScale(self.frame_layer if self.frame_layer else self.frame,1.3,5)
        elif model == "cvdnn":
            blob = cv2.dnn.blobFromImage(self.frame, 1.0, (300, 300), [104, 117, 123], False, False)
            self.net.setInput(blob)
            detections = self.net.forward()
            faces = []
            for i in range(detections.shape[2]):
                confidence = detections[0, 0, i, 2]
                if confidence > self.conf_threshold:
                    x1 = int(detections[0, 0, i, 3] * self.frame.shape[1])
                    y1 = int(detections[0, 0, i, 4] * self.frame.shape[0])
                    x2 = int(detections[0, 0, i, 5] * self.frame.shape[1])
                    y2 = int(detections[0, 0, i, 6] * self.frame.shape[0])
                    faces.append([x1,y1,x2-x1,y2-y1])
            return faces
        return []
        
    def detect_faces(self):
        faces = self.run_face_detection('hc')
        for x,y,w,h in faces:
            cv2.rectangle(self.frame,(x,y),(x+w,y+h),(0,255,0),2)
            
    def get(self):
        while True:
            if not self.ret or self.stopVideo:
                break
            (self.ret,self.frame) = self.cap.read()
            self.detect_faces()    
    
    def stop(self):
        self.stopVideo = True

    def start(self):
        threading.Thread(target=self.get).start()