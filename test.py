from view import view
from parameter import parameter
from aic import aic


params=parameter()
env=aic(params)
for i in range(100):
    view(env)
    print(env.state())
    a=[[0]*1+[1]+[0]*6+[0.5,0.5,0.5]]*5
    print(a)
    env.action(a)