import numpy as np
import matplotlib.pyplot as plt
plt.ion()

def view(env):
    
    plt.clf()

    agents=np.array([[a.x,a.y] for a in env.agents])
    plt.scatter(agents.T[0],agents.T[1],marker="o")

    pois=np.array([[p.x,p.y] for p in env.pois])
    plt.scatter(pois.T[0],pois.T[1],marker="v")

    plt.xlim([0,env.params.map_size])
    plt.ylim([0,env.params.map_size])
    plt.pause(0.1)