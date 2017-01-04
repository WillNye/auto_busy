import json
import time
import warnings
import datetime
from collections import deque

import psutil
import numpy as np
import imutils
from imutils.object_detection import non_max_suppression
import cv2
from pywinauto.application import Application

from advanced_detection.tempimage import TempImage


class AdvancedCamShift:
    def __init__(self):
        self.hog = cv2.HOGDescriptor()
        self.hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
        warnings.filterwarnings("ignore")
        self.conf = json.load(open("conf.json"))
        self.timestamp = datetime.datetime.now()
        self.ts = self.timestamp.strftime("%A %d %B %Y %I:%M:%S%p")
        (self.dX, self.dY) = (0, 0)
        self.counter = 0
        self.for_show = None
        self.track_windows = None
        self.app_name = 'pycharm.exe'
        self.window_name = 'camstat - [C:\\Users\\wbeasley\\PycharmProjects\\camstat] - ...\\non_vsm_scripts\\update_tables.py - PyCharm 2016.2.3'
        self.camera_url = 'rtsp://admin:admin@10.10.50.33:8554/CH001.sdp'

        # initialize the camera and grab a reference to the raw camera capture
        try:
            self.camera = cv2.VideoCapture(self.camera_url)
        except Exception as e:
            print(e)

    def _define_windows(self, frame):
        # detect people in the image
        (rects, weights) = self.hog.detectMultiScale(frame, winStride=(4, 4),
                                                     padding=(8, 8), scale=1.05)

        # apply non-maxima suppression to the bounding boxes using a
        # fairly large overlap threshold to try to maintain overlapping
        # boxes that are still people
        self.track_windows = rects
        rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
        pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)
        current_objects = len(pick)

        if self.conf["show_video"]:
            # draw the final bounding boxes
            for (xA, yA, xB, yB) in pick:
                cv2.rectangle(self.for_show, (xA * 2, yA * 2), (xB * 2, yB * 2), (0, 255, 0), 2)

            if current_objects > 0:
                # draw the text and timestamp on the frame
                self.ts = self.timestamp.strftime("%A %d %B %Y %I:%M:%S%p")
                cv2.putText(self.for_show, "Occupied by {} people".format(str(current_objects)), (10, 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                cv2.putText(self.for_show, self.ts, (10, self.for_show.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
                            0.35, (0, 0, 255), 1)
            else:
                cv2.putText(self.for_show, "Unoccupied", (10, 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        return current_objects

    def start_detection(self):
        # capture frames from the camera
        while True:
            # grab the raw NumPy array representing the image and initialize
            # the timestamp and occupied/unoccupied text
            (grabbed, frame) = self.camera.read()
            self.timestamp = datetime.datetime.now()

            # resize the frame, convert it to grayscale, and blur it
            if self.conf["show_video"]:
                self.for_show = imutils.resize(frame, width=800)
            frame = imutils.resize(frame, width=400)

            current_objects = self._define_windows(frame)

            if current_objects > 0:
                self.counter += 1
                if self.counter > 5:
                    for proc in psutil.process_iter():
                        if proc.name() == self.app_name:
                            app = Application(backend="uia").connect(process=proc.pid)
                            dlg_spec = app.window(best_match=self.window_name)
                            dlg_spec.wrapper_object().maximize()
            else:
                self.counter = 0

            # check to see if the frames should be displayed to screen
            if self.conf["show_video"]:
                # display the security feed
                cv2.imshow("Security Feed", self.for_show)
                key = cv2.waitKey(100) & 0xFF


if __name__ == '__main__':
    object_tracing = AdvancedCamShift()
    object_tracing.start_detection()
