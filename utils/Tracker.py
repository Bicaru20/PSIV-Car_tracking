from imutils.video import FPS
import imutils
import cv2
import sys
import os

from utils.detection_with_mean import object_detection
from utils.Tracker_helper import Tracker


cars_centroids = object_detection()
tracker = Tracker()

for centroid in cars_centroids:
    near_id = tracker.check_nearby(centroid)
    if near_id is None:
        tracker.new_id(centroid)
        continue
    tracker.update(near_id, centroid)

