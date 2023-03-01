from random import random

def init_fn(n):
    return n+random(),n+random()    

class parameter:
    n_agents=5
    battery=20
    time_steps=50
    speed=2.0
    map_size=30
    agent_init=lambda: init_fn(15)