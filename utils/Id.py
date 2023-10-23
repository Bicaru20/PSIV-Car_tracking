import uuid


class Id:
    def __init__(self, x, y):
        self.id = str(uuid.uuid4())[0:4]
        self.x = x
        self.y = y
        self.first_cor = (x, y)
        self.path = [(x, y)]
        self.last_cor = None
        self.last_updated = True
        self.frames_not_found = 0
        self.last_direction_y = None  # up, down, None
        self.last_direction_x = None  # left, right, None
        self.updated_counter = 0
        self.crossed_right = False
        self.crossed_left = False

    def update_centroid(self, x, y, nearby_movement=False):
        if nearby_movement:
            self.x = x
            self.y = y
            self.path.append((x, y))
            self.frames_not_found = 0
        if not nearby_movement:
            self.x = x
            self.y = y
            self.path.append((x, y))
            self.frames_not_found = 0
            self.last_updated = True
        if len(self.path) > 1:
            self.update_last_direction()

    def increment_not_found(self):
        self.frames_not_found += 1
        self.last_updated = False

    def exit(self):
        self.last_cor = (self.x, self.y)

    def update_last_direction(self):
        alfa = 2
        self.last_direction_y = "left" if self.path[-2][0] > self.path[-1][0] else "right"
        self.last_direction_x = "up" if self.path[-2][1] > self.path[-1][1] else "down"
