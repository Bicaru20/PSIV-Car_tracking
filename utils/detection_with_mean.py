from imutils.video import FPS
import imutils
import cv2
import sys
import os


path_file = os.path.join(os.path.dirname(os.path.dirname(
    __file__)), 'video\\short.mp4')

config = {
    "show": False
}

# TODO: Reduir el soroll de la imatge i aplicar Yolo


def object_detection():
    stream = cv2.VideoCapture(path_file)
    fps = FPS().start()
    count = 1
    # initializing subtractor
    mean = None
    cars_centroids = []
    while True:
        (grabbed, frame) = stream.read()

        if not grabbed or count == 1000:
            break

        frame = imutils.resize(frame, width=450)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Eliminate the upper 1/3 of the frame
        frame = frame[int(frame.shape[0]/3):, :]

        if mean is None:
            mean = frame.astype("float")
            continue

        alpha = 0.01
        cv2.accumulateWeighted(frame, mean, alpha)

        fgmask = cv2.absdiff(frame, mean.astype("uint8"))

        # Threshold to binarize
        fgmask = cv2.threshold(fgmask, 28, 255, cv2.THRESH_BINARY)[1]

        cnts, _ = cv2.findContours(fgmask.copy(), cv2.RETR_EXTERNAL,
                                   cv2.CHAIN_APPROX_SIMPLE)
        cnts = [c for c in cnts if cv2.contourArea(c) > 500]

        centroids = []
        for c in cnts:
            (x, y, w, h) = cv2.boundingRect(c)
            centroid_x = x + w // 2
            centroid_y = y + h // 2
            centroids.append((centroid_x, centroid_y))
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.circle(frame, (centroid_x, centroid_y), 4, (0, 0, 255), -1)

        if config["show"]:
            cv2.imshow("Frame", frame)
            cv2.waitKey(0)

        if centroids != []:
            cars_centroids.append(centroids)

        fps.update()
        count += 1

    cv2.destroyAllWindows()

    return cars_centroids


if __name__ == "__main__":
    object_detection()
