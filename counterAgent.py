
from math import sqrt
import numpy as np


class CounterAgent:
    def __init__(self, params):
        # Counterfactual agent moves randomly between four corners of the map
        self.params = params
        self.x, self.y = params.map_size + np.random.random(), params.map_size + np.random.random()
        self.x_, self.y_ = self.x, self.y
        self.points = [[1, 1], [params.map_size - 1, 1],
                       [1, params.map_size - 1], [params.map_size - 1, params.map_size - 1]]
        self.pt_idx = np.random.randint(0, 4)
        self.curr_goal = self.points[self.pt_idx]

    def reset(self):
        self.x, self.y = self.x_, self.y_
        self.curr_goal = [1, 1]
        self.pt_idx = 0

    def move(self):
        # Calc distance to current goal
        x, y = self.curr_goal
        r = sqrt((x - self.x) ** 2.0 + (y - self.y) ** 2.0) + 1e-9

        # If I'm at the goal, change to a new goal
        if r < 1:
            new_idx = np.random.randint(0, 4)
            while_brk = 0
            while new_idx == self.pt_idx and while_brk < 5:
                new_idx = np.random.randint(0, 4)
                while_brk += 1
            self.pt_idx = new_idx
            self.curr_goal = self.points[self.pt_idx]
            x, y = self.curr_goal
            r = sqrt((x - self.x) ** 2.0 + (y - self.y) ** 2.0) + 1e-9

        # Move
        self.x += (x - self.x) / r
        self.y += (y - self.y) / r


class DumbParam:
    def __init__(self):
        self.map_size = 30


if __name__ == '__main__':
    p = DumbParam()
    ag = CounterAgent(p)

    for _ in range(10):
        ag.move()

