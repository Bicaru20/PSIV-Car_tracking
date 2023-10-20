import cv2
from ultralytics import YOLO
import os

from Yolo import Yolo
from Tracker import Tracker

if __name__ == '__main__':

    # Path to the video file
    path_file = os.path.join(os.path.dirname(os.path.dirname(
        __file__)), 'videos/short.mp4')

    # Initialize the YOLOv8 model
    yolo = Yolo('yolov8n.pt')

    # Initialize the Tracker
    tracker = Tracker()

    # Open the video file
    video_path = path_file
    cap = cv2.VideoCapture(video_path)
    count = 0

    while cap.isOpened():

        # Temporal limit
        count += 1
        if count == 200:
            break

        # Read the frame
        success, frame = cap.read()

        # Check if we are at the end of the video
        if not success:
            cap.release()
            break

        # Detect cars in the frame
        centroids = yolo.detect(frame)
        if centroids is None:
            continue

        # Track the cars
        tracker.identify_cars(centroids)
        tracker.update_counters()
        tracker.update_output(print_output=True)

        # Display the number of cars going up, down and left
        print("---------------------------------------------")
        print("Frame: ", count)
        print("FPS: ", cap.get(cv2.CAP_PROP_FPS))
        print("---------------------------------------------")
        print("Counter UP:", tracker.get_counter_up())
        print("Counter DOWN:", tracker.get_counter_down())
        print("---------------------------------------------""")
        print("Current Up: ", tracker.get_current_up())
        print("Current Down: ", tracker.get_down())
        print("Current Left: ", tracker.get_left())
        print("Current Right: ", tracker.get_right())
        print("\n")
