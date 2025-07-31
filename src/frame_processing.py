import os
import cv2
import face_recognition
import numpy as np
from typing import List
class FrameProcessing:
    BUFFER_FRAME = 6
    CURRENT_FRAME_COUNT = 0
    PREVIOUS_NAME = ""
    IS_MATCH = False
    def __init__(self, source_of_processing: str, path: str = None, frame=None):
        self._source_of_processing = source_of_processing.lower()
        self._path = path
        self.imagesFaces = []
        self.namesFaces = []
        self._encodesList = []
        self._frame = frame
        self.optionChoosen()

    def optionChoosen(self):
        if self._source_of_processing == "data":
            self.dataProcessing(self._path)
        elif self._source_of_processing == "live-video":
            self.live_videoProcessing(self._frame)
        else:
            print(f'{self._source_of_processing} not found or invalid source. Valid sources : "data", "live-video"')
    
    def dataProcessing(self, path: str):
        stored_raw_data = os.listdir(self._path)
        for element in stored_raw_data:
            if element != '.DS_Store':
                self.namesFaces.append(os.path.splitext(element)[0])
                imgFile = cv2.imread(f'{path}/{element}')
                self.imagesFaces.append(imgFile)


        for img in self.imagesFaces:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encodes = face_recognition.face_encodings(img)[0]
            self._encodesList.append(encodes)

    def live_videoProcessing(self, frame):
        frame = cv2.resize(frame, (0,0), None, 0.25, 0.25)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.find_encodings(frame)

    def find_encodings(self, frame):
        self._face_locations = face_recognition.face_locations(frame)
        self._face_encodings = face_recognition.face_encodings(frame, self.face_locations)
        if self._face_encodings:
            for faceLocation, faceEncoding in zip(self._face_locations, self._face_encodings):
                match = face_recognition.compare_faces(self._encodesList, faceEncoding)
                distance = face_recognition.face_distance(self._encodesList, faceEncoding)
                print(distance)
                name = "unknown"
            
                if (len(distance) > 0):
                    lowest_match = np.argmin(distance)
                    if match[lowest_match] == True and distance[lowest_match] < 0.6:
                        name = self.namesFaces[lowest_match].upper()
                        self.PREVIOUS_NAME = name
                        print(name)
                        self.CURRENT_FRAME_COUNT = 0
                        self.IS_MATCH = True
                    else:
                        name = "unknown"
                        self.IS_MATCH = False
                        self.CURRENT_FRAME_COUNT = self.BUFFER_FRAME

                if self.CURRENT_FRAME_COUNT < self.BUFFER_FRAME and self.IS_MATCH:
                    name = self.PREVIOUS_NAME
                else:
                    name = "unknown"

                self.CURRENT_FRAME_COUNT += 1
                