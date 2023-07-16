import rotatable
import movable

import pygame
import math

class Polygon(rotatable.Rotatable):
    def __init__(self,x,y,dx,dy,rotation,world_width,world_height):
        super().__init__(x,y,dx,dy,rotation,world_width,world_height)
        self.mOriginalPolygon = []
        self.mColor = (255,255,255)
    
    def getPolygon(self):
        return self.mOriginalPolygon
    
    def getColor(self):
        return self.mColor
    
    def setPolygon(self, point_list):
        self.mOriginalPolygon = []
        for point in point_list:
            if isinstance(point,tuple):
                self.mOriginalPolygon.append(point)
            else:
                pass
        
    def setColor(self, color):
        if isinstance(color, tuple) and len(color) == 3:
            self.mColor = color
        else:
            pass
    
    def draw(self, surface):
        polygon_points = self.rotateAndTranslatePointList(self.getPolygon())
        pygame.draw.polygon(surface, self.getColor(), polygon_points)
    
    def getRadius(self):
        num_points = len(self.mOriginalPolygon)
        if num_points == 0:
            return 0
        else:
            sum_distances = 0
            for point in self.mOriginalPolygon:
                distance = math.sqrt(point[0]**2 + point[1]**2)
                sum_distances += distance
            return sum_distances / num_points
                