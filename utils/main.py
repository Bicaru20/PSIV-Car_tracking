import cv2
from ultralytics import YOLO
import os 

from Yolo import yolo_detection
from Tracker import tracker

path_file = os.path.join(os.path.dirname(os.path.dirname(
        __file__)),'video\\output7.mp4')

model = YOLO('yolov8n.pt')

# Open the video file
video_path = path_file
cap = cv2.VideoCapture(video_path)
count = 0
direction = []
Up = 0
Down = 0

while cap.isOpened():
    count += 1
    if count == 200:
        break
    success, frame = cap.read()
    if not success:
        continue

    centroids = yolo_detection(model, frame)
    if centroids is None:
        continue
    direction = tracker(centroids, direction)
    for x in direction:
        if 'Up' in x:
            Up += 1
        elif 'Down' in x:
            Down += 1
    print('Up: ', Up)
    print('Down: ', Down)

#We need to do this because the last iteration of the loop does not get appended to the direction list
direction = tracker(centroids, direction, last_iter=True)
for x in direction:
    if 'Up' in x:
        Up += 1
    elif 'Down' in x:
        Down += 1
print('Up: ', Up)
print('Down: ', Down)