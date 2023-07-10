from AIC.view import view
from AIC.parameter import parameter
from AIC.aic import aic

import numpy as np

params = parameter()
env = aic(params)
for i in range(100):
    state = env.state()
    g=sum(env.G())
    view(env, i, g, state, 0.3)
    # a = np.array([[0] * 8 + [0.5, 0.5, 0.5]] * 5)
    a = np.zeros((params.n_agents, env.action_size()))
    a[:, -3:] = 1.0
    
    idxs=[0,1,6,7,7]
    if i>10:
        a[-3:]=0
        idxs=[2,3,4,5,5]
        
    a[range(len(idxs)), idxs] = 1
    # print(a)
    env.action(a)
