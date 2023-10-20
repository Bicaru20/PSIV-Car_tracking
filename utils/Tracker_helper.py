from scipy.spatial import distance


class Id:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y
        self.last_update = 0
        self.first_cor = (x, y)
        self.last_cor = (x, y)

    def update_centroid(self, x, y):
        self.last_cor = (self.x, self.y)
        self.x = x
        self.y = y
        self.last_update = 0
        # I changed it so that x and y are the actual coordinates of the centroid and
        # last_cor are the last coordinates of the centroid because it will be much easier to calculate
        # if it goes down or up

    def increment_last_update(self):
        self.last_update += 1

class Tracker:
    def __init__(self):
        self.tracked_objects = {}  # Dictionary to store tracked objects by their IDs

    def new_id(self, centroid):
        # Check if ID 0 is available, if not, find the first available ID
        for object_id in range(len(self.tracked_objects) + 1):
            if object_id not in self.tracked_objects:
                new_id = object_id
                break
        self.tracked_objects[new_id] = Id(new_id, centroid[0], centroid[1])
        return new_id

    def update(self, object_id, centroid):
        # Update the position of an object with a given ID
        self.tracked_objects[object_id].update_centroid(centroid[0], centroid[1])

    def check_nearby(self, centroid):
        # Check if a given centroid is close to an existing object
        if len(self.tracked_objects) != 0:
            distances = {}
            for object_id in self.tracked_objects:
                d = distance.euclidean((self.tracked_objects[object_id].x, self.tracked_objects[object_id].y), centroid)
                distances[object_id] = d

            # Keep the object ID with the smallest distance and check if it is below a certain threshold
            min_distance_object_id = min(distances, key=distances.get)
            if distances[min_distance_object_id] < 100:
                return min_distance_object_id
        return None

    def increment_last_updates(self):
        # Increment the last_update counters for objects that were not updated in the current iteration
        for object_id in self.tracked_objects:
            self.tracked_objects[object_id].increment_last_update()

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
    
    def get_car_direction(self,object_id, last_iter=False):
        if self.tracked_objects[object_id].y > self.tracked_objects[object_id].last_cor[1]:
            direction='DOWN'
        elif  self.tracked_objects[object_id].y < self.tracked_objects[object_id].last_cor[1]:
            direction='UP'
        else:
            direction='NO MOVEMENT'
        return direction








        