import cv2
from ultralytics import YOLO
import os 


path_file = os.path.join(os.path.dirname(os.path.dirname(
        __file__)),'video\\output7.mp4')

config = {
    "show": False
}


def yolo_detection():
    # Load the YOLOv8 model
    model = YOLO('yolov8n.pt')

    # Open the video file
    video_path = path_file
    cap = cv2.VideoCapture(video_path)

    # Loop through the video frames
    count = 0
    frames = []
    while cap.isOpened():
        # Read a frame from the video
        success, frame = cap.read()

        if success:
            # Run YOLOv8 inference on the frame
            count += 1
            if count == 200:
                break
            # if count % 5 != 0:
            #     continue
            
            results = model(frame)

            # Visualize the results on the frame
            car_results = [result for result in results[0] if result.names[2] == 'car']  # Assuming class ID for "car" is 2

            # Extract centroids of car contours
            if len(car_results) == 0:
                continue
            centroids = []
            for car_result in car_results:
                for data in car_result.boxes.data.tolist():
                    x1, y1, x2, y2, _, _ = data
                    x = int(x1)
                    y = int(y1)
                    w = int(x2) - int(x1)
                    h = int(y2) - int(y1)
                    centroid_x = x + w // 2
                    centroid_y = y + h // 2
                    centroids.append((centroid_x, centroid_y))
                    cv2.rectangle(frame, (x,y), (x+w, y+h), (0, 255, 0), 2)
                    cv2.circle(frame, (centroid_x, centroid_y), 4, (0, 0, 255), -1)
            # Display the annotated frame
            if config["show"]:
                cv2.imshow("YOLOv8 Inference", frame)
                cv2.waitKey(1)
            frames.append(centroids)
    
    return frames
        
    

if __name__ == '__main__':
    yolo_detection()

        