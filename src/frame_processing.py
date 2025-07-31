import os
import cv2
import face_recognition
import numpy as np
from video_output import VideoOutput
from singleton import Singleton
from attendance_loader import Attendance_Loader

class FrameProcessing(Singleton):
    BUFFER_FRAME = 6
    CURRENT_FRAME_COUNT = 0
    PREVIOUS_NAME = ""
    IS_MATCH = False

    _encodesList: list = []
    namesFaces: list = []
    _initialized = False

    def __init__(self, source_of_processing: str, path: str = None, frame=None):
        source = source_of_processing.lower()

        if not FrameProcessing._initialized and source == "data":
            self._load_known_faces(path)
            FrameProcessing._initialized = True

        if source == "live-video" and frame is not None:
            self._process_live_frame(frame)

    def _load_known_faces(self, path: str):
        for file in os.listdir(path):
            if file.lower().endswith(('.jpg', '.png', '.jpeg')):
                name = os.path.splitext(file)[0]
                FrameProcessing.namesFaces.append(name)
                img = cv2.cvtColor(cv2.imread(os.path.join(path, file)), cv2.COLOR_BGR2RGB)
                enc = face_recognition.face_encodings(img)[0]
                FrameProcessing._encodesList.append(enc)

    def _process_live_frame(self, frame):
        small = cv2.resize(frame, (0,0), fx=0.25, fy=0.25)
        rgb_small = cv2.cvtColor(small, cv2.COLOR_BGR2RGB)
        self._find_and_display(rgb_small, frame)

    def _find_and_display(self, small_frame, original_frame):
        locs = face_recognition.face_locations(small_frame)
        encs = face_recognition.face_encodings(small_frame, locs)

        for (top, right, bottom, left), face_encoding in zip(locs, encs):
            matches = face_recognition.compare_faces(FrameProcessing._encodesList, face_encoding)
            dists = face_recognition.face_distance(FrameProcessing._encodesList, face_encoding)

            name = "unknown"
            if dists.size > 0:
                best_idx = np.argmin(dists)
                if matches[best_idx] and dists[best_idx] < 0.6:
                    name = FrameProcessing.namesFaces[best_idx].upper()

                    FrameProcessing.PREVIOUS_NAME = name
                    FrameProcessing.CURRENT_FRAME_COUNT = 0
                    FrameProcessing.IS_MATCH = True
                    mark_attendance = Attendance_Loader(name)
                else:
                    FrameProcessing.IS_MATCH = False
                    FrameProcessing.CURRENT_FRAME_COUNT = FrameProcessing.BUFFER_FRAME


            if FrameProcessing.CURRENT_FRAME_COUNT < FrameProcessing.BUFFER_FRAME and FrameProcessing.IS_MATCH:
                name = FrameProcessing.PREVIOUS_NAME
            else:
                name = "unknown"

            FrameProcessing.CURRENT_FRAME_COUNT += 1


            top, right, bottom, left = top*4, right*4, bottom*4, left*4
            VideoOutput(name, original_frame, left, top, right, bottom)
