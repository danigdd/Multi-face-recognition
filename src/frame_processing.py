import os
import cv2
import face_recognition
from typing import List
class FrameProcessing:
    def __init__(self, source_of_processing: str, path: str):
        self._source_of_processing = source_of_processing.lower()
        self._path = path
        self.imagesFaces = []
        self.namesFaces = []
        self._encodesList = []
    def optionChoosen(self):
        if self._source_of_processing == "data":
            self.dataProcessing(self._path)
        elif self._source_of_processing == "live-video":
            pass
        else:
            print(f'{self._source_of_processing} not found or invalid source. Valid sources : "data", "live-video"')
    
    def dataProcessing(self, path: str):
        stored_raw_data = os.listdir(self._path)
        for element in stored_raw_data:
            if element != '.DS_Store':
                self.namesFaces.append(os.path.splitext(element)[0])
                imgFile = cv2.imread(f'{path}/{element}')
                self.imagesFaces.append(imgFile)
                encodesList = []

        for img in self.imagesFaces:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encodes = face_recognition.face_encodings(img)[0]
            self._encodesList.append(encodes)

    def live_videoProcessing(self):
        pass

    def find_encodings(self, images_list_to_encode: List):
        pass
