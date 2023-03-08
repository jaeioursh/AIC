from view import view
from parameter import parameter
from aic import aic

import numpy as np

params = parameter()
env = aic(params)
for i in range(50):
    state = env.state()
    view(env, state, i)
    # a = np.array([[0] * 8 + [0.5, 0.5, 0.5]] * 5)
    a = np.zeros((params.n_agents, env.action_size()))
    a[:, -3:] = 0.5
    a[:, 1] = 1
    # print(a)
    env.action(a)
