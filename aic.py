from math import atan2,pi,sqrt
import numpy as np

def pois2type(pois):
    lst=[]
    for poi in pois:
        if not poi in lst:
            lst.append(poi)
    types=[]
    
    for poi in pois:
        for i in range(len(lst)):
            if poi==lst[i]:
                types.append(i)

    return types
        


class aic:
    def __init__(self,params):
        self.params=params
        self.poi_types=pois2type(params.poi_class)
        self.n_poi_types=max(self.poi_types)+1
        
        self.pois=[]
        for pos,poi_class in zip(params.poi_pos,params.poi_class):
            self.pois.append(poi_class(pos[0],pos[1],params))

        self.agents=[]
        for pos,agent_class in zip(params.agent_pos,params.agent_class):
            self.agents.append(agent_class(pos[0],pos[1],params))

    def reset(self):
        for p in self.pois:
            p.reset()
        for a in self.agents:
            a.reset()

    def G(self):
        g=[0.0]*len(self.poi_types)
        for idx,poi in zip(self.poi_types,self.pois):
            g[idx]+=poi.complete
        return g

    def D(self):
        d=[[0.0]*len(self.poi_types) for _ in range(self.params.n_agents)]
        for idx,poi in zip(self.poi_types,self.pois):
            for i in range(self.params.n_agents):
                d[i][idx]+=poi.dvec[i]
        return d
    
    #bins pois and agents for the sensors and the actions
    def binning(self):
        #          n sensors for each poi type, +1 for agents
        bins=[[[] for _ in range((self.n_poi_types+1)*self.params.n_sensors) ] for _ in range(self.params.n_agents)]
        for i in range(self.params.n_agents):
            agent=self.agents[i]
            X=agent.x
            Y=agent.y
            for type,poi in zip(self.poi_types,self.pois):
                x=poi.x
                y=poi.y
                r=sqrt((x-X)**2+(y-Y)**2)
                idx=int(0.99999*(atan2(y-Y,x-X)+pi)/(pi*2.0)*self.params.n_sensors)
                idx+=type*self.params.n_sensors
                bins[i][idx].append([poi,r])

            for j in range(self.params.n_agents):
                if i!=j:
                    agent=self.agents[j]
                    x=agent.x
                    y=agent.y
                    r=sqrt((x-X)**2+(y-Y)**2)
                    idx=int(0.99999*(atan2(y-Y,x-X)+pi)/(pi*2.0)*self.params.n_sensors)
                    idx+=self.n_poi_types*self.params.n_sensors
                    bins[i][idx].append([agent,r])
        return bins

    def state(self):
        bins=self.binning()
        S=[]
        for i in range(self.params.n_agents):
            bin=bins[i]
            poi_bin=bin[:-self.params.n_sensors]
            agent_bin=bin[-self.params.n_sensors:]
            state_poi_complete=[sum([poi.complete for poi,r in pois]) if len(pois)>0 else 0 for pois in poi_bin]
            state_poi_dist=[sum([1/(r+1) for poi,r in pois]) if len(pois)>0 else 0 for pois in poi_bin]
            state_agent_dist=[sum([1/(r+1) for agent,r in agents]) if len(agents)>0 else 0 for agents in agent_bin]
            state_battery=[self.agents[i].battery/self.params.battery]
            S.append(state_poi_complete+state_poi_dist+state_agent_dist+state_battery)
        return np.array(S)

    def action(self,A):
        bins=self.binning()    
        for i in range(self.params.n_agents):
            bin=bins[i]
            agent=self.agents[i]
            a=A[i]
            idx=np.argmax(a[:-3])
            if len(bin[idx])>0:
                
                movement=a[-3]
                effort=a[-2]
                speed=a[-1]

                poi,r=min(bin[idx],key=lambda x:x[1])
                agent.move(poi.x,poi.y,movement)

                if r<self.params.interact_range:
                    agent.interact(effort,speed)
                    poi.observe(i,effort,speed)
