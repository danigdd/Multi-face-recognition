import cv2 
from singleton import Singleton
import face_recognition
from frame_processing import FrameProcessing

class VideoInput(Singleton):

    def __init__(self):
        self._live_capture = cv2.VideoCapture(0)
        self._checkCamera()
        self._while_loop()
    
    def _checkCamera(self):
        if not self._live_capture.isOpened():
            print("Cannot open camera")
            exit()
    def _while_loop(self):
        while True:
            ret, current_frame = self._live_capture.read()

            processed_encodings = FrameProcessing("live-video", frame=current_frame)
            cv2.imshow("Webcam", current_frame)
            cv2.waitKey(1)

            