import cv2 
from singleton import Singleton
import face_recognition
from frame_processing import FrameProcessing

class VideoInput(Singleton):
    BUFFER_FRAME = 6
    CURRENT_FRAME_COUNT = 0
    PREVIOUS_NAME = ""
    IS_MATCH = False

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

            y1, x2, y2, x1 = faceLocation
            if name =="unknown":
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255,0,0), 2)
                cv2.putText(frame, 'unknown', (faceLocation[3], faceLocation[2] + 30), cv2.FONT_HERSHEY_COMPLEX, 1, (255,0,0), 1)
                continue
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255,0,0), 2)
            cv2.putText(frame, f'{name}', (faceLocation[3], faceLocation[2] + 30), cv2.FONT_HERSHEY_COMPLEX, 1, (255,0,0), 1)