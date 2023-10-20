import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from Tracker_helper import Tracker

track = Tracker()

def tracker(cars_centroids, direction = [], last_iter=False):

    if not last_iter:
        for centroid in cars_centroids:
            if centroid == []:
                continue
            near_id = track.check_nearby(centroid)
            if near_id is None:
                track.new_id(centroid)
                continue
            track.update(near_id, centroid)
            track.increment_last_updates()

        direction.extend(track.get_direction(last_iter=last_iter))

    else:
        direction.extend(track.get_direction(last_iter=last_iter))

    return direction

def tracker_2(centroid,last_iter=False):
    if not last_iter:
        if centroid != []:
            near_id = track.check_nearby(centroid)
        if near_id is not None:
            track.update(near_id, centroid)
            track.increment_last_updates()
            direction = track.get_car_direction(near_id)
        else:
            id_new =track.new_id(centroid)
            direction = track.get_car_direction(id_new)
        return direction


#TODO: Comprovar que el moviment no sigui horitzontal


