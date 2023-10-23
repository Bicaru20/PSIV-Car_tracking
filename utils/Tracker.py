import os
import cv2
from scipy.spatial import distance

from utils.Id import Id

START_LINE_A = (190, 400)
END_LINE_A = (285, 400)
START_LINE_B = (290, 400)
END_LINE_B = (390, 400)
START_LINE_UNIQUE = (190, 400)
END_LINE_UNIQUE = (390, 400)
START_LINE_LEFT = (200, 210)
END_LINE_LEFT = (200, 350)
START_LINE_RIGHT = (450, 210)
END_LINE_RIGHT = (450, 350)

config = {
    "n_lines": 2,
    "check_vertical": True,
}


class Tracker:
    def __init__(self, cap):
        self.cap = cap  # Video capture
        self.count_up = 0
        self.count_down = 0
        self.count_right = 0
        self.count_left = 0
        self.n_frame = 0  # Number of frame
        self.tracked_objects = {}  # Dictionary to store tracked objects by their IDs
        # Create the output folder if it does not exist
        if not os.path.exists("output"):
            os.makedirs("output")
        # Check last video number
        last_video = 0
        for file in os.listdir("output"):
            if file.endswith(".mp4"):
                last_video = max(last_video, int(
                    file.split(".")[0].split("_")[1]))
        # Create the output video
        self.output = cv2.VideoWriter(f"output/output_{last_video + 1}.mp4", cv2.VideoWriter_fourcc(
            *'MP4V'), 30, (int(cap.get(3)), int(cap.get(4))), True)

    def new_id(self, centroid):
        new_car = Id(centroid[0], centroid[1])
        self.tracked_objects[new_car.id] = new_car

    def update(self, object_id, centroid):
        # Update the position of an object with a given ID
        # if (
        #     self.tracked_objects[object_id].x >= centroid[0] + 5 and self.tracked_objects[object_id].x <= centroid[0] - 5 and
        #     self.tracked_objects[object_id].y >= centroid[1] +
        #         5 and self.tracked_objects[object_id].y <= centroid[1] - 5
        # ):
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
            if distances[min_distance_object_id] < 40:
                self.tracked_objects[min_distance_object_id].update_centroid(
                    centroid[0], centroid[1], nearby_movement=True)
                return min_distance_object_id
        return None

    def get_tracked_objects(self):
        # Get a list of tracked objects
        return list(self.tracked_objects.values())

    def update_output(self, frame, n_frame, fps, print_output=False):
        self.n_frame = n_frame
        # Update the output video with the current frame
        overlay = frame.copy()
        if config["n_lines"] == 1:
            cv2.line(frame, START_LINE_UNIQUE, END_LINE_UNIQUE, (0, 255, 0), 12)
        elif config["n_lines"] == 2:
            cv2.line(frame, START_LINE_A, END_LINE_A, (0, 255, 0), 12)
            cv2.line(frame, START_LINE_B, END_LINE_B, (255, 0, 0), 12)
        if config["check_vertical"]:
            cv2.line(frame, START_LINE_LEFT, END_LINE_LEFT, (0, 255, 255), 12)
            cv2.line(frame, START_LINE_RIGHT, END_LINE_RIGHT, (255, 255, 0), 12)
        frame = cv2.addWeighted(overlay, 0.5, frame, 0.5, 0)
        for object_id in self.tracked_objects:
            car = self.tracked_objects[object_id]
            centroid = (
                car.x,
                car.y,
            )
            x1 = centroid[0] - 5
            y1 = centroid[1] - 5
            x2 = centroid[0] + 5
            y2 = centroid[1] + 5

            # Draw the bounding box of the object and the track id
            text = f"{car.id} ({car.last_direction_x} - {car.last_direction_y})"
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 3)

            if x1 + len(text) * 8 > frame.shape[1]:
                despl = x1 + len(text) * 8 - frame.shape[1] + 5
            else:
                despl = 0

            cv2.rectangle(frame, (x1 - 1 - despl, y1 - 20),
                          (x1 + len(text) * 8 - despl, y1), (0, 0, 255), -1)
            cv2.putText(
                frame,
                text,
                (x1 - despl + 5, y1 - 7),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.4,
                (255, 255, 255),
                2,
            )
            cv2.circle(frame, (car.x, car.y), 4, (0, 255, 0), -1)
            for i in range(1, len(car.path)):
                point1 = car.path[i - 1]
                point2 = car.path[i]
                cv2.line(frame, (point1), (point2), (0, 255, 0), 2)

        cv2.putText(frame, f"FPS: {fps:.2f}", (10, 35),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 6)
        cv2.putText(frame, f"Frame: {self.n_frame}", (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        cv2.putText(
            frame, f"Up - {self.count_up}", (START_LINE_B[0], START_LINE_B[1] -
                                             10), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 2
        )
        cv2.putText(
            frame, f"Down - {self.count_down}", (START_LINE_A[0], START_LINE_A[1] -
                                                 10), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 2
        )
        cv2.putText(
            frame, f"Left - {self.count_left}", (START_LINE_LEFT[0], START_LINE_LEFT[1] -
                                                 10), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 2
        )
        cv2.putText(
            frame, f"Right - {self.count_right}", (START_LINE_RIGHT[0], START_LINE_RIGHT[1] -
                                                   10), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 2
        )

        if print_output:
            cv2.imshow("Output", frame)
            cv2.waitKey(1)

        # Write the frame to the output video
        self.output.write(frame)

        return frame

    def identify_cars(self, centroids):
        for car in self.tracked_objects:
            self.tracked_objects[car].increment_not_found()
        for centroid in centroids:
            find_id = self.check_nearby(centroid)
            if not find_id:
                self.new_id((centroid[0], centroid[1]))
            else:
                self.update(find_id, centroid)

        to_delete = []
        for car in self.tracked_objects:
            if self.tracked_objects[car].frames_not_found > 3:
                self.tracked_objects[car].exit()
                to_delete.append(car)

        for car in to_delete:
            del self.tracked_objects[car]

    def update_counters(self):
        for car in self.tracked_objects:
            self.tracked_objects[car].updated_counter -= 1 if self.tracked_objects[car].updated_counter > 0 else 0
            x_last = self.tracked_objects[car].path[-1][0]
            y_last = self.tracked_objects[car].path[-1][1]
            x_last_5 = self.tracked_objects[car].path[-6][0] if len(
                self.tracked_objects[car].path) > 5 else self.tracked_objects[car].path[0][0]
            y_last_5 = self.tracked_objects[car].path[-6][1] if len(
                self.tracked_objects[car].path) > 5 else self.tracked_objects[car].path[0][1]

            if config["n_lines"] == 1:
                if (START_LINE_UNIQUE[0] <= x_last and x_last <= END_LINE_UNIQUE[0]) and (y_last_5 < START_LINE_UNIQUE[1] and y_last > START_LINE_UNIQUE[1]) and self.tracked_objects[car].updated_counter == 0:
                    self.count_down += 1
                    self.tracked_objects[car].updated_counter = 5
                elif (START_LINE_UNIQUE[0] <= x_last and x_last <= END_LINE_UNIQUE[0]) and (y_last_5 > START_LINE_UNIQUE[1] and y_last < START_LINE_UNIQUE[1]) and self.tracked_objects[car].updated_counter == 0:
                    self.count_up += 1
                    self.tracked_objects[car].updated_counter = 5
            else:
                if (START_LINE_A[0] <= x_last and x_last <= END_LINE_A[0]) and (y_last_5 < START_LINE_A[1] and y_last > START_LINE_A[1]) and self.tracked_objects[car].updated_counter == 0:
                    self.count_down += 1
                    self.tracked_objects[car].updated_counter = 5
                elif (START_LINE_B[0] <= x_last and x_last <= END_LINE_B[0]) and (y_last_5 > START_LINE_B[1] and y_last < START_LINE_B[1]) and self.tracked_objects[car].updated_counter == 0:
                    self.count_up += 1
                    self.tracked_objects[car].updated_counter = 5
            if config["check_vertical"]:
                if (START_LINE_LEFT[1] <= y_last and y_last <= END_LINE_LEFT[1]) and (x_last_5 < START_LINE_LEFT[0] and x_last > START_LINE_LEFT[0]) and self.tracked_objects[car].updated_counter == 0:
                    if self.tracked_objects[car].crossed_left == False and self.tracked_objects[car].crossed_right == False:
                        self.tracked_objects[car].crossed_left = True
                    self.tracked_objects[car].updated_counter = 5
                elif (START_LINE_RIGHT[1] <= y_last and y_last <= END_LINE_RIGHT[1]) and (x_last_5 > START_LINE_RIGHT[0] and x_last < START_LINE_RIGHT[0]) and self.tracked_objects[car].updated_counter == 0:
                    if self.tracked_objects[car].crossed_right == False and self.tracked_objects[car].crossed_left == False:
                        self.tracked_objects[car].crossed_right = True
                    self.tracked_objects[car].updated_counter = 5
                elif (START_LINE_LEFT[1] <= y_last and y_last <= END_LINE_LEFT[1]) and (x_last_5 > START_LINE_LEFT[0] and x_last < START_LINE_LEFT[0]) and self.tracked_objects[car].updated_counter == 0:
                    if self.tracked_objects[car].crossed_left == False and self.tracked_objects[car].crossed_right == True:
                        self.count_left += 1
                    self.tracked_objects[car].crossed_left = True
                    self.tracked_objects[car].updated_counter = 5
                elif (START_LINE_RIGHT[1] <= y_last and y_last <= END_LINE_RIGHT[1]) and (x_last_5 < START_LINE_RIGHT[0] and x_last > START_LINE_RIGHT[0]) and self.tracked_objects[car].updated_counter == 0:
                    if self.tracked_objects[car].crossed_right == False and self.tracked_objects[car].crossed_left == True:
                        self.count_right += 1
                    self.tracked_objects[car].crossed_right = True
                    self.tracked_objects[car].updated_counter = 5

    def get_counter_up(self):
        return self.count_up

    def get_counter_down(self):
        return self.count_down
    
    def get_counter_left(self):
        return self.count_left
    
    def get_counter_right(self):
        return self.count_right

    def get_current_up(self):
        current_up = 0
        for car in self.tracked_objects:
            if self.tracked_objects[car].last_direction_y == "up":
                current_up += 1
        return current_up

    def get_current_down(self):
        current_down = 0
        for car in self.tracked_objects:
            if self.tracked_objects[car].last_direction_y == "down":
                current_down += 1
        return current_down

    def get_current_left(self):
        current_left = 0
        for car in self.tracked_objects:
            if self.tracked_objects[car].last_direction_x == "left":
                current_left += 1
        return current_left

    def get_current_right(self):
        current_right = 0
        for car in self.tracked_objects:
            if self.tracked_objects[car].last_direction_x == "right":
                current_right += 1
        return current_right

    def get_total(self):
        return self.count_down + self.count_up
