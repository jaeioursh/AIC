from math import tanh
from matplotlib import pyplot as plt
import numpy as np


class poi:
    def __init__(self, x, y, work, params):
        self.new_complete = None
        self.x = x
        self.y = y
        self.type_val = 1.0

        self.work = work  # work done / x val of completeness function
        self.work_ = work  # For resetting
        self.complete = self.fn(work, 1)  # how completed it is based on work done / y value of completeness function
        self.g_complete = self.fn(work, 1)
        self.params = params
        self.dvec = [0] * params.n_agents

    def fn(self, work, eff):
        # Completeness depends on the previous amount done and the total effort put in
        return work * eff

    def reset(self):
        self.work = self.work_
        self.complete = self.fn(self.work, 1)
        self.g_complete = self.fn(self.work, 1)
        self.dvec = [0] * self.params.n_agents
        self.new_complete = None

    def observe(self, agent_idx, effort, speed):
        self.work += speed
        self.new_complete = max(self.fn(self.work, effort), self.complete)
        self.dvec[agent_idx] += self.new_complete - self.complete
        self.complete = self.new_complete
        self.g_complete = max(self.fn(self.work, effort), self.g_complete)

    def cf_observe(self, effort):
        self.complete = min(self.complete + effort, 1)


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


if __name__ == '__main__':

    ts = [0.001, 0.1, 0.3, 0.5]

    x = np.linspace(0, 3)
    y = np.linspace(0, 3)
    X, Y = np.meshgrid(x, y)


    def th_fun(work, eff, type_val):
        # Completeness depends on the previous amount done and the total effort put in
        th = []
        for e in eff:
            th.append(tanh(work * e * type_val))
        return th

    def lin(work, eff, type_val):
        return work * eff * type_val

    tv_l = 0.1
    tv_t = 0.1
    z_l = lin(X, Y, tv_l)
    z_t = []
    for x0 in x:
        z_t.append(th_fun(x0, y, tv_t))

    max_val = np.max([np.max(z_l), np.max(z_t)])
    plt.subplot(1,2,1)
    plt.contourf(X, Y, z_t, vmax=max_val)
    plt.title(f'Tanh {tv_t}')

    plt.subplot(1,2,2)
    plt.contourf(X, Y, z_l, vmax=max_val)
    plt.colorbar()

    plt.title(f'Lin {tv_l}')
    plt.show()

