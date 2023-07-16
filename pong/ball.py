import random
import pygame

class Ball:
    def __init__(self,size,min_x,max_x,min_y,max_y,left_paddle_x,right_paddle_x):
        self.size = size
        self.min_x = min_x
        self.max_x = max_x
        self.min_y = min_y
        self.max_y = max_y
        self.mDX = 0
        self.mDY = 0
        self.left_paddle_x = left_paddle_x
        self.right_paddle_x = right_paddle_x

        self.x = min_x
        self.y = min_y
        self.left_paddle_min_y = min_y
        self.left_paddle_max_y = max_y
        self.right_paddle_min_y = min_y
        self.right_paddle_max_y = max_y
        
        
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    def getSize(self):
        return self.size
    
    def getDX(self):
        return self.mDX
    
    def getDY(self):
        return self.mDY
    
    def getMinX(self):
        return self.min_x
    
    def getMaxX(self):
        return self.max_x
    
    def getMinY(self):
        return self.min_y
    
    def getMaxY(self):
        return self.max_y
    
    def getLeftPaddleX(self):
        return self.left_paddle_x
    
    def getLeftPaddleMinY(self):
        return self.left_paddle_min_y
    
    def getLeftPaddleMaxY(self):
        return self.left_paddle_max_y
    
    def getRightPaddleX(self):
        return self.right_paddle_x
    
    def getRightPaddleMinY(self):
        return self.right_paddle_min_y
    
    def getRightPaddleMaxY(self):
        return self.right_paddle_max_y
        
    def setPosition(self,x,y):
        if x >= self.min_x and y >= self.min_y:
            if x <= (self.max_x - self.size) and y <= (self.max_y - self.size):
                self.x = x
                self.y = y
            else:
                pass
        
    def setSpeed(self,dx, dy):
        self.mDX = dx
        self.mDY = dy
    
    def setLeftPaddleY(self,paddle_min_y, paddle_max_y):
        if paddle_min_y >= self.min_y and paddle_max_y <= self.max_y:
            if paddle_min_y < paddle_max_y:
                self.left_paddle_min_y = paddle_min_y
                self.left_paddle_max_y = paddle_max_y
        else:
            pass
        
    def setRightPaddleY (self,paddle_min_y,paddle_max_y):
        if paddle_min_y >= self.min_y and paddle_max_y <= self.max_y:
            if paddle_min_y < paddle_max_y:
                self.right_paddle_min_y = paddle_min_y
                self.right_paddle_max_y = paddle_max_y
        else:
            pass
    
    def checkTop(self, new_y):
        if new_y <= self.min_y:
            self.mDY *= -1
            new_y = self.min_y + (self.min_y - new_y)
            return new_y
        else:
            return new_y
            
    
    def checkBottom(self,new_y):
        if new_y + self.size >= self.max_y:
            self.mDY *= -1
            new_position = self.size + new_y
            distance = new_position - self.max_y
            new_y = self.max_y - distance - self.size
            return new_y
        else:
            return new_y
    
    def checkLeft(self,new_x):
        if new_x <= self.min_x:
            self.mDX = 0
            self.mDY = 0
            new_x = self.min_x
            return new_x
        else:
            return new_x
    
    def checkRight(self,new_x):
        if new_x + self.size >= self.max_x:
            self.mDX = 0
            self.mDY = 0
            new_x = self.max_x - self.size
            return new_x
        return new_x
            
    
    def checkLeftPaddle(self,new_x,new_y):
        mid_y = (new_y + self.y)/2
        if mid_y >= self.left_paddle_min_y and mid_y <= self.left_paddle_max_y and new_x <= self.left_paddle_x and self.x >= self.left_paddle_x:
            self.mDX *= -1
            delta_x2 = self.left_paddle_x - new_x
            new_x = self.left_paddle_x + delta_x2
            return new_x
        return new_x
    
    def checkRightPaddle(self,new_x,new_y):
        mid_y = (new_y + self.y)/2
        distance = (self.size + new_x) - self.right_paddle_x
        if mid_y >= self.right_paddle_min_y and mid_y <= self.right_paddle_max_y and (new_x + self.size) >= self.right_paddle_x and (self.x + self.size) <= self.right_paddle_x:
            self.mDX *= -1
            new_x = self.right_paddle_x - distance - self.size
            return new_x
        return new_x

    def move(self,dt):
        # local variables
        new_x = self.x + self.mDX * dt
        new_y = self.y + self.mDY * dt
        
        # check boundaries
        new_y = self.checkTop(new_y)
        new_y = self.checkBottom(new_y)
        new_x = self.checkLeft(new_x)
        new_x = self.checkRight(new_x)
        new_x = self.checkLeftPaddle(new_x, new_y)
        new_x = self.checkRightPaddle(new_x, new_y)
        
        # set new_x and new_y to x and y
        self.x = new_x
        self.y = new_y
        
    def serveLeft(self, x, min_y, max_y, min_dx, max_dx, min_dy, max_dy):
        self.x = x
        self.y = random.uniform(min_y, max_y)
        self.mDX = random.uniform(min_dx, max_dx)
        self.mDY = random.uniform(min_dy, max_dy)
        
    def serveRight(self, x, min_y, max_y, min_dx, max_dx, min_dy, max_dy):
        self.x = x
        self.y = random.uniform(min_y, max_y)
        self.mDX = random.uniform(-min_dx, -max_dx)
        self.mDY = random.uniform(min_dy, max_dy)
        
    def draw(self, surface):
        pygame.draw.circle(surface, (255, 255, 255), (self.x, self.y), int(self.size/2))