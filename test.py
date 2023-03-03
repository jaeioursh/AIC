from view import view
from parameter import parameter
from aic import aic

import numpy as np

params=parameter()
env=aic(params)
for i in range(1):
    print(env.poi_types)
    state=env.state()
    #view(env,state)
    a=np.array([[0]*8+[0.5,0.5,0.5]]*5)
    #for i in range(len(a)):
    #    a[i,i]=1
    a[:,0]=2
    #print(a)
    env.action(a)