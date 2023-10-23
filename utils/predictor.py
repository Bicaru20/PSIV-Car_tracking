import cv2
import os
import numpy as np

from ultralytics import YOLO

config = {
    "show": False
}


class Predictor:
    def __init__(self, yolo_model_path):
        self.yolo_model = YOLO(yolo_model_path)
        self.background_subtractor = cv2.createBackgroundSubtractorMOG2()
        self.counter = 0  # Contador para alternar entre métodos
        self.max_counter = 5  # Número de frames para usar background subtraction antes de cambiar a YOLO

    def predict(self, frame):
        if self.counter < self.max_counter:
            centroids = self.detect_with_background_subtraction(frame)
            self.counter += 1
        else:
            centroids = self.detect_with_yolo(frame)
            self.counter = 0

        return centroids

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

    def detect_with_background_subtraction(self, frame):
        output = frame.copy()

        # Apply background subtraction
        fg_mask = self.background_subtractor.apply(frame)

        # Clean up the mask (optional)
        kernel = np.ones((5, 5), np.uint8)
        fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, kernel)

        dilation_kernel = np.ones((8, 8), np.uint8)  # Adjust the kernel size as needed
        fg_mask = cv2.dilate(fg_mask, dilation_kernel)

        # Find contours in the foreground mask
        contours, _ = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        centroids = []

        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)

            # Calculate centroid
            centroid_x = x + w // 2
            centroid_y = y + h // 2

            # Ensure the detected object is of a minimum size
            if w > 45 and h > 45:
                centroids.append((centroid_x, centroid_y))
                cv2.rectangle(output, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.circle(output, (centroid_x, centroid_y), 4, (0, 0, 255), -1)

        # Display the annotated frame
        if config["show"]:
            cv2.imshow("Background Subtraction", output)
            cv2.waitKey(1)

        return centroids


if __name__ == '__main__':
    yolo = Predictor('yolov8n.pt')
    yolo.detect_yolo(cv2.imread(os.path.join(
        os.path.dirname(__file__), "../videos/test.jpg")))
