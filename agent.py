from math import sqrt

class agent:

    def __init__(self,params):
        self.params=params
        self.x,self.y=params.agent_init()
        self.x_,self.y_ = self.x,self.y # to reset values
        self.top_speed=params.speed
        self.battery=params.battery
    
    def reset(self):
        self.battery=self.params.battery
        self.x,self.y = self.x_,self.y_

    def move(self,x,y,speed):

        r = sqrt((x-self.x)**2.0 +(y-self.y))
        if r>1:
    
            dx=(x-self.x)/r
            dy=(y-self.y)/r
            self.x+=dx*self.top_speed*speed
            self.y+=dy*self.top_speed*speed
            self.battery-=speed*speed
    
    def interact(self,effort,speed):
        self.battery-=effort*speed

    

