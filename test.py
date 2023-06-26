from view import view
from pymap_elites_multiobjective.parameters.parameters349 import Parameters as params
from aic import aic

import numpy as np

# params.counter_move = False
env = aic(params)


for i in range(50):
    state = env.state()
    max_quad = np.argmax(state[0, 8:16])
    g = sum(env.G())
    view(env, i, g, max_quad, state, 0.3)
    idxs = [0]
    if not i % 8:
        a = np.zeros((params.n_agents, env.action_size()))
        a[:, -3:] = 1.0
        # rand_choice = np.random.randint(0, a.shape[1] - 3)
        a[0, max_quad] = 1
    env.action(a)
