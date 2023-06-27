import numpy as np
import matplotlib.pyplot as plt


def view(env, ts, g):
    # plt.ion()

    plt.clf()
    # if state is not None:
    #     plt.subplot(1, 2, 1)
    agents = np.array([[a.x, a.y] for a in env.agents])
    cf = np.array([[cfa.x, cfa.y] for cfa in env.counter_agents])
    plt.scatter(agents.T[0], agents.T[1], marker="o")
    plt.scatter(cf.T[0], cf.T[1], marker="o", color='red')

    pois = np.array([[p.x, p.y] for p in env.pois])
    colors = ["b", "k", "r", "c"]
    c = [colors[t] for t in env.poi_types]
    plt.scatter(pois.T[0], pois.T[1], marker="v", c=c)

    plt.xlim([-2, env.params.map_size + 2])
    plt.ylim([-2, env.params.map_size + 2])

    ag = env.agents[0]
    plt.title(f'time: {ts} G: {g:.2f} \n min:{ag.min_dist:.02f} max:{ag.max_dist:.02f} avg: {ag.avg_dist[0] / ag.avg_dist[1]:.02f}')

    plt.savefig(f'/home/anna/PycharmProjects/pymap_elites_multiobjective/examples/rollouts/plt{ts}.png')
