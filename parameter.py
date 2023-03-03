from random import random
from poi import tanh_poi,linear_poi
from agent import agent
def init_fn(n):
    return n+random(),n+random()    

class parameter:
    n_agents=5
    battery=20
    time_steps=50
    speed=2.0
    map_size=30

    poi_pos=[[1,1],[20,5],[25,25]]
    n_pois=len(poi_pos)
    poi_class=[tanh_poi]*2+[linear_poi]

    agent_class=[agent]*n_agents
    agent_pos=[init_fn(15) for i in range(n_agents)]

    interact_range=2.0
    n_sensors=4