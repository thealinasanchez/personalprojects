import pygame


class Paddle:
    def __init__(self, x, y, width, height, speed, min_y, max_y):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.min_y = min_y
        self.max_y = max_y
        
    def getRightX(self):
        right_side = self.x + self.width
        return right_side
    
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    def getWidth(self):
        return self.width
    
    def getHeight(self):
        return self.height
    
    def getSpeed(self):
        return self.speed
    
    def getMaxY(self):
        return self.max_y
    
    def getMinY(self):
        return self.min_y
    
    def getBottomY(self):
        bottom_y = self.y + self.height
        return bottom_y
    
    def setPosition(self, y):
        if y < self.min_y or y + self.height > self.max_y:
            pass
        else:
            self.y = y
            
    def moveUp(self, dt):
        new_y = self.y - self.speed * dt
        if new_y < self.min_y:
            self.y = self.min_y
        else:
            self.y = new_y
            
    def moveDown(self, dt):
        new_y = self.y + self.speed * dt
        if new_y + self.height > self.max_y:
            self.y = self.max_y - self.height
        else:
            self.y = new_y
            
    def draw(self, surface):
        pygame.draw.rect(surface, (255,255,255), (self.x, self.y, self.width, self.height))
    
    
    
    
        
        
        
        