from scipy.spatial import distance


class Id:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y
        self.last_update = 0
        self.first_cor = (x,y)
        self.last_five = None

    def update_centroid(self, x, y):
        self.x = x
        self.y = y
        if len(self.last_five) == 5:
            self.last_five.pop()
        self.last_five.add((x, y))       



class Trucker:
    def __init__(self):
        self.tracked_objects = {}  # Dictionary to store tracked objects by their IDs

    def new_id(self, centroid):
        # Create a new object ID for a given centroid
        new_id = len(self.tracked_objects)
        self.tracked_objects[new_id] = Id(new_id, centroid[0], centroid[1])
        return new_id
    
    def update(self, object_id, centroid):
        # Update the position of an object with a given ID
        self.tracked_objects[object_id].update_centroid(centroid[0], centroid[1])
        self.tracked_objects[object_id].new_update()

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

    def get_tracked_objects(self):
        # Get a list of tracked objects
        return list(self.tracked_objects.values())




        