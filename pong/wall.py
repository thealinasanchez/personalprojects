import pygame

class Wall:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height

    def getRightX(self):
        right_x = self.x + self.width
        return right_x

    def getBottomY(self):
        bottom_y = self.y + self.height
        return bottom_y

    def draw(self, surface):
        rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(surface, (255,255,255), rect)    
    
    
    
    
    