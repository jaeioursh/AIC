import numpy as np
import matplotlib.pyplot as plt

plt.ion()


def view(env, state, ts):
    plt.clf()
    plt.subplot(1, 2, 1)
    agents = np.array([[a.x, a.y] for a in env.agents])
    plt.scatter(agents.T[0], agents.T[1], marker="o")

    pois = np.array([[p.x, p.y, p.type_val] for p in env.pois])
    plt.scatter(pois.T[0], pois.T[1], marker="v", c=pois.T[2])

    plt.xlim([-2, env.params.map_size + 2])
    plt.ylim([-2, env.params.map_size + 2])

    plt.title(f'time: {ts}')
    plt.subplot(1, 2, 2)
    plt.imshow(state)
    plt.pause(0.1)
