import cv2
import os

from utils.Predictor import Predictor
from utils.Tracker import Tracker

if __name__ == '__main__':

    # Path to the video file
    path_file = os.path.join(os.path.dirname(os.path.dirname(
        __file__)), 'videos/short.mp4')

    print(path_file)

    cap = cv2.VideoCapture(path_file)

    # Initialize the YOLOv8 model
    predictor = Predictor(yolo_model_path='yolov8n.pt')

    # Initialize the Tracker
    tracker = Tracker(cap)

    count = 0

    print("Starting the video...")
    print(f"Cap Status: {cap.isOpened()}")

    while cap.isOpened():

        # Temporal limit
        if count >= 200:
            break

        # Read the frame
        success, frame = cap.read()

        # Check if we are at the end of the video
        if not success:
            print("End of the video")
            cap.release()
            break

        # Detect cars in the frame
        centroids = predictor.detect_with_yolo(frame)
        if centroids is None:
            continue

        # Track the cars
        tracker.identify_cars(centroids)
        tracker.update_counters()
        tracker.update_output(frame, print_output=True)

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

        count += 5
        cap.set(cv2.CAP_PROP_POS_FRAMES, count)

    cap.release()
    tracker.output.release()
    cv2.destroyAllWindows()
