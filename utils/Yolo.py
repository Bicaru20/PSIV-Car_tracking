import cv2
from ultralytics import YOLO
import os

config = {
    "show": True
}


class Yolo:
    def __init__(self, model_path):
        self.model = YOLO(model_path)

    def detect(self, frame):

        results = self.model(frame)

        # Extract centroids of car contours
        if len(results) == 0:
            return None
        centroids = []
        for car_result in results:
            for i, data in enumerate(car_result.boxes.data.tolist()):
                print(f"\nCar {i}:")
                print(data)
                print("-----------------------------")
                x1, y1, x2, y2, conf, clas = data
                if clas == 2:
                    x = int(x1)
                    y = int(y1)
                    w = int(x2) - int(x1)
                    h = int(y2) - int(y1)
                    centroid_x = x + w // 2
                    centroid_y = y + h // 2
                    centroids.append((centroid_x, centroid_y))
                    if conf > 0.45:
                        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                        cv2.circle(frame, (centroid_x, centroid_y), 4, (0, 0, 255), -1)

        # Display the annotated frame
        if config["show"]:
            cv2.imshow("YOLOv8 Inference", frame)
            cv2.waitKey(0)

        return centroids


if __name__ == '__main__':
    yolo = Yolo('yolov8n.pt')
    yolo.detect(cv2.imread(os.path.join(os.path.dirname(__file__), "../videos/test.jpg")))
