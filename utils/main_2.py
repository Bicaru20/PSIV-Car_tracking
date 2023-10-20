import cv2
from ultralytics import YOLO
import os 

from Yolo import yolo_detection_2
from Tracker import tracker, tracker_2

path_file = os.path.join(os.path.dirname(os.path.dirname(
        __file__)),'video\\output7.mp4')

model = YOLO('yolov8n.pt')

config = {
    "show": True
}
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
    
    centroids,x,y,w,h = yolo_detection_2(model, frame)
    # We get the centroids of every car detected in the actual frame
    if centroids is None:
        continue
    for i in range(len(centroids)):
        direction = tracker_2(centroids[i])
        cv2.rectangle(frame, (x[i],y[i]), (x[i]+w[i], y[i]+h[i]), (0, 255, 0), 2)
        cv2.circle(frame, centroids[i], 4, (0, 0, 255), -1)
        cv2.putText(frame, f"Direction: {direction}", (x[i], y[i] + h[i] + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        # Display the annotated frame
    if config["show"]:
        cv2.imshow("YOLOv8 Inference", frame)
        cv2.waitKey(1)



##We need to do this because the last iteration of the loop does not get appended to the direction list
#direction = tracker(centroids, direction, last_iter=True)
#for x in direction:
#    if 'Up' in x:
#        Up += 1
#    elif 'Down' in x:
#        Down += 1
#print('Up: ', Up)
#print('Down: ', Down)