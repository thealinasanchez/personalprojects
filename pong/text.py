import pygame

class Text:

    def __init__( self, string, x, y ):
        self.mX = x
        self.mY = y
        self.mString = string
        self.mColor = ( 255, 255, 255 )
        font_height = 24
        self.mFont = pygame.font.SysFont( "Courier New", font_height )
        return

    def setText( self, string ):
        self.mString = string
        return

    def setColor( self, color ):
        self.mColor = color
        return

    def setSize( self, size ):
        self.mFont = pygame.font.SysFont( "Courier New", size )
        return

    def draw( self, surface ):
        text_object = self.mFont.render( self.mString, False, self.mColor )
        text_rect = text_object.get_rect( )
        text_rect.center = ( int( self.mX ), int( self.mY ) )
        surface.blit( text_object, text_rect )
        return
