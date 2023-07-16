import polygon
import math
import random

class Rock(polygon.Polygon):
    def __init__(self,x,y,world_width,world_height):
        dx = 0
        dy = 0
        rotation = random.uniform(0, 359.9)
        super().__init__(x,y,dx,dy,rotation, world_width, world_height)
        shape = self.createRandomPolygon(random.uniform(10,20), 5)
        self.setPolygon(shape)
        self.setColor((128,128,128))
        self.setSpinRate(random.uniform(-90,90))
        self.accelerate(random.uniform(10,20))
    
    def createRandomPolygon(self, r, num_points):
        points = []
        angle = 0
        angle_diff = 360/num_points
        for i in range(num_points):
            dx = math.cos(math.radians(angle))
            dy = math.sin(math.radians(angle))
            d = random.uniform(.7, 1.3) * r
            points.append((d*dx, d*dy))
            angle += angle_diff
        return points
    
    def getSpinRate(self):
        return self.mSpinRate
    
    def setSpinRate(self, spin_rate):
        self.mSpinRate = spin_rate
    
    def evolve(self, dt):
        self.rotate(self.getSpinRate() * dt)
        self.move(dt)