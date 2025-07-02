import pygame

class paddle:
    def __init__(self,screen_width,screen_height):
        self.WIDTH = 150 
        self.HEIGHT = 10
        self.X_POS = (screen_width / 2) - (self.WIDTH / 2)
        self.Y_POS = screen_height - self.HEIGHT - 20
        self.SPEED = 10
        self.color = (255,255,255)
        self.rect = pygame.Rect(self.X_POS, self.Y_POS, self.WIDTH, self.HEIGHT)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
