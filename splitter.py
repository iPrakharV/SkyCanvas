from CONSTANTS import *
import cv2


class Splitter:
    def __init__(self):
        self.feature_params = dict(maxCorners = DRONE_COUNT, qualityLevel = 0.2, minDistance = 2, blockSize = 7)
    


    def split_points(self,frame):
        return cv2.goodFeaturesToTrack(frame, mask = None, **self.feature_params)
