
from flask import Flask, render_template, Response, request
from camera import VideoCamera
from camera import TimeLapse
import time
import threading
import os

#pi_camera = VideoCamera() # flip pi camera if upside down.

# Ensure only vids folder is accessible to prevent all files from being accessed remotely
app = Flask(__name__, static_folder='vids')

@app.route('/')
def awjfuqhfaifjifw():
    return render_template('homepage.html') #you can customze index.html here

#@app.route('/livestream')
#def index():
   # return render_template('livestream.html') #you can customze index.html here

@app.route('/timelapse')
def aehufijf3ua():
    return render_template('timelapse.html') #you can customze index.html here

def gen(camera):
    #get camera frame
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')



if __name__ == '__main__':
    timelapseobj = TimeLapse()
    threading.Thread(target=timelapseobj.image_capturer).start()
    threading.Thread(target=timelapseobj.compose_timelapse).start()


    app.run(host='0.0.0.0', debug=False)
    

