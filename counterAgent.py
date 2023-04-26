
from math import sqrt
import numpy as np


class CounterAgent:
    def __init__(self, params, cnum):
        # Counterfactual agent moves randomly between four corners of the map
        self.params = params
        self.c_num = cnum
        self.x, self.y = (params.map_size/2) + np.random.uniform(0, 3), (params.map_size/2) + np.random.uniform(0, 3)
        self.x_, self.y_ = self.x, self.y
        # This is a randomly generated list from numpy for 12 map locations. I generated it once to fix it for each agent (up to 10)
        self.visit_order_all = [[5, 0, 4, 10, 11, 7, 3, 0, 6, 4, 3, 9, 9, 11, 2, 11, 3, 6, 5, 4, 11, 2, 0, 2, 5, 3, 7, 0, 1, 10, 4, 2, 4, 9, 10, 10, 1, 11, 10, 9],
                                [1, 3, 7, 4, 4, 9, 10, 3, 6, 8, 11, 1, 5, 11, 9, 3, 1, 9, 7, 10, 6, 6, 10, 2, 9, 7, 7, 5, 2, 8, 9, 10, 2, 4, 11, 5, 6, 5, 7, 7],
                                [9, 3, 8, 4, 8, 8, 1, 0, 8, 1, 5, 6, 10, 0, 9, 11, 2, 6, 1, 3, 1, 0, 5, 6, 0, 9, 2, 11, 10, 7, 3, 9, 4, 9, 6, 2, 10, 1, 2, 0],
                                [10, 9, 11, 10, 4, 11, 9, 3, 2, 0, 1, 5, 3, 3, 4, 4, 6, 8, 7, 7, 7, 7, 8, 11, 2, 4, 4, 9, 0, 4, 3, 0, 7, 8, 4, 5, 6, 1, 5, 3],
                                [6, 9, 7, 11, 0, 2, 0, 2, 0, 2, 10, 9, 3, 1, 4, 0, 6, 10, 4, 10, 5, 7, 3, 7, 9, 2, 4, 0, 3, 10, 4, 4, 7, 0, 9, 8, 3, 8, 7, 0],
                                [9, 1, 1, 11, 7, 5, 1, 6, 6, 1, 1, 11, 7, 2, 5, 11, 6, 6, 6, 3, 5, 7, 7, 8, 9, 1, 2, 6, 10, 9, 4, 7, 7, 7, 8, 2, 1, 0, 8, 0],
                                [7, 11, 0, 8, 10, 11, 0, 0, 5, 9, 4, 2, 6, 9, 4, 0, 3, 6, 3, 7, 5, 6, 6, 2, 7, 9, 3, 4, 1, 7, 11, 3, 11, 0, 0, 0, 9, 6, 1, 2],
                                [1, 0, 9, 5, 8, 2, 7, 10, 2, 0, 2, 0, 10, 10, 2, 8, 0, 0, 0, 0, 10, 1, 3, 9, 11, 8, 6, 2, 7, 1, 10, 0, 1, 8, 6, 9, 9, 8, 11, 6],
                                [3, 4, 11, 6, 11, 8, 4, 1, 10, 9, 10, 1, 4, 4, 10, 2, 7, 5, 5, 6, 0, 2, 10, 6, 7, 8, 0, 7, 11, 1, 9, 4, 3, 4, 8, 8, 3, 6, 7, 2],
                                [6, 5, 1, 8, 2, 11, 7, 3, 2, 11, 6, 2, 11, 11, 8, 6, 8, 9, 6, 6, 1, 11, 3, 7, 10, 1, 8, 0, 7, 0, 4, 6, 6, 11, 8, 2, 1, 0, 10, 0]]

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
        self.visit_order = self.visit_order_all[self.c_num]
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

