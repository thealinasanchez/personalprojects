import math



class Movable:
    def __init__(self,x,y,dx,dy,world_width,world_height):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.world_width = world_width
        self.world_height = world_height
        self.mActive = True
        
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    def getDX(self):
        return self.dx
    
    def getDY(self):
        return self.dy
    
    def getWorldWidth(self):
        return self.world_width
    
    def getWorldHeight(self):
        return self.world_height
    
    def getActive(self):
        return self.mActive
    
    def setActive(self, active):
        self.mActive = active
        return self.mActive
    
    def move(self, dt):
        self.x = (self.x + dt * self.dx) % self.world_width
        self.y = (self.y + dt * self.dy) % self.world_height
    
    
    def hits(self, other):
        distance = math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)
        return distance <= self.getRadius() + other.getRadius()

    def accelerate(self, delta_velocity):
        raise NotImplementedError
    
    def evolve(self, dt):
        raise NotImplementedError
    
    def draw(self, surface):
        raise NotImplementedError
    
    def getRadius(self):
        raise NotImplementedError
    
        