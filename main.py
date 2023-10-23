import cv2
import time

from utils.Predictor import Predictor
from utils.Tracker import Tracker

if __name__ == '__main__':

    # Path to the video file
    path_file = "videos/short.mp4"

    cap = cv2.VideoCapture(path_file)

    # Initialize the YOLOv8 model
    predictor = Predictor(yolo_model_path='yolov8n.pt')

    # Initialize the Tracker
    tracker = Tracker(cap)

    count = 0

    print("\n" + "-" * 50)
    print("Starting the video...")
    print(f"Cap Status: {cap.isOpened()}")

    while cap.isOpened():

        start_time = time.time()

        # Temporal limit
        if count >= 400:
            pass

        # Read the frame
        success, frame = cap.read()

        # Check if we are at the end of the video
        if not success:
            print("End of the video")
            cap.release()
            break

        # Detect cars in the frame
        centroids = predictor.predict(frame)

        if centroids is None:
            continue

        # Track the cars
        tracker.identify_cars(centroids)
        tracker.update_counters()
        tracker.update_output(frame=frame, n_frame=count,
                              fps=1 / (time.time() - start_time), print_output=False)

        # Display the number of cars going up, down and left
        print("\n---------------------------------------------")
        print("Frame: ", count)
        print("FPS: ", 1 / (time.time() - start_time))
        print("---------------------------------------------")
        print("Counter UP:", tracker.get_counter_up())
        print("Counter DOWN:", tracker.get_counter_down())
        print("---------------------------------------------""")
        print("Current Up: ", tracker.get_current_up())
        print("Current Down: ", tracker.get_current_down())
        print("Current Left: ", tracker.get_current_left())
        print("Current Right: ", tracker.get_current_right())
        print("\n")

        count += 5
        cap.set(cv2.CAP_PROP_POS_FRAMES, count)

    cap.release()
    tracker.output.release()
    cv2.destroyAllWindows()
