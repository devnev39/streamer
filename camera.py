import cv2
import face_recognition
import threading

class Camera:
    def __init__(self,uri:str,model:str):
        """
        model : hc or fcr
        """
        self.uri = uri
        self.cam = cv2.VideoCapture(uri)
        self.detector = cv2.CascadeClassifier("clf.xml")
        self.model = model
        _,self.frame = self.cam.read()
        self.stopVideo = False
        # self.bytes = cv2.imencode()
    
    def __del__(self):
        self.cam.release()

    def get_single_frame(self):
        _, frame = self.cam.read()
        return frame
    
    def process_single_frame(self,frame):
        grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if not self.model:
            ret,jpeg = cv2.imencode(".jpg",frame)
            return jpeg.tobytes()
        
        if self.model == "hc":
            faces = self.detector.detectMultiScale(grey,1.3,5)
            for x,y,w,h in faces:
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
        
        if self.model == "fcr":
            faces = face_recognition.face_locations(grey)
            for top,right,bottom,left in faces:
                cv2.rectangle(grey,(left,top),(right,bottom),(0,255,0),2)
        return frame
    
    def get_fram(self,text : str):
        _ , frame = self.cam.read()
        frame = cv2.resize(frame,(int(frame.shape[1]/2),int(frame.shape[0]/2)))
        grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if not self.model:
            cv2.putText(frame,text,(0,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2,cv2.LINE_AA)
            ret,jpeg = cv2.imencode(".jpg",frame)
            return jpeg.tobytes()
        
        if self.model == "hc":
            faces = self.detector.detectMultiScale(grey,1.3,5)
            for x,y,w,h in faces:
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
        
        if self.model == "fcr":
            faces = face_recognition.face_locations(grey)
            for top,right,bottom,left in faces:
                cv2.rectangle(grey,(left,top),(right,bottom),(0,255,0),2)
        cv2.putText(frame,text,(0,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2,cv2.LINE_AA)
        ret, jpeg = cv2.imencode(".jpg",frame)
        return jpeg.tobytes()
    
    def start(self,*args):
        threading.Thread(target=self.get_fram,args=args).start()
    
    def stop(self):
        self.stopVideo = True