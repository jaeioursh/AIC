from parameter import parameter
from aic import aic
import pyximport
import tqdm
pyximport.install()
from ccea import *


def test():
    p=parameter()
    env=aic(p)

    n_steps=50

    data=dict()
    data['Number of Agents']=p.n_agents
    data['Trains per Episode']=32
    initCcea(input_shape=env.state_size(), num_outputs=env.action_size(), num_units=20)(data)

    gens=tqdm.trange(100)
    for generation in gens:
        G=[]
        for i in range(data['Trains per Episode']):
            data["World Index"]=i
            assignCceaPolicies(data)
            env.reset()
            pols=data["Agent Policies"]
            for j in range(n_steps):
                S=env.state()
                A=[]
                for s,pol in zip(S,pols):
                    A.append(pol.get_action(s))
                env.action(A)
            g=sum(env.G())
            
            data["Agent Rewards"]=[g]*p.n_agents
            
            rewardCceaPolicies(data)
            G.append(g)
        evolveCceaPolicies(data)
        gens.set_description("G:" +str(max(G)))

if __name__ == "__main__":
    test()