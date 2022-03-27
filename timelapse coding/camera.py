

import cv2
from imutils.video.pivideostream import PiVideoStream
import time
import numpy as np
from picamera import PiCamera
import os
from datetime import datetime,timedelta
import os
import moviepy.video.io.ImageSequenceClip
import queue

class TimeLapse(object):
    def __init__(self,interval=200,directory="vids/",video_name="timelapse.mp4",fps=4):
        self.interval = interval
        self.directory = directory
        self.video_name = video_name
        self.fps = fps
        self.signalqueue = queue.Queue()

        """self.num = 0
        for filename in os.scandir(self.directory):
            if filename.is_file():
                realfilename = filename.split(directory + "/")[1]
                try:
                    num = int(realfilename)
                    if num > self.num:
                        self.num = num
                except Exception as e:
                    print(e)"""

    
    def compose_timelapse(self):
        while True:
            try:
                self.signalqueue.get(timeout=300)
            
                image_files = [os.path.join(self.directory,img)for img in os.listdir(self.directory)if img.endswith(".jpg")]
                image_files.sort(key=lambda x: os.path.getmtime(x))
                clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(image_files, fps=self.fps)
                clip.write_videofile(self.directory + "alt.mp4")
                os.remove(self.directory + self.video_name)
                os.rename(self.directory + "alt.mp4", self.directory + self.video_name)
            except:
                pass
                
            
    
    def image_capturer(self):
        camera = PiCamera()
        time.sleep(2.0)
        for filename in camera.capture_continuous(self.directory + 'img{timestamp:%Y-%m-%d-%H-%M-%S}.jpg'):
            print(f"Captured {filename} for timelapse")
            self.signalqueue.put("OK")
            time.sleep(self.interval)




class VideoCamera(object):
    def __init__(self, flip = False):
        self.vs = PiVideoStream().start()
        self.flip = flip
        time.sleep(2.0)

    def __del__(self):
        self.vs.stop()

    def flip_if_needed(self, frame):
        if self.flip:
            return np.flip(frame, 0)
        return frame

    def get_frame(self):
        frame = self.flip_if_needed(self.vs.read())
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()

