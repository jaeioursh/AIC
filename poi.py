from math import tanh

class poi:
    def __init__(self,x,y,work,params):
        self.x=x
        self.y=y
        self.type_val=1.0
        
        self.work=work #work done
        self.work_=work
        self.complete=self.fn(work,1) #how completed it is based on work done
        
        self.params=params
        self.dvec=[0]*params.n_agents

    def fn(self,work,p):
        return work*p

    def reset(self):
        self.work=self.work_
        self.complete=self.fn(self.work,1)
        self.dvec=[0]*self.params.n_agents


    def observe(self,agent_idx,effort,speed):
        self.work+=speed
        self.new_complete=self.fn(self.work,effort)
        self.dvec[agent_idx]+=self.new_complete-self.complete
        self.complete=self.new_complete

class linear_poi(poi):
    def __init__(self, x, y, params):
        super().__init__(x, y, 0.0, params)
        self.type_val=0.1
        
    def fn(self,work,p):
        return min(work*p*self.type_val,1)

class tanh_poi(poi):
    def __init__(self, x, y, params):
        super().__init__(x, y, 0.0, params)
        self.type_val=0.5
    def fn(self,work,p):
        return tanh(work*p*self.type_val)
    
    


