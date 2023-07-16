import circle



class Bullet(circle.Circle):
    def __init__(self,x,y,dx,dy,rotation,world_width,world_height):
        super().__init__(x,y,dx,dy,rotation,3,world_width,world_height)
        self.mAge = 0.0
        self.accelerate(100.0)
        self.move(0.1)
    
    def getAge(self):
        return self.mAge
    
    def setAge(self,age):
        self.mAge = age
        return self.mAge
    
    def evolve(self,dt):
        self.move(dt)
        self.mAge += dt
        if self.mAge > 6.0:
            self.setActive(False)