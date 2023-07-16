import star
import movable
import bullet
import circle
import rotatable
import rock
import polygon
import ship

import pygame
import math
import random

class Asteroids:
    def __init__(self, world_width, world_height):
        self.mWorldWidth = world_width
        self.mWorldHeight = world_height
        self.mShip = ship.Ship(self.mWorldWidth/2, self.mWorldHeight/2, self.mWorldWidth, self.mWorldHeight)
        self.mRocks = []
        self.mBullets = []
        self.mStars = []
        
        # create rocks
        for i in range(10):
            x = random.randint(0, self.mWorldWidth)
            y = random.randint(0, self.mWorldHeight)
            self.mRocks.append(rock.Rock(x,y,self.mWorldWidth,self.mWorldHeight))

        # create stars
        for i in range(20):
            x = random.randint(0, self.mWorldWidth)
            y = random.randint(0, self.mWorldHeight)
            star_a = star.Star(x,y,self.mWorldWidth,self.mWorldHeight)
            self.mStars.append(star_a)
            
        self.mObjects = self.getObjects()
            

    def getWorldWidth(self):
        return self.mWorldWidth
    
    def getWorldHeight(self):
        return self.mWorldHeight
    
    def getShip(self):
        return self.mShip
    
    def getRocks(self):
        return self.mRocks
    
    def getBullets(self):
        return self.mBullets
    
    def getStars(self):
        return self.mStars
    
    def getObjects(self):
        obj_list = []
        for rock in self.mRocks:
            obj_list.append(rock)
        obj_list.append(self.mShip)
        for bullet in self.mBullets:
            obj_list.append(bullet)
        for star in self.mStars:
            obj_list.append(star)
        return obj_list
    
    def turnShipLeft(self, delta_rotation):
        self.mShip.rotate(-delta_rotation)
    
    def turnShipRight(self, delta_rotation):
        self.mShip.rotate(delta_rotation)
    
    def accelerateShip(self, delta_velocity):
        self.mShip.accelerate(delta_velocity)
    
    def fire(self):
        if len(self.mBullets) < 3:
            bullet_a = self.mShip.fire()
            self.mBullets.append(bullet_a)
            self.mObjects.append(bullet_a)
            
    def evolveAllObjects(self, dt):
        for obj in self.mObjects:
            obj.evolve(dt)
    
    def collideShipAndBullets(self):
        for bullet in self.mBullets:
            if self.mShip.hits(bullet):
                #self.mShip.setActive(False)
                bullet.setActive(False)
    
    def collideShipAndRocks(self):
        for rock in self.mRocks:
            if self.mShip.hits(rock):
                self.mShip.setActive(False)
                rock.setActive(False)
    
    def collideRocksAndBullets(self):
        for bullet in self.mBullets:
            for rock in self.mRocks:
                if rock.hits(bullet):
                    bullet.setActive(False)
                    rock.setActive(False)
    
    def removeInactiveObjects(self):
        for obj in self.mObjects:
            if not obj.getActive():
                self.mObjects.remove(obj)
                if isinstance(obj,rock.Rock):
                    self.mRocks.remove(obj)
                elif isinstance(obj,bullet.Bullet):
                    self.mBullets.remove(obj)
    
    def evolve(self, dt):
        self.evolveAllObjects(dt)
        self.collideShipAndBullets()
        self.collideShipAndRocks()
        self.collideRocksAndBullets()
        self.removeInactiveObjects()
    
    def draw(self, surface):
        surface.fill((0,0,0))
        for obj in self.mObjects:
            if obj.getActive():
                obj.draw(surface)