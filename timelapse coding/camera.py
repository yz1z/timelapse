

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


## Create timelapse object
class TimeLapse(object):
    ## Set interval and directory where videos will be saved and frames per second
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

    
    ## Composes a timelapse as soon as picture is taken
    def compose_timelapse(self):
        while True:
            ## If timeout error happens retry ( from queue)
            try:
                self.signalqueue.get(timeout=300)
                ## Get images in a list
                image_files = [os.path.join(self.directory,img)for img in os.listdir(self.directory)if img.endswith(".jpg")]
                ## Sort images from time
                image_files.sort(key=lambda x: os.path.getmtime(x))
                ## Compose timelapse
                clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(image_files, fps=self.fps)
                ## Save video to a demo file
                clip.write_videofile(self.directory + "alt.mp4")
                ## Since writing the video can take a while it will be saved as alt.mp4 and then renamed to the actual video name so it dosnt load on the we site
                os.remove(self.directory + self.video_name)
                os.rename(self.directory + "alt.mp4", self.directory + self.video_name)
            except:
                pass
                
            
    ## Capture a image every interval seconds and save with timestamp
    def image_capturer(self):
        camera = PiCamera()
        time.sleep(2.0)
        for filename in camera.capture_continuous(self.directory + 'img{timestamp:%Y-%m-%d-%H-%M-%S}.jpg'):
            print(f"Captured {filename} for timelapse")
            self.signalqueue.put("OK")
            time.sleep(self.interval)



## Video Camera for LIVE CAMERA THIS IS NOT NEEDED
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

