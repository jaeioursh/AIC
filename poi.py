from math import tanh


class poi:
    def __init__(self, x, y, work, params):
        self.new_complete = None
        self.x = x
        self.y = y
        self.type_val = 1.0

        self.work = work  # work done / x val of completeness function
        self.work_ = work  # For resetting
        self.complete = self.fn(work, 1)  # how completed it is based on work done / y value of completeness function

        self.params = params
        self.dvec = [0] * params.n_agents

    def fn(self, work, eff):
        # Completeness depends on the previous amount done and the total effort put in
        return work * eff

    def reset(self):
        self.work = self.work_
        self.complete = self.fn(self.work, 1)
        self.dvec = [0] * self.params.n_agents

    def observe(self, agent_idx, effort, speed):
        self.work += speed
        self.new_complete = max(self.fn(self.work, effort),self.complete)
        self.dvec[agent_idx] += self.new_complete - self.complete
        self.complete = self.new_complete


class linear_poi(poi):
    def __init__(self, x, y, params):
        super().__init__(x, y, 0.0, params)
        self.type_val = 0.1

    def fn(self, work, eff):
        # Completeness depends on the previous amount done and the total effort put in
        return min(work * eff * self.type_val, 1)


class tanh_poi(poi):
    def __init__(self, x, y, params):
        super().__init__(x, y, 0.0, params)
        self.type_val = 0.1

    def fn(self, work, eff):
        # Completeness depends on the previous amount done and the total effort put in
        return tanh(work * eff * self.type_val)
