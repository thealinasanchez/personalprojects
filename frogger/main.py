import pygame
import game
import frogger

TITLE = "Frogger"
NUM_ROWS = 11
NUM_COLS = 15
CELL_SIZE = 50
WINDOW_WIDTH  = NUM_COLS * CELL_SIZE
WINDOW_HEIGHT = NUM_ROWS * CELL_SIZE
DESIRED_RATE  = 30

class PygameApp(game.Game):

    def __init__(self, title, width, height, frame_rate):
        game.Game.__init__(self, title, width, height, frame_rate)

        # create a game instance
        self.game = frogger.Frogger(width, height, NUM_ROWS, NUM_COLS, CELL_SIZE)


    def game_logic(self, keys, newkeys, buttons, newbuttons, mouse_position, dt):
        # keys contains all keys currently held down
        # newkeys contains all keys pressed since the last frame
        # Use pygame.K_? as the keyboard keys.
        # Examples: pygame.K_a, pygame.K_UP, etc.
        # if pygame.K_UP in newkeys:
        #    The user just pressed the UP key
        #
        # buttons contains all mouse buttons currently held down
        # newbuttons contains all buttons pressed since the last frame
        # Use 1, 2, 3 as the mouse buttons
        # if 3 in buttons:
        #    The user is holding down the right mouse button
        #
        # mouse_position contains x and y location of mouse in window
        # dt contains the number of seconds since last frame

        # Update the state of the game instance
        if pygame.K_UP in keys:
            self.game.up()
        if pygame.K_DOWN in keys:
            self.game.down()
        if pygame.K_LEFT in keys:
            self.game.left()
        if pygame.K_RIGHT in keys:
            self.game.right()

        self.game.evolve(dt)

    def paint(self, surface):
        # Draw the current state of the game instance
        self.game.draw(surface)

def main():
    pygame.font.init()
    game = PygameApp(TITLE, WINDOW_WIDTH, WINDOW_HEIGHT, DESIRED_RATE)
    game.main_loop()

if __name__ == "__main__":
    main()
