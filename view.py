import numpy as np
import matplotlib.pyplot as plt
plt.ion()

def view(env,state=None):
    
    plt.clf()
    if state is not None:
        plt.subplot(1,2,1)
    agents=np.array([[a.x,a.y] for a in env.agents])
    plt.scatter(agents.T[0],agents.T[1],marker="o")

    pois=np.array([[p.x,p.y] for p in env.pois])
    colors=["b","k","r","c"]
    c=[colors[t] for t in env.poi_types]
    plt.scatter(pois.T[0],pois.T[1],marker="v",c=c)

    plt.xlim([0,env.params.map_size])
    plt.ylim([0,env.params.map_size])


    if state is not None:
        plt.subplot(1,2,2)
        plt.imshow(state)
    plt.pause(0.1)