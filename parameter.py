from random import random
from poi import tanh_poi
def init_fn(n):
    return n+random(),n+random()    

class parameter:
    n_agents=5
    battery=20
    time_steps=50
    speed=2.0
    map_size=30
    agent_init=lambda: init_fn(15)
    poi_pos=[[0,1],[20,5],[30,2]]
    n_pois=len(poi_pos)
    poi_class=[tanh_poi]*n_pois