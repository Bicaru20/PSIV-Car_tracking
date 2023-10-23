import cv2
from ultralytics import YOLO
import os

config = {
    "show": False
}


class Predictor:
    def __init__(self, yolo_model_path):
        self.yolo_model = YOLO(yolo_model_path)

    def detect_with_yolo(self, frame):

        output = frame.copy()

        results = self.yolo_model(frame)

        # Extract centroids of car contours
        if len(results) == 0:
            return None
        centroids = []
        for car_result in results:
            for i, data in enumerate(car_result.boxes.data.tolist()):
                print("\n-----------------------------")
                print(f"Car {i}:")
                print(data)
                x1, y1, x2, y2, conf, clas = data
                if clas == 2:
                    x = int(x1)
                    y = int(y1)
                    w = int(x2) - int(x1)
                    h = int(y2) - int(y1)
                    centroid_x = x + w // 2
                    centroid_y = y + h // 2
                    if conf > 0.45:
                        centroids.append((centroid_x, centroid_y))
                        cv2.rectangle(output, (x, y), (x+w, y+h),
                                      (0, 255, 0), 2)
                        cv2.circle(output, (centroid_x, centroid_y),
                                   4, (0, 0, 255), -1)

        # Display the annotated frame
        if config["show"]:
            cv2.imshow("YOLOv8 Inference", output)
            cv2.waitKey(0)

        return centroids

    def detect_our(self, frame):
        # Our predictor LINEAR REGRESSION??
        return None


if __name__ == '__main__':
    yolo = Predictor('yolov8n.pt')
    yolo.detect_yolo(cv2.imread(os.path.join(
        os.path.dirname(__file__), "../videos/test.jpg")))
