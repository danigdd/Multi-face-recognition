import face_recognition
import numpy as np
import cv2
import os
from frame_processing import FrameProcessing

path = 'data/known-faces/'

known_encodes = FrameProcessing("data", path)
known_encodes.optionChoosen()
print("Encoding complete")

live_capture = cv2.VideoCapture(0)

buffer_frame = 4
current_frame_count = 0
previous_name = "unknown"
is_match = False
if not live_capture.isOpened():
    print("Cannot open camera")
    exit()
while True:
    ret, frame = live_capture.read()

    frame = cv2.resize(frame, (0,0), None, 0.25, 0.25)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    if face_encodings:
        for faceLocation, faceEncoding in zip(face_locations, face_encodings):
            match = face_recognition.compare_faces(known_encodes._encodesList, faceEncoding)
            distance = face_recognition.face_distance(known_encodes._encodesList, faceEncoding)
            print(distance)
            name = "unknown"
        
            if (len(distance) > 0):
                lowest_match = np.argmin(distance)
                if match[lowest_match] == True and distance[lowest_match] < 0.6:
                    name = known_encodes.namesFaces[lowest_match].upper()
                    previous_name = name
                    print(name)
                    current_frame_count = 0
                    is_match = True
                else:
                    name = "unknown"
                    is_match = False
                    current_frame_count = buffer_frame

            if current_frame_count < buffer_frame and is_match:
                name = previous_name
            else:
                name = "unknown"

            current_frame_count += 1



            y1, x2, y2, x1 = faceLocation
            if name =="unknown":
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255,0,0), 2)
                cv2.putText(frame, 'unknown', (faceLocation[3], faceLocation[2] + 30), cv2.FONT_HERSHEY_COMPLEX, 1, (255,0,0), 1)
                continue
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255,0,0), 2)
            cv2.putText(frame, f'{name}', (faceLocation[3], faceLocation[2] + 30), cv2.FONT_HERSHEY_COMPLEX, 1, (255,0,0), 1)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    cv2.imshow("Webcam", frame)
    cv2.waitKey(1)