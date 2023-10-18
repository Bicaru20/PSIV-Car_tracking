import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.detection_with_mean import object_detection
from utils.Yolo import yolo_detection
from utils.Tracker_helper import Tracker


#cars_centroids = object_detection()
cars_centroids = yolo_detection()
tracker = Tracker()
direction = []

for centroid in cars_centroids:
    for center in centroid:
        if center == []:
            continue
        near_id = tracker.check_nearby(center)
        if near_id is None:
            tracker.new_id(center)
            continue
        tracker.update(near_id, center)
        tracker.increment_last_updates()

    direction.extend(tracker.get_direction())

direction.extend(tracker.get_direction(last_iter=True))

print(direction)

#TODO: Comprovar que el moviment no sigui horitzontal


