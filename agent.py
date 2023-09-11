from math import sqrt


class agent:

    def __init__(self, x, y, params):
        self.params = params
        self.x, self.y = x, y
        self.x_, self.y_ = self.x, self.y  # to reset values
        self.top_speed = params.speed
        # self.battery = params.battery
        self.battery = 18
        self.min_dist = []
        self.max_dist = []
        self.avg_dist = []

    def reset(self):
        # self.battery = self.params.battery
        self.battery = 18
        self.x, self.y = self.x_, self.y_
        self.min_dist = []
        self.max_dist = []
        self.avg_dist = []

    def move(self, x, y, velocity):
        r = sqrt((x - self.x) ** 2.0 + (y - self.y) ** 2.0) + 1e-9
        dx = (x - self.x) / r
        dy = (y - self.y) / r
        self.x += dx * self.top_speed * velocity
        self.y += dy * self.top_speed * velocity
        self.battery -= velocity

    def interact(self, effort):
        self.battery -= effort
