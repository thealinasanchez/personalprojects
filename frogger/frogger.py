import pygame
import froggerlib
import random

class Frogger:
    
    def __init__(self, window_width, window_height, num_rows, num_cols, cell_size):
        self.window_width = window_width
        self.window_height = window_height
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size = cell_size
        self.game_over = False
        self.game_win = False
        self.num_roads = (self.num_rows - 3)//2
        self.num_waters = (self.num_rows - 3 - self.num_roads)
        self.padding = .10

        #Making the frog
        x = (num_cols //2 + self.padding) * cell_size
        y = (num_rows - 1 + self.padding) * cell_size
        w = cell_size * (1-2*self.padding)
        h = cell_size * (1-2*self.padding)
        dx = x
        dy = y
        s = 6
        hg = self.cell_size
        vg = self.cell_size
        self.frog = froggerlib.Frog(x,y, w, h, dx, dy, s, hg, vg)

        #Making multiple roads
        self.roads = []
        for i in range(self.num_roads):
            x = 0
            y = (self.num_rows - 2 - i) * self.cell_size
            w = self.window_width
            h = self.cell_size
            self.roads.append(froggerlib.Road(x,y,w,h))

        #Making multiple waters
        self.waters = []
        for i in range(self.num_waters):
            x = 0
            y = (self.num_rows - 2 -self.num_roads - 1 - i) * self.cell_size
            w = self.window_width
            h = self.cell_size
            self.waters.append(froggerlib.Water(x,y,w,h))

        #Making multiple cars going to right
        self.cars = []
        for i in range(self.num_roads):
            x = random.randrange(0, self.window_width)
            y = (self.num_rows - 2 - i + self.padding/2) * self.cell_size
            dx = self.window_width + self.cell_size + random.randrange(self.cell_size, self.window_width)
            dy = y
            w = self.cell_size * 2
            h = self.cell_size * (1-1*self.padding)
            s = 5
            self.cars.append(froggerlib.Car(x,y,w,h,dx, dy, s))

        #Making multiple racecars going to right
        self.racecars = []
        for i in range(self.num_roads):
            x = random.randrange(0, self.window_width)
            y = (self.num_rows - 2 - i + self.padding/2) * self.cell_size
            dx = self.window_width + self.cell_size + random.randrange(self.cell_size, self.window_width)
            dy = y
            w = self.cell_size * 2
            h = self.cell_size * (1-1*self.padding)
            mins = 2
            maxs = 8
            self.racecars.append(froggerlib.RaceCar(x, y, w, h, dx, dy, mins, maxs))

        #Making multiple dozers going to left
        self.dozers = []
        for i in range(self.num_roads):
            x = self.window_width + self.cell_size + random.randrange(self.cell_size, self.window_width)
            y = (self.num_rows - 2 - i + self.padding/2) * self.cell_size
            dx = -self.cell_size * 4
            dy = y
            w = self.cell_size * 3
            h = self.cell_size * (1-1 * self.padding)
            s = 2
            self.dozers.append(froggerlib.Dozer(x, y, w, h, dx, dy, s))
        
        #Making multiple logs go right
        self.logs_right = []
        for i in range(self.num_waters):
            x = random.randrange(0, self.window_width)
            y = (self.num_rows - 2 - self.num_roads - 1 - i + self.padding/2) * self.cell_size
            dx = self.window_width + self.cell_size + random.randrange(self.cell_size)
            dy = y
            w = self.cell_size * 2
            h = self.cell_size * (1-1*self.padding)
            s = 3
            self.logs_right.append(froggerlib.Log(x,y,w,h,dx,dy,s))

        #Making multiple turtles go left
        self.turtles = []
        for i in range(self.num_waters):
            x = self.window_width + self.cell_size + random.randrange(self.cell_size, self.window_width)
            y = (self.num_rows - 2 - self.num_roads - 1 - i + self.padding/2) * self.cell_size
            dx = -self.cell_size * 4
            dy = y
            w = self.cell_size
            h = self.cell_size * (1-1*self.padding)
            s = 3
            self.turtles.append(froggerlib.Turtle(x,y,w,h,dx,dy,s))

        #Making the beginning stage
        x = 0
        y = (self.num_rows - 1)* self.cell_size
        w = self.window_width
        h = self.cell_size
        self.stage1 = froggerlib.Stage(x, y, w, h)

        #Making the middle stage
        x = 0
        y = (self.num_rows - 2 - self.num_roads) * self.cell_size
        w = self.window_width
        h = self.cell_size
        self.stage2 = froggerlib.Stage(x, y, w, h)

        #Making home1
        x = self.cell_size * 3
        y = 0
        w = self.cell_size * 2
        h = self.cell_size
        self.home1 = froggerlib.Home(x,y,w,h)

        #Making home2
        x = self.cell_size * 8
        y = 0
        w = self.cell_size * 2
        h = self.cell_size
        self.home2 = froggerlib.Home(x,y,w,h)

        #Making home3
        x = self.cell_size * 13
        y = 0
        w = self.cell_size * 2
        h = self.cell_size
        self.home3 = froggerlib.Home(x,y,w,h)

        #Making grass1
        x = 0
        y = 0
        w = self.cell_size * 3
        h = self.cell_size
        self.grass1 = froggerlib.Grass(x, y, w, h)

        #Making grass2
        x = self.cell_size * 5
        y = 0
        w = self.cell_size * 3
        h = self.cell_size
        self.grass2 = froggerlib.Grass(x,y,w,h)

        #Making grass3
        x = self.cell_size * 10
        y = 0
        w = self.cell_size * 3
        h = self.cell_size
        self.grass3 = froggerlib.Grass(x,y,w,h)

        
        


    #Player keys
    def up(self):
        self.frog.up()
    
    def down(self):
        self.frog.down()

    def left(self):
        self.frog.left()

    def right(self):
        self.frog.right()

    #Where the logic goes
    def evolve(self, dt): #dt stands for delta time. Used for changing the time
        if self.game_over:
            return 
        
        if self.game_win:
            return

        self.frog.move()
        if self.frog.outOfBounds(self.window_width, self.window_height):
            self.game_over = True

        if self.grass1.hits(self.frog):
            self.game_over = True
        
        if self.grass2.hits(self.frog):
            self.game_over = True

        if self.grass3.hits(self.frog):
            self.game_over = True


        if self.frog.overlapWithLocatable(self.home1):
            self.game_win = True

        if self.frog.overlapWithLocatable(self.home2):
            self.game_win = True

        if self.frog.overlapWithLocatable(self.home3):
            self.game_win = True

        for water in self.waters:
            if water.hits(self.frog):
                self.game_over = True

        for car in self.cars:
            car.move()
            if car.atDesiredLocation():
                car.setX(-car.getWidth()-random.randrange(car.getWidth()))
            if car.hits(self.frog):
                self.game_over = True

        for racecar in self.racecars:
            racecar.move()
            if racecar.atDesiredLocation():
                racecar.setX(-car.getWidth()-random.randrange(car.getWidth()))
            if racecar.hits(self.frog):
                self.game_over = True

        for dozer in self.dozers:
            dozer.move()
            if dozer.atDesiredLocation():
                dozer.setX(self.window_width + self.cell_size + random.randrange(self.cell_size))
            if dozer.hits(self.frog):
                self.game_over = True
            
        for log_right in self.logs_right:
            log_right.move()
            if log_right.atDesiredLocation():
                log_right.setX(-log_right.getWidth()-random.randrange(log_right.getWidth()))
            log_right.supports(self.frog)

        for turtle in self.turtles:
            turtle.move()
            if turtle.atDesiredLocation():
                turtle.setX(self.window_width + self.cell_size + random.randrange(self.cell_size))
            turtle.supports(self.frog)

    #Where objects are drawn
    def draw(self, surface):
        surface.fill((255,255,255))

        if self.game_over:
            surface.fill((255,0,0))
            return
        
        if self.game_win:
            surface.fill((0,255,0))
            return
        
        for road in self.roads:
            draw_obj(surface, road, (10,10,10))

        for car in self.cars:
            draw_obj(surface, car, (255,10,10))
        
        for racecar in self.racecars:
            draw_obj(surface, racecar, (160,32,240))

        for dozer in self.dozers:
            draw_obj(surface,dozer, (255,192,203))

        for water in self.waters:
            draw_obj(surface, water, (0,0,255))

        for log_right in self.logs_right:
            draw_obj(surface, log_right, (150,75,0))

        for turtle in self.turtles:
            draw_obj(surface, turtle, (1,75,32))

        draw_obj(surface, self.stage1, (200,200,200))
        draw_obj(surface, self.stage2, (200,200,200))
        draw_obj(surface, self.grass1, (1,50,32))
        draw_obj(surface, self.grass2, (1,50,32))
        draw_obj(surface, self.grass3, (1,50,32))
        draw_obj(surface, self.home1, (255,255,0))
        draw_obj(surface, self.home2, (255,255,0))
        draw_obj(surface, self.home3, (255,255,0))
        draw_obj(surface, self.frog, (0,255,0))

#Universal function
def draw_obj(surface, obj, color): #This doesn't need to be indented into the class & can be used universally
    r = pygame.Rect(obj.getX(), obj.getY(), obj.getWidth(), obj.getHeight())
    pygame.draw.rect(surface, color, r)     