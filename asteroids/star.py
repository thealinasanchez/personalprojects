import random
import circle


class Star(circle.Circle):
    def __init__(self, x, y, world_width, world_height):
        super().__init__(x,y,0,0,0,2,world_width,world_height)
        self.setBrightness(random.randint(0,255))
    
    def getBrightness(self):
        return self.mBrightness
    
    def setBrightness(self,brightness):
        if brightness >= 0 and brightness <= 255:
            self.mBrightness = brightness
            self.setColor((brightness,brightness,brightness))
    
    def evolve(self, dt):
        choice = random.choice([-10, 0, 10])
        new_brightness = self.getBrightness() + choice
        if new_brightness >= 0 and new_brightness <= 255:
            self.setBrightness(new_brightness)
            
    
    
    