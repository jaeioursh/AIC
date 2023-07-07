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
            [12, 12, 10, 14, 15, 1, 1, 0, 3, 15, 9, 10, 4, 11, 9, 1, 12, 5, 13, 2, 9, 3, 14, 2, 10, 12, 4, 4, 15, 10],
            [14, 12, 9, 12, 2, 14, 15, 15, 14, 0, 13, 6, 1, 10, 3, 3, 14, 1, 0, 8, 4, 5, 4, 14, 11, 6, 0, 10, 14, 8],
            [5, 13, 9, 3, 15, 0, 2, 1, 13, 8, 4, 7, 8, 1, 9, 12, 11, 4, 2, 1, 9, 12, 1, 0, 7, 2, 8, 7, 13, 1],
            [7, 14, 3, 3, 15, 1, 8, 6, 3, 10, 7, 0, 2, 6, 2, 0, 12, 15, 8, 9, 10, 4, 12, 12, 11, 2, 8, 6, 3, 11],
            [14, 5, 9, 13, 0, 5, 12, 8, 12, 8, 3, 15, 15, 9, 10, 7, 2, 2, 3, 6, 10, 2, 0, 15, 3, 4, 3, 6, 1, 3],
            [2, 14, 8, 9, 11, 9, 5, 15, 13, 12, 3, 14, 1, 7, 14, 7, 1, 12, 5, 4, 5, 8, 12, 6, 6, 3, 9, 7, 4, 15],
            [10, 0, 3, 1, 6, 1, 1, 8, 9, 6, 0, 7, 7, 8, 7, 0, 0, 9, 0, 13, 14, 7, 5, 4, 3, 10, 1, 10, 14, 1],
            [5, 5, 8, 0, 7, 3, 0, 8, 2, 3, 11, 15, 12, 12, 1, 11, 6, 10, 5, 0, 8, 14, 3, 2, 12, 11, 1, 11, 9, 10],
            [7, 6, 3, 6, 10, 12, 11, 12, 4, 1, 10, 12, 11, 14, 1, 15, 7, 1, 2, 12, 7, 15, 9, 4, 5, 8, 9, 12, 2, 12],
            [2, 10, 11, 10, 14, 6, 9, 6, 11, 8, 1, 8, 11, 12, 15, 15, 11, 14, 8, 2, 0, 8, 1, 12, 15, 9, 12, 6, 7, 12]]
        self.visit_order = self.all_cfs_visits[self.idx]
        self.pt_num = 0
        self.curr_goal = self.points[self.visit_order[self.pt_num]]

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
                print(self.pt_num)
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
