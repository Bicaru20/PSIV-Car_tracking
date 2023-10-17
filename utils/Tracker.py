import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.detection_with_mean import object_detection
from utils.Tracker_helper import Tracker


cars_centroids = object_detection()
tracker = Tracker()
direction = []

for centroid in cars_centroids:
    for center in centroid:
        if center == []:
            continue
        near_id = tracker.check_nearby(center[0])
        if near_id is None:
            tracker.new_id(center[0])
            continue
        tracker.update(near_id, center[0])
        tracker.increment_last_updates()

    direction.extend(tracker.get_direction())

direction.extend(tracker.get_direction(last_iter=True))

print(direction)

#TODO: Comprovar que el moviment no sigui horitzontal


