from math import sqrt


class agent:

    def __init__(self, x, y, params):
        self.params = params
        self.x, self.y = x, y
        self.x_, self.y_ = self.x, self.y  # to reset values
        self.top_speed = params.speed
        self.battery = params.battery
        self.min_dist = 100
        self.max_dist = 0
        self.avg_dist = [0, 0]

    def reset(self):
        self.battery = self.params.battery
        self.x, self.y = self.x_, self.y_
        self.min_dist = 100
        self.max_dist = 0
        self.avg_dist = [0, 0]

    def move(self, x, y, movement):
        r = sqrt((x - self.x) ** 2.0 + (y - self.y) ** 2.0) + 1e-9
        dx = (x - self.x) / r
        dy = (y - self.y) / r
        self.x += dx * self.top_speed * movement
        self.y += dy * self.top_speed * movement
        self.battery -= movement * movement

    def interact(self, effort, speed):
        self.battery -= effort * speed
