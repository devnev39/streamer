Streamer is a fastapi backend performing face detection based on the request url

url format : http://localhost:8000/URI/model/video

**URI**<br>
    represents the offline video file name or
    cam if you want stream ip webcam hosted from a smartphone

**model**<br>
    represents the model to apply to each frame 
    can be hc for cascade classifier
    can be cvdnn for dnn
    can be fcr for face_recognition library