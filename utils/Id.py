import os
import sys
import uuid


class Id:
    def __init__(self, x, y):
        self.id = uuid.uuid4()[:4]
        self.x = x
        self.y = y
        self.first_cor = (x, y)
        self.path = []
        self.last_cor = None
        self.frames_not_updated = 0

    def update_centroid(self, x, y):
        self.x = x
        self.y = y
        self.path.append((x, y))
        self.frames_not_updated = 0

    def increment_not_updated(self):
        self.frames_not_updated += 1
