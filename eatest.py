from parameter import parameter
from aic import aic
import pyximport
import tqdm
import numpy as np
from view import view
pyximport.install()
from ccea import *

def display(data,env,n_steps):
    assignBestCceaPolicies(data)
    env.reset()
    pols=data["Agent Policies"]
    for j in range(n_steps):
        S=env.state()
        A=[]
        for s,pol in zip(S,pols):
            A.append((pol.get_action(s)+1)/2)
        env.action(A)
        g=sum(env.G())
        view(env,j,g)
def test():
    p=parameter()
    env=aic(p)
    data=dict()
    data['Number of Agents']=p.n_agents
    data['Trains per Episode']=32
    initCcea(input_shape=env.state_size(), num_outputs=env.action_size(), num_units=20)(data)

    gens=tqdm.trange(20)
    for generation in gens:
        G=[]
        for i in range(data['Trains per Episode']):
            data["World Index"]=i
            assignCceaPolicies(data)
            env.reset()
            pols=data["Agent Policies"]
            for j in range(p.time_steps):
                S=env.state()
                A=[]
                for s,pol in zip(S,pols):
                    A.append((pol.get_action(s)+1)/2)
                env.action(A)
            g=sum(env.G())
            d=np.sum(env.D(),axis=1)
            data["Agent Rewards"]=[g]*p.n_agents
            data["Agent Rewards"]=d

            rewardCceaPolicies(data)
            G.append(g)
        evolveCceaPolicies(data)
        if generation%250==249:
            display(data,env,p.time_steps)
        gens.set_description("G:" +str(max(G)))

if __name__ == "__main__":
    test()