from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from camera import Camera
import uvicorn
import time
import cv2
from Getvideo import GetVideo
from pyngrok import ngrok

app = FastAPI()

p_frame = 0
stream_thread_started = False
cap = None
    
def putFPS(frame, fps):
    """
    Add iterations per second text to lower-left corner of a frame.
    """

    cv2.putText(frame, "{:.0f} fps".format(fps),
        (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 2.0, (0, 255, 0))
    return frame

def gen(camera : Camera):
    global cap
    global p_frame
    global stream_thread_started

    if not stream_thread_started or cap == None:
        cap = GetVideo(camera.uri)
        cap.start()
        stream_thread_started = True
    
    while True:
        try:
            c_frame = time.time()
            f_rate = 1 / (c_frame - p_frame)
            frame = cap.frame
            _ , frame = cv2.imencode(".jpg",putFPS(cap.frame,round(f_rate)))
            frame = frame.tobytes()
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            p_frame = c_frame
            print(round(f_rate))
        except Exception as ex:
            print(ex)
            cap.stop()
            stream_thread_started = False
            break
        # cv2.waitKey(20)
        

@app.get("/{uri}/{model}/video")
async def videoFeed(uri : str,model:str):
    return  StreamingResponse(gen(Camera("http://192.168.0.100:8080/video" if uri == "cam" else uri,"" if model=="NONE" else model)),
                    media_type='multipart/x-mixed-replace; boundary=frame')


if __name__=="main":
    uvicorn.run("app:app --reload",port=8000,log_level="info")
    addr = ngrok.connect(8000,"http")
    print(addr)

# JWT auth
# Header authentication
# Asyc progd
