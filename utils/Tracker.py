from helper import create_video_writer
from deep_sort.tools import generate_detections as gdet
from deep_sort.deep_sort.detection import Detection
from deep_sort.deep_sort import nn_matching
from deep_sort.deep_sort.tracker import Tracker
from collections import deque
from ultralytics import YOLO
import datetime
import os
import cv2
import numpy as np
from scipy.spatial import distance

from Id import Id

START_LINE_A = (114, 695)
END_LINE_A = (268, 695)
START_LINE_B = (278, 695)
END_LINE_B = (420, 695)


class Tracker:
    def __init__(self, cap):
        self.cap = cap  # Video capture
        self.total_up = 0
        self.total_down = 0
        self.n_frames = 0  # Number of frame
        self.tracked_objects = {}  # Dictionary to store tracked objects by their IDs
        # Output video
        self.output = cv2.VideoWriter(os.path.join(os.path.dirname(
            os.path.dirname(__file__)), 'output/output.mp4'), cv2.VideoWriter_fourcc(*'MP4V'), 30, (int(cap.get(3)), int(cap.get(4))), True)

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

    def increment_last_updates(self):
        # Increment the last_update counters for objects that were not updated in the current iteration
        for object_id in self.tracked_objects:
            self.tracked_objects[object_id].increment_last_update()

    def get_tracked_objects(self):
        # Get a list of tracked objects
        return list(self.tracked_objects.values())

    def update_output(self, frame, print_output=False):
        # Update the output video with the current frame
        overlay = frame.copy()
        cv2.line(frame, START_LINE_A, END_LINE_A, (0, 255, 0), 12)
        cv2.line(frame, START_LINE_B, END_LINE_B, (255, 0, 0), 12)
        frame = cv2.addWeighted(overlay, 0.5, frame, 0.5, 0)
        for object_id in self.tracked_objects:
            if not self.tracked_objects[object_id].last_updated:
                continue
            centroid = (
                self.tracked_objects[object_id].x, self.tracked_objects[object_id].y)
            x1 = centroid[0] - 5
            y1 = centroid[1] - 5
            x2 = centroid[0] + 5
            y2 = centroid[1] + 5

            # Draw the bounding box of the object and the track id
            text = f"{object_id.id} ({object_id.last_direction_x} - {object_id.last_direction_y})"
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 3)
            cv2.rectangle(
                frame, (x1 - 1, y1 - 20), (x1 + len(text)
                                           * 12, y1), (0, 0, 255), -1
            )
            cv2.putText(
                frame,
                text,
                (x1 + 5, y1 - 8),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 255, 255),
                2,
            )
            cv2.circle(frame, (object_id.x, object_id.y), 4, (0, 255, 0), -1)
            for i in range(1, len(object_id.path)):
                point1 = object_id.path[i - 1]
                point2 = object_id.path[i]
                cv2.line(frame, (point1), (point2), (0, 255, 0), 2)

            fps = self.cap.get(cv2.CAP_PROP_FPS)
            cv2.putText(frame, f"FPS: {fps:.2f}", (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 8)
            cv2.putText(
                frame, f"Up - {self.total_up}", (START_LINE_A[0] - 20, START_LINE_A[1] -
                                                 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2
            )
            cv2.putText(
                frame, f"Down - {self.total_down}", (START_LINE_B[0] - 20, START_LINE_B[1] -
                                                     10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2
            )

        if print_output:
            # Show the output frame
            cv2.imshow("Output", frame)
            print("-" * 50)
            print("Counter Up: ", self.total_up)
            print("Counter Down: ", self.total_down)
            print("-" * 50)

        # Write the frame to the output video
        self.output.write(frame)

        return frame
