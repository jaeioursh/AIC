from math import atan2, pi, sqrt
import numpy as np
from AIC.counterAgent import CounterAgent


def pois2type(pois):
    lst = []
    for poi in pois:
        if not poi in lst:
            lst.append(poi)
    types = []

    for poi in pois:
        for i in range(len(lst)):
            if poi == lst[i]:
                types.append(i)

    return np.array(types,dtype=np.int32)


class aic:
    def __init__(self, params):
        self.params = params
        self.poi_types = pois2type(params.poi_class)
        self.n_poi_types = max(self.poi_types) + 1

        self.pois = []
        # Creates POIs and puts them in a list
        for pos, poi_class in zip(params.poi_pos, params.poi_class):
            self.pois.append(poi_class(pos[0], pos[1], params))

        self.agents = []
        # Creates agents and puts them in a list
        for pos, agent_class in zip(params.agent_pos, params.agent_class):
            self.agents.append(agent_class(pos[0], pos[1], params))

        self.n_counter = params.counter
        self.counter_agents = [CounterAgent(params) for _ in range(self.n_counter)]

    def reset(self):
        for p in self.pois:
            p.reset()
        for a in self.agents:
            a.reset()

    def G(self):
        g = np.zeros(self.n_poi_types)
        for idx, poi in zip(self.poi_types, self.pois):
            g[idx] += poi.complete
        return g

    def D(self):
        d = np.zeros( (self.params.n_agents,self.n_poi_types))
        for idx, poi in zip(self.poi_types, self.pois):
            for i in range(self.params.n_agents):
                d[i][idx] += poi.dvec[i]
        return d

    # bins pois and agents for the sensors and the actions
    def binning(self):
        # TODO: Add check for sensor range
        # One set of bins per agent
        # Each set of bins has n sensors for each poi type, +1 for agents
        bins = [[[] for _ in range((self.n_poi_types + 1) * self.params.n_sensors)] for _ in
                range(self.params.n_agents)]
        for i in range(self.params.n_agents):
            agent = self.agents[i]
            X = agent.x
            Y = agent.y
            for type, poi in zip(self.poi_types, self.pois):
                x = poi.x
                y = poi.y
                # Dist between agent and POI
                r = sqrt((x - X) ** 2 + (y - Y) ** 2)
                # TODO:This math will need to be explained to me please
                idx = int(0.99999 * (atan2(y - Y, x - X) + pi) / (pi * 2.0) * self.params.n_sensors)
                idx += type * self.params.n_sensors
                # Add the POI and dist to agent to the appropriate bin
                bins[i][idx].append([poi, r])

            # Bin the agents that are within sensor range
            # If we want to speed this up, we can do the calculation once and save for both agents i & j
            for j in range(self.params.n_agents):
                if i != j:
                    ag = self.agents[j]
                    x = ag.x
                    y = ag.y
                    # Distance between agents
                    r = sqrt((x - X) ** 2 + (y - Y) ** 2)
                    idx = int(0.99999 * (atan2(y - Y, x - X) + pi) / (pi * 2.0) * self.params.n_sensors)
                    idx += self.n_poi_types * self.params.n_sensors
                    bins[i][idx].append([ag, r])

            # Bin the counter-agents that are within sensor range -- goes in the same bins as the agents
            for k in range(self.n_counter):
                ag = self.counter_agents[k]
                x = ag.x
                y = ag.y
                # Distance between agents
                r = sqrt((x - X) ** 2 + (y - Y) ** 2)
                idx = int(0.99999 * (atan2(y - Y, x - X) + pi) / (pi * 2.0) * self.params.n_sensors)
                idx += self.n_poi_types * self.params.n_sensors
                bins[i][idx].append([ag, r])
                if r < agent.min_dist:
                    agent.min_dist = r
                if r > agent.max_dist:
                    agent.max_dist = r
                agent.avg_dist[0] += r
                agent.avg_dist[1] += 1
        return bins

    def state(self):
        # Gets the inputs from the sensors for each agent
        bins = self.binning()
        self.bins = bins
        S = []
        for i in range(self.params.n_agents):
            bin = bins[i]
            # Final n sensors are for agents
            poi_bin = bin[:-self.params.n_sensors]
            agent_bin = bin[-self.params.n_sensors:]
            # Sum of completeness state for POIs in each sensor bin
            state_poi_complete = [sum([poi.complete for poi, r in pois]) if len(pois) > 0 else 0 for pois in poi_bin]
            state_poi_dist = [sum([1 / (r + 1) for poi, r in pois]) if len(pois) > 0 else 0 for pois in poi_bin]
            # Distance density for agents in each sensor bin
            state_agent_dist = [sum([1 / (r + 1) for agent, r in agents]) if len(agents) > 0 else 0 for agents in
                                agent_bin]
            # Battery percentage for agent
            state_battery = [self.agents[i].battery / self.params.battery]
            S.append(state_poi_complete + state_poi_dist + state_agent_dist + state_battery)
        return np.array(S)

    def state_size(self):
        # POI portion of the state has one bin per poi type for each sensor
        # Double it for distance and completeness values
        poi_st = (self.n_poi_types * self.params.n_sensors * 2)
        ag_st = self.params.n_sensors
        return poi_st + ag_st + 1  # Add one for the battery value

    def action(self, A):
        # Get the POIs and agents in sensor range for all agents
        bins = self.bins
        for c_ag in self.counter_agents:
            c_ag.move()

        for i in range(self.params.n_agents):
            if self.agents[i].battery > 0:
                # For each agent
                bin = bins[i]
                agent = self.agents[i]
                # Get the action
                a = A[i]
                # Determine which bin is being targeted
                idx = np.argmax(a[:-3])
                # If there is something in that bin, move toward it
                # If not, it is a null action
                if len(bin[idx]) > 0:
                    # Determines behaviors
                    movement = a[-3]
                    effort = a[-2]
                    speed = a[-1]

                    # Move toward chosen destination
                    poi, r = min(bin[idx], key=lambda x: x[1])
                    agent.move(poi.x, poi.y, movement)

                    # If within range, complete observations
                    if r < self.params.interact_range:
                        agent.interact(effort, speed)
                        poi.observe(i, effort, speed)

    def action_size(self):
        # Can choose any POI type in any sensor region
        poi_act = self.n_poi_types * self.params.n_sensors
        # Behavior variables are movement, effort, speed
        bh_vars = 3
        return poi_act + bh_vars
