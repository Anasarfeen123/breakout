import pygame

class ball:
    def __init__(self,screen_width,screen_height):
        self.RADIUS = 20
        self.X_POS = screen_width // 2
        self.Y_POS = screen_height // 2
        self.VELOCITY_X = 10
        self.VELOCITY_Y = 10
        self.COLOR = (255,255,255)
        self.RECT = pygame.Rect(self.X_POS - self.RADIUS, self.Y_POS - self.RADIUS, self.RADIUS * 2, self.RADIUS * 2)

    def draw(self, screen):
        pygame.draw.circle(screen, self.COLOR, self.RECT.center, self.RADIUS)
    
    def move(self):
        self.RECT.x += self.VELOCITY_X
        self.RECT.y += self.VELOCITY_Y
    
    def flip_vertically(self):
        self.VELOCITY_Y *= -1
    def flip_horizontally(self):
        self.VELOCITY_X *= -1