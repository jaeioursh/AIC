
from math import sqrt
import numpy as np


class CounterAgent:
    def __init__(self, params, cnum, poi_xy):
        # Counterfactual agent moves randomly between four corners of the map
        self.params = params
        self.c_num = cnum
        self.x, self.y = (params.map_size/2) + np.random.uniform(0, 3), (params.map_size/2) + np.random.uniform(0, 3)
        self.x_, self.y_ = self.x, self.y
        self.obs_amt = 0.1

        self.poi_visit = params.poi_visit
        self.points = poi_xy
        # Randomly generated list of
        self.visit_order = np.random.randint(0, params.n_pois, 30)
        self.pt_num = 0
        self.curr_goal = self.points[self.visit_order[self.pt_num]]

    def setup_visit_points(self):
        # Use this if the visit locations are independent of the POI locations
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

        at_goal = False
        # If I'm at the goal, change to a new goal
        if r < 1:
            at_goal = True
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

        # If agent is not visiting POIs, return false as a flag to never impact completeness of POIs
        if not self.poi_visit:
            return False

        # Otherwise, if agent reaches a POI, return the POI number so it can impact POI
        if at_goal:
            return self.visit_order[self.pt_num]
        else:
            return False


class DumbParam:
    def __init__(self):
        self.map_size = 30


if __name__ == '__main__':
    p = DumbParam()
    ag = CounterAgent(p, 0)

    for _ in range(10):
        ag.move()

