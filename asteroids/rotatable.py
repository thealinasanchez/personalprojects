import movable
import math

class Rotatable(movable.Movable):
    
    def __init__(self, x, y, dx, dy, rotation, world_width, world_height):
        super().__init__(x, y, dx, dy, world_width, world_height)
        self.rotation = rotation
    
    def getRotation(self):
        return self.rotation
    
    def rotate(self, delta_rotation):
        self.rotation = (self.rotation + delta_rotation) % 360
        if self.rotation < 0:
            self.rotation += 360
    
    def splitDeltaVIntoXAndY(self, rotation, delta_velocity):
        xc = math.cos(math.radians(rotation)) * delta_velocity #x component
        yc = math.sin(math.radians(rotation)) * delta_velocity #y component
        return xc, yc
    
    def accelerate(self, delta_velocity):
        '''
        if self.rotation == 0:
            self.dx += 1 #cosine(0)
            self.dy += 0 #sine(0)
        elif self.rotation == 90:
            self.dx += 0 #cosine(90)
            self.dy += 1 #sine(90)
        '''
        # ---- generalized ----
        xc, yc = self.splitDeltaVIntoXAndY(self.rotation, delta_velocity)
        self.dx += xc
        self.dy += yc
        
    
    def rotatePoint(self,x,y):
        angle = math.atan2(y,x)
        new_angle = math.degrees(angle) + self.rotation
        d = math.sqrt(x**2 + y**2)
        newx, newy = self.splitDeltaVIntoXAndY(new_angle, d)
        return newx,newy
    
    def translatePoint(self,x,y):
        newx = self.x + x
        newy = self.y + y
        return newx,newy
    
    def rotateAndTranslatePoint(self,x,y):
        newx,newy = self.rotatePoint(x,y)
        newx,newy = self.translatePoint(newx,newy)
        return newx, newy
    
    def rotateAndTranslatePointList(self,point_list):
        new_list = []
        for point in point_list:
            x = point[0]
            y = point[1]
            new_point = self.rotateAndTranslatePoint(x,y)
            new_list.append(new_point)
        return new_list