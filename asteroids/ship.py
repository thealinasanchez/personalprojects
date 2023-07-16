import polygon
import bullet

class Ship(polygon.Polygon):
    def __init__(self, x, y, world_width, world_height):
        super().__init__(x, y, 0, 0, 0, world_width, world_height)
        self.setPolygon([(10, 0),(-10, 10),(-10, -10)])
        
    def evolve(self, dt):
        self.move(dt)
        
    def fire(self):
        outline = self.getPolygon()
        gun_x, gun_y = self.rotateAndTranslatePoint(outline[0][0], outline[0][1])
        b = bullet.Bullet(gun_x, gun_y, self.dx, self.dy, self.getRotation(), self.getWorldWidth(), self.getWorldHeight())
        return b
        
        