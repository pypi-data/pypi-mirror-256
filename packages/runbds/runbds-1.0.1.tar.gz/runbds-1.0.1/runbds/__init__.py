import numpy as np
import math

class Bdarg:
    def __init__(self,arg:list):
        self.arg=arg
    
    def __getitem__(self,i:int):
        return self.arg[i]
    
    def __setitem__(self, i:int, v):
        self.data[i] = v
        
    def __len__(self):
        return len(self.arg)

class Bdsarg:
    def __init__(self,arg:list[Bdarg]):
        self.arg=arg
    
    def __getitem__(self,i:int):
        return self.arg[i]
    
    def __setitem__(self, i:int, v):
        self.data[i] = v
        
    def __len__(self):
        return len(self.arg)

class Body:
    def __init__(self, weight, pos0, v0):
        '''
        weight:The weight of the body
        pos0:the position of the body,like[2,-4,0]
        v0:the velocity of the body,like[3,-1,7]
        '''
        self.m = weight
        self.pos = pos0
        self.v = v0

    def update(self, others, delta_t)->None:
        

        ft = np.array([0, 0, 0])
        for bodyi in others:
            
            ft_dir = (bodyi.pos - self.pos) / np.linalg.norm(bodyi.pos - self.pos)
            
            ft = ft + (bodyi.m * self.m / sum(np.square(bodyi.pos - self.pos))) * ft_dir
        at = ft / self.m
        
        self.pos = self.pos + self.v * delta_t + 0.5 * at * (delta_t ** 2)
        
        self.v = self.v + at * delta_t
        
class Bodies:
    def __init__(self,bn:int,arg:Bdsarg,tms=0.1):
        self.stars=[Body(arg[i][0],arg[i][1],arg[i][2]) for i in range(0,bn)]
        self.TIMESTEP = tms
    
    def run(self,t:int)->None:
        if t<self.TIMESTEP:raise RuntimeError("time error!")
        for _ in np.arange(0,t/self.TIMESTEP):
            for body in self.stars:
                starscopy = self.stars[:]
                starscopy.remove(body)
                body.update(starscopy,self.TIMESTEP)
    
    def getpos(self)->list:
        poses=[]
        for star in self.stars:
            poses.append(star.pos)   
        return poses
            
                
class BodiesSR:
    def __init__(self,bn:int,arg:Bdsarg,tms=0.1):
        args=[]
        for v in arg:
            args.append((v[0]*math.sqrt(3),
                       np.array(v[1]),
                       np.array(v[2])))
        self.bds=Bodies(bn,arg,tms)
        
    def run(self,t:int)->None:
        self.bds.run(t)
    
    def getpos(self)->list:
        return self.bds.getpos()
    
  