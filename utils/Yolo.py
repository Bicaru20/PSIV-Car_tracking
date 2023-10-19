import cv2
from ultralytics import YOLO
import os 

path_file = os.path.join(os.path.dirname(os.path.dirname(
        __file__)),'video\\output7.mp4')

config = {
    "show": False
}


def yolo_detection(model, frame):
    
    results = model(frame)

    # Visualize the results on the frame

    # Extract centroids of car contours
    if len(results) == 0:
        return None
    centroids = []
    for car_result in results:
        for data in car_result.boxes.data.tolist():
            x1, y1, x2, y2, _, clas = data
            if clas == 2:
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
    
    return centroids
        
    

if __name__ == '__main__':
    yolo_detection()

        