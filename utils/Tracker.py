import os
import sys
import cv2
import numpy as np
from scipy.spatial import distance

from Id import Id


class Tracker:
    def __init__(self):
        self.tracked_objects = {}  # Dictionary to store tracked objects by their IDs

    def new_id(self, centroid):
        new_car = Id(centroid[0], centroid[1])
        self.tracked_objects[new_car.id] = new_car

    def update(self, object_id, centroid):
        # Update the position of an object with a given ID
        self.tracked_objects[object_id].update_centroid(
            centroid[0], centroid[1])

    def check_nearby(self, centroid):
        # Check if a given centroid is close to an existing object
        if len(self.tracked_objects) != 0:
            distances = {}
            for object_id in self.tracked_objects:
                d = distance.euclidean(
                    (self.tracked_objects[object_id].x, self.tracked_objects[object_id].y), centroid)
                distances[object_id] = d

            # Keep the object ID with the smallest distance and check if it is below a certain threshold
            min_distance_object_id = min(distances, key=distances.get)
            if distances[min_distance_object_id] < 100:
                return min_distance_object_id
        return None

    def increment_updates(self):
        # Increment the last_update counters for objects that were not updated in the current iteration
        for object_id in self.tracked_objects:
            self.tracked_objects[object_id].increment_not_updated()

    def get_tracked_objects(self):
        # Get a list of tracked objects
        return list(self.tracked_objects.values())

    def get_direction(self, last_iter=False):
        # Get the direction of the tracked object
        direction = []
        objects_to_delete = []
        for object_id in self.tracked_objects:
            if self.tracked_objects[object_id].last_update > 50 or last_iter:
                if self.tracked_objects[object_id].last_cor[0] > self.tracked_objects[object_id].first_cor[0]:
                    direction.append('Up')
                elif self.tracked_objects[object_id].last_cor[0] == self.tracked_objects[object_id].first_cor[0]:
                    direction.append('No movement')
                else:
                    direction.append('Down')

                objects_to_delete.append(object_id)

        # Delete tracked objects outside of the loop
        for object_id in objects_to_delete:
            del self.tracked_objects[object_id]

        return direction
    
    def identify_cars(self,centroids):
        for centroid in centroids:
            find_id = self.check_nearby(centroid)
            if find_id == None:
                # Create new car
                self.new_id(centroid[0],centroid[1])
            else:
                self.update(find_id,centroid)
        
        self.increment_updates()

        for cars in self.tracked_objects:
            if cars.last_update > 8:
                 del self.tracked_objects[cars]

        





