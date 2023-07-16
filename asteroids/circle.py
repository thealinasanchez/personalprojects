import rotatable
import pygame



class Circle(rotatable.Rotatable):
    def __init__(self,x,y,dx,dy,rotation,radius,world_width,world_height):
        super().__init__(x,y,dx,dy,rotation,world_width,world_height)
        self.mRadius = radius
        self.mColor = (255,255,255)
        
    def getRadius(self):
        return self.mRadius
    
    def getColor(self):
        return self.mColor
    
    def setRadius(self, radius):
        if radius >= 1:
            self.mRadius = radius
        else:
            pass
        return self.mRadius
    
    def setColor(self, color):
        self.mColor = color
        return self.mColor
    
    def draw(self, surface):
        pygame.draw.circle(surface, self.getColor(), (int(self.getX()), int(self.getY())), int(self.getRadius()))