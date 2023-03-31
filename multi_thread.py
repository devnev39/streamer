import cv2
from FPS import FPS
from Getvideo import GetVideo

def putFPS(frame, fps):
    """
    Add iterations per second text to lower-left corner of a frame.
    """

    cv2.putText(frame, "{:.0f} fps".format(fps),
        (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 2.0, (0, 255, 0))
    return frame

def non_threading():
    cap = cv2.VideoCapture(0)
    fps = FPS().start()

    while True:
        ret,frame = cap.read()
        if not ret or cv2.waitKey(1) == ord('q'):
            break
        putFPS(frame,fps.fps())
        cv2.imshow('frame',frame)
        fps.increment()

def with_threading():
    cap = GetVideo('two.mp4')    
    cap.start()
    fps = FPS().start()
    while True:
        if not cap.ret or cv2.waitKey(1) == ord('q'):
            cap.stop()
            break
        frame = cap.frame
        frame = putFPS(frame,fps.fps())
        cv2.imshow('frame',frame)
        fps.increment()

with_threading()