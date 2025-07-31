import face_recognition
import numpy as np
import cv2
import os
from frame_processing import FrameProcessing
from video_input import VideoInput

path = 'data/known-faces/'

known_encodes = FrameProcessing("data", path)
print("Encoding complete")
print(known_encodes.namesFaces)
camera = VideoInput()

