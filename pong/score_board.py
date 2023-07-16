import pygame

class ScoreBoard:
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.left_score = 0
        self.right_score = 0
        self.serve_status = 1
    
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    def getWidth(self):
        return self.width
    
    def getHeight(self):
        return self.height
    
    def getLeftScore(self):
        return self.left_score
    
    def getRightScore(self):
        return self.right_score
        
    def getServeStatus(self):
        return self.serve_status
        
    def isGameOver(self):
        if self.serve_status in [3,4]:
            return True
        else:
            return False
    
    def scoreLeft(self):
        if not self.isGameOver():
            self.left_score += 1
            if self.left_score == 9:
                self.serve_status = 3
                
    def scoreRight(self):
        if not self.isGameOver():
            self.right_score += 1
            if self.right_score == 9:
                self.serve_status = 4
    
    def swapServe(self):
        if not self.isGameOver():
            if self.serve_status == 1:
                self.serve_status = 2
            elif self.serve_status == 2:
                self.serve_status = 1
    
    def draw(self, surface):
        font = pygame.font.SysFont(None, 30)
        text_left = font.render(str(self.left_score), True, (255, 255, 255))
        text_right = font.render(str(self.right_score), True, (255, 255, 255))
        rect_left = text_left.get_rect()
        rect_right = text_right.get_rect()
        rect_left.center = (self.x + self.width//4, self.y + self.height//2)
        rect_right.center = (self.x + 3*self.width//4, self.y + self.height//2)
        pygame.draw.rect(surface, (0, 0, 0), (self.x, self.y, self.width, self.height), 2)
        pygame.draw.line(surface, (0, 0, 0), (self.x + self.width//2, self.y), (self.x + self.width//2, self.y + self.height), 2)
        surface.blit(text_left, rect_left)
        surface.blit(text_right, rect_right)
    
    
    
    
    
        
    

    
    

    
   
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
        