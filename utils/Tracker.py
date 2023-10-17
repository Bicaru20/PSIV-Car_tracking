from imutils.video import FPS
import imutils
import cv2
import sys
import os

from utils.detection_with_mean import object_detection


cars_centroids = object_detection()