import numpy as np
import matplotlib.pyplot as plt



def view(env, ts,g, state=None, dly=0.1):
    plt.ion()

    plt.clf()
    if state is not None:
        plt.subplot(1, 2, 1)
    agents = np.array([[a.x, a.y] for a in env.agents])
    plt.scatter(agents.T[0], agents.T[1], marker="o")

    pois = np.array([[p.x, p.y] for p in env.pois])
    colors = ["b", "k", "r", "c"]
    c = [colors[t] for t in env.poi_types]
    plt.scatter(pois.T[0], pois.T[1], marker="v", c=c)

    plt.xlim([-2, env.params.map_size + 2])
    plt.ylim([-2, env.params.map_size + 2])

    plt.title(f'time: {ts} G: {g:.2f}')

    if state is not None:
        plt.subplot(1, 2, 2)
        plt.imshow(state)
    plt.pause(dly)
