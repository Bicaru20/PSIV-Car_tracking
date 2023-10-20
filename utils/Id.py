import os
import sys
import uuid


class Id:
    def __init__(self, id, x, y):
        self.id = uuid.uuid4()
        self.x = x
        self.y = y
        self.last_update = 0
        self.first_cor = (x, y)
        self.last_cor = (x, y)

    def update_centroid(self, x, y):
        self.x = x
        self.y = y
        self.last_cor = (x, y)
        self.last_update = 0

    def increment_last_update(self):
        self.last_update += 1
