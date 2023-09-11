from math import tanh
from matplotlib import pyplot as plt
import numpy as np


class poi:
    def __init__(self, x, y, params):
        self.params = params
        self.x = x
        self.y = y
        self.type_val = 1.0

        self.work = 0   # How much effort has been put in so far (x val of function)
        self.complete = 0
        self.g_complete = 0
        self.dvec = [0] * params.n_agents

    def reset(self):
        # self.work = self.work_
        self.complete = 0
        self.g_complete = 0
        self.dvec = [0] * self.params.n_agents
        self.work = 0

    def fn(self, ):
        return min(self.work, 1)

    def observe(self, agent_idx, effort):
        # This is not limited to 1
        self.work += effort
        # This is limited to 1
        new_complete = self.fn()
        self.dvec[agent_idx] += new_complete - self.complete
        self.complete = new_complete
        self.g_complete = new_complete

    def cf_observe(self, effort):
        self.complete = min(self.complete + effort, 1)


class linear_poi(poi):
    def __init__(self, x, y, params):
        super().__init__(x, y, params)
        self.type_val = 0.5

    def fn(self):
        # Completeness depends on the previous amount done and the total effort put in
        return min(self.work * self.type_val, 1)


class tanh_poi(poi):
    def __init__(self, x, y, params):
        super().__init__(x, y, params)
        self.type_val = 1.3

    def fn(self):
        # Completeness depends on the previous amount done and the total effort put in
        return min(tanh(self.work * self.type_val), 1)


if __name__ == '__main__':
    x = np.linspace(0, 3)

    def th_fun(eff, type_val):
        # Completeness depends on the previous amount done and the total effort put in
        th = []
        for e in eff:
            th.append(min(1.0, tanh(e * type_val)))
        return th

    def lin(eff, type_val):
        vals = eff * type_val
        vals[vals > 1.] = 1.
        return vals

    tv_l = 0.5
    tv_t = 1.3
    z_l = lin(x, tv_l)
    z_t = th_fun(x, tv_t)

    max_val = np.max([np.max(z_l), np.max(z_t)])
    plt.subplot(1,2,1)
    plt.plot(x, z_t)
    plt.title(f'Tanh {tv_t}')

    plt.subplot(1,2,2)
    plt.plot(x, z_l)

    plt.title(f'Lin {tv_l}')
    plt.show()

