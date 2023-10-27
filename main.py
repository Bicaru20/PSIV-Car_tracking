import cv2
import time

from utils.Predictor import Predictor
from utils.Tracker import Tracker

config = {
    "frame_jump": 2,
    "show": True,
    "frame_start": 0,
    "frame_end": None,
}

correct_results = {
    "short.mp4": {
        "up": 6,
        "down": 2,
    },
    "middle.mp4": {
        "up": 5,
        "down": 7,
    },
    "shadow.mp4": {
        "up": 3,
        "down": 10,
    },
    "long_1.mp4": {
        "up": 8,
        "down": 24,
    },
    "long_2.mp4": {
        "up": 6,
        "down": 133,
    },
}

if __name__ == '__main__':

    # Path to the video file
    path_file = "short.mp4"

    cap = cv2.VideoCapture("videos/" + path_file)

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
        if count == 0:
            cap.set(cv2.CAP_PROP_POS_FRAMES, config["frame_start"])
        if config["frame_end"]:
            if count >= config["frame_end"]:
                cap.release()

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
                              fps=(1 / (time.time() - start_time) * config["frame_jump"]),
                              print_output=config["show"])

        # Display the number of cars going up, down and left
        print("\n---------------------------------------------")
        print(f"Frame: {count}/{cap.get(cv2.CAP_PROP_FRAME_COUNT)}")
        print("FPS: ", (1 / (time.time() - start_time)) * config["frame_jump"])
        print("---------------------------------------------")
        print("Counter UP:", tracker.get_counter_up())
        print("Counter DOWN:", tracker.get_counter_down())
        print("Counter LEFT:", tracker.get_counter_left())
        print("Counter RIGHT:", tracker.get_counter_right())
        print("---------------------------------------------")
        print("Current Up: ", tracker.get_current_up())
        print("Current Down: ", tracker.get_current_down())
        print("Current Left: ", tracker.get_current_left())
        print("Current Right: ", tracker.get_current_right())
        print("\n")

        count += config["frame_jump"]
        cap.set(cv2.CAP_PROP_POS_FRAMES, count)

    # Show the results
    tracker.check_results(correct_results[path_file].get("up"), correct_results[path_file].get("down"))

    cap.release()
    tracker.output.release()
    cv2.destroyAllWindows()
