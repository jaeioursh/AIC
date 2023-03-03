from view import view
from parameter import parameter
from aic import aic

import numpy as np

params=parameter()
env=aic(params)
for i in range(100):
    
    state=env.state()
    view(env,state)
    a=np.array([[0]*8+[0.5,0.5,0.5]]*5)
    a[:,1]=1
    print(a)
    env.action(a)