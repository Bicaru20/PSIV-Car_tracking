class Trucker:
    def __init__(self):
        self.tracked_objects = {}  # Dictionary to store tracked objects by their IDs

    def update(self, object_id, centroid):
        # Update the position of an object with a given ID
        if object_id in self.tracked_objects:
            self.tracked_objects[object_id]["coordinates"].append(centroid)
        else:
            self.tracked_objects[object_id] = {
                "coordinates": [centroid],
                "last_updated_frame": 0
            }

    def is_moving(self, object_id, new_frame):
        # Check if an object with a given ID is moving
        if object_id in self.tracked_objects:
            last_updated_frame = self.tracked_objects[object_id]["last_updated_frame"]
            if new_frame - last_updated_frame > 1:
                return True
        return False

    def get_tracked_objects(self):
        # Get a list of tracked objects
        return list(self.tracked_objects.keys())

    def update_last_frame(self, object_id, new_frame):
        # Update the last frame when an object was updated
        if object_id in self.tracked_objects:
            self.tracked_objects[object_id]["last_updated_frame"] = new_frame
