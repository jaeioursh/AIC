from math import sqrt
import numpy as np


class CounterAgent:
    def __init__(self, params, poi_xy, cf_xy, cf_i):
        # Counterfactual agent moves randomly between four corners of the map
        self.params = params
        try:
            self.x, self.y = cf_xy
        except TypeError:
            print("something went wrong here")
        self.x_, self.y_ = self.x, self.y
        self.obs_amt = 0.1
        self.idx = cf_i

        self.poi_visit = params.poi_visit
        self.points = poi_xy
        # Randomly generated list of POI visits
        # self.visit_order = np.random.randint(0, params.n_pois, 30)

        # This pre-determines the visit order for each CF for repeatability
        self.all_cfs_visits = [
            [9, 14, 14, 5, 1, 11, 9, 3, 1, 0, 8, 5, 8, 6, 5, 3, 4, 3, 11, 2, 0, 3, 6, 3, 7, 2, 1, 9, 0, 15],
            [6, 15, 6, 7, 5, 4, 12, 0, 6, 0, 15, 15, 11, 6, 12, 1, 5, 10, 6, 1, 5, 5, 10, 5, 10, 7, 9, 0, 3, 6],
            [7, 15, 15, 7, 13, 12, 13, 0, 6, 3, 7, 2, 15, 6, 3, 9, 14, 2, 14, 8, 6, 9, 6, 9, 14, 13, 3, 6, 7, 7],
            [15, 5, 9, 11, 7, 1, 5, 12, 4, 15, 8, 1, 7, 10, 9, 6, 11, 15, 2, 10, 15, 5, 10, 0, 12, 6, 9, 15, 0, 1],
            [9, 5, 14, 0, 12, 6, 1, 4, 11, 3, 7, 14, 4, 4, 3, 14, 6, 9, 7, 0, 11, 0, 8, 9, 1, 3, 13, 8, 8, 10],
            [0, 13, 5, 14, 5, 2, 4, 13, 13, 10, 14, 13, 10, 15, 7, 11, 0, 6, 11, 8, 12, 2, 7, 8, 9, 14, 12, 7, 5, 0],
            [7, 2, 11, 0, 11, 1, 12, 1, 12, 3, 11, 11, 14, 2, 0, 2, 4, 9, 2, 9, 9, 3, 5, 2, 11, 15, 15, 0, 4, 13],
            [1, 0, 7, 12, 8, 10, 8, 15, 2, 7, 5, 5, 7, 5, 10, 10, 8, 5, 1, 15, 15, 11, 0, 13, 6, 15, 6, 6, 6, 14],
            [6, 9, 14, 3, 2, 0, 14, 15, 4, 4, 1, 8, 6, 3, 14, 1, 12, 11, 9, 7, 10, 3, 0, 9, 4, 1, 10, 5, 14, 2],
            [8, 2, 7, 3, 5, 14, 9, 7, 7, 7, 11, 2, 11, 7, 3, 8, 1, 0, 13, 3, 13, 4, 8, 11, 0, 12, 1, 3, 10, 15],
            [12, 9, 3, 14, 2, 9, 7, 6, 5, 0, 3, 9, 2, 9, 10, 10, 9, 15, 8, 0, 9, 13, 13, 3, 8, 3, 14, 8, 8, 1],
            [5, 0, 0, 6, 4, 12, 13, 8, 15, 5, 10, 10, 15, 0, 14, 0, 11, 14, 9, 4, 11, 0, 1, 5, 4, 13, 13, 8, 3, 3],
            [7, 5, 5, 8, 1, 2, 6, 5, 15, 4, 5, 12, 6, 6, 6, 0, 12, 11, 13, 0, 15, 9, 0, 15, 11, 2, 7, 13, 7, 13],
            [12, 7, 13, 3, 4, 5, 10, 4, 15, 0, 4, 6, 3, 13, 8, 5, 11, 9, 12, 7, 15, 5, 1, 0, 13, 11, 14, 0, 12, 8],
            [15, 2, 4, 13, 15, 4, 14, 2, 7, 14, 0, 12, 14, 11, 15, 1, 15, 12, 7, 14, 2, 9, 3, 6, 1, 9, 8, 15, 8, 9],
            [13, 5, 1, 13, 7, 7, 13, 10, 12, 2, 2, 0, 11, 11, 8, 2, 11, 11, 2, 5, 10, 5, 0, 1, 6, 10, 8, 4, 1, 3],
            [2, 10, 1, 5, 0, 14, 12, 5, 0, 13, 4, 0, 7, 13, 15, 9, 13, 0, 7, 13, 1, 11, 6, 1, 14, 4, 6, 1, 4, 2],
            [2, 12, 8, 8, 15, 3, 2, 1, 12, 13, 13, 6, 2, 11, 15, 10, 0, 3, 4, 0, 9, 14, 1, 14, 9, 5, 9, 12, 5, 10],
            [6, 8, 9, 3, 1, 6, 2, 9, 8, 15, 15, 13, 4, 7, 2, 6, 4, 15, 14, 12, 10, 14, 8, 3, 3, 4, 0, 4, 0, 5],
            [1, 0, 10, 7, 3, 4, 12, 11, 9, 13, 12, 5, 13, 3, 3, 15, 2, 0, 11, 8, 14, 9, 0, 15, 0, 10, 1, 9, 6, 9],
            [1, 3, 7, 5, 4, 5, 10, 15, 7, 7, 14, 15, 15, 8, 14, 13, 3, 4, 8, 2, 7, 10, 11, 10, 3, 12, 1, 2, 10, 2],
            [5, 7, 11, 13, 7, 6, 13, 2, 10, 8, 14, 15, 4, 4, 6, 9, 3, 6, 14, 13, 0, 9, 9, 6, 13, 13, 6, 13, 10, 6],
            [4, 4, 8, 3, 0, 0, 9, 10, 7, 11, 10, 1, 9, 8, 5, 5, 3, 7, 0, 4, 6, 12, 13, 15, 9, 10, 14, 5, 2, 1],
            [1, 7, 14, 10, 0, 10, 8, 4, 3, 1, 14, 6, 12, 14, 8, 4, 8, 13, 5, 14, 13, 6, 13, 4, 0, 3, 11, 7, 1, 2],
            [3, 6, 12, 6, 14, 0, 0, 0, 0, 4, 14, 0, 9, 0, 11, 0, 11, 13, 7, 6, 4, 4, 15, 9, 1, 2, 14, 3, 9, 14],
            [2, 8, 7, 0, 0, 8, 8, 11, 9, 6, 11, 3, 4, 13, 9, 0, 6, 8, 5, 1, 5, 0, 5, 3, 0, 13, 1, 13, 2, 15],
            [14, 10, 13, 6, 2, 3, 10, 1, 1, 15, 13, 13, 13, 10, 12, 6, 9, 9, 2, 9, 2, 14, 14, 2, 7, 0, 1, 8, 3, 2],
            [8, 12, 5, 8, 3, 4, 9, 6, 0, 0, 4, 9, 6, 3, 1, 3, 9, 13, 10, 9, 7, 11, 13, 10, 7, 3, 14, 7, 8, 7],
            [4, 9, 2, 4, 11, 9, 6, 5, 3, 8, 0, 12, 15, 15, 9, 3, 11, 4, 9, 12, 10, 11, 15, 3, 0, 5, 8, 6, 15, 15],
            [11, 0, 8, 2, 5, 2, 9, 13, 2, 6, 8, 15, 15, 6, 3, 7, 8, 7, 11, 10, 8, 4, 3, 9, 8, 14, 7, 6, 14, 14]]
        # self.visit_order = self.all_cfs_visits[self.idx]
        self.visit_order = self.all_cfs_visits[np.random.randint(0, 30)]
        self.pt_num = 0
        self.curr_goal = self.points[self.visit_order[self.pt_num]]

    def reset(self):
        self.x, self.y = self.x_, self.y_
        self.visit_order = self.all_cfs_visits[np.random.randint(0, 30)]
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
            # This loops it back to the start so the cf never runs out of things to do
            if self.pt_num >= len(self.visit_order):
                self.pt_num = 0
            self.curr_goal = self.points[self.visit_order[self.pt_num]]
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
