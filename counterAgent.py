
from math import sqrt
import numpy as np


class CounterAgent:
    def __init__(self, params, cnum):
        # Counterfactual agent moves randomly between four corners of the map
        self.params = params
        self.c_num = cnum
        self.x, self.y = (params.map_size/2) + np.random.uniform(0, 3), (params.map_size/2) + np.random.uniform(0, 3)
        self.x_, self.y_ = self.x, self.y
        # This is a randomly generated list from numpy for 12 map locations. I generated it once to fix it for each agent (up to 5)
        self.visit_order_all = [[0,  4,  6,  8,  5,  5,  4, 10,  4,  1,  9,  3,  2, 11,  4, 11, 2,  6,  7,  7,  9,  4, 8,  9,  2, 10,  4,  6, 11,  9],
                                [8,  2,  7,  9,  3,  0,  2,  6,  2,  1,  5,  6,  9,  9,  6,  9, 0,  0,  9,  1,  2,  3, 4,  0,  2, 10,  8,  0,  8,  1],
                                [9,  5,  3,  0,  4,  4,  9,  4, 11,  3,  9, 10, 10,  9,  6,  1, 5,  4,  7,  3,  6,  7, 1,  2,  0,  4,  6,  2,  1,  9],
                                [8,  6, 11,  8,  2,  1,  0,  2,  4,  9,  0,  6,  2,  9,  5, 11, 9,  1,  8,  4,  1,  9, 5,  1,  5,  1,  1,  8,  3,  2],
                                [0,  5, 10, 10,  4,  6,  0,  5,  4, 11, 11,  4,  2,  6,  9,  7, 8,  4,  6,  4,  1,  4, 9,  3,  2,  1, 11,  1,  2,  9]]
        self.points = self.setup_visit_points()
        self.visit_order = self.visit_order_all[self.c_num]
        self.pt_num = 0
        self.curr_goal = self.points[self.visit_order[self.pt_num]]

    def setup_visit_points(self):
        point_diffs = [2, 5, 8]
        corners = np.array([[0, 0], [0, self.params.map_size], [self.params.map_size, 0], [self.params.map_size, self.params.map_size]])
        points = []
        for p in point_diffs:
            diffs = np.array([[p, p], [p, -p], [-p, p], [-p, -p]])
            points.extend(corners + diffs)
        return np.array(points)

    def reset(self):
        self.x, self.y = self.x_, self.y_
        self.pt_num = 0
        self.curr_goal = self.points[self.visit_order[self.pt_num]]

    def move(self):
        # Calc distance to current goal
        x, y = self.curr_goal
        r = sqrt((x - self.x) ** 2.0 + (y - self.y) ** 2.0) + 1e-9

        # If I'm at the goal, change to a new goal
        if r < 1:
            self.pt_num += 1
            try:
                self.curr_goal = self.points[self.visit_order[self.pt_num]]
            except IndexError:
                print(self.c_num, self.pt_num)
                print(self.visit_order)
                exit()
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
    ag = CounterAgent(p, 0)

    for _ in range(10):
        ag.move()

