import uuid


class Id:
    def __init__(self, x, y):
        self.id = uuid.uuid4()[:4]
        self.x = x
        self.y = y
        self.first_cor = (x, y)
        self.path = []
        self.last_cor = None
        self.last_updated = False
        self.frames_not_updated = 0
        self.last_direction_y = None  # up, down, None
        self.last_direction_x = None  # left, right, None

    def update_centroid(self, x, y):
        self.x = x
        self.y = y
        self.path.append((x, y))
        self.last_updated = True
        self.frames_not_updated = 0
        self.last_direction_y = "left" if self.path[-2][0] + \
            5 < self.path[-1][0] else "right" if self.path[-2][0] - 5 > self.path[-1][0] else None
        self.last_direction_x = "up" if self.path[-2][1] + \
            5 < self.path[-1][1] else "down" if self.path[-2][1] - 5 > self.path[-1][1] else None

    def increment_not_updated(self):
        self.frames_not_updated += 1
        self.last_updated = False

    def exit(self):
        self.last_cor = (self.x, self.y)
