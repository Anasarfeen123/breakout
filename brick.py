import pygame, random

class bricks:
    def __init__(self, screen_width, screen_height):
        self.WIDTH = 80
        self.HEIGHT = 30
        self.PADDING = 10
        self.ROWS = 6
        self.COLS = 16
        self.LEFT_MARGIN = 50
        self.TOP_MARGIN = 50
        self.color = [(0,255,255),(255,0,255),(255,255,0)]
        self.bricks = []
        self.powerups = ["2balls","speeddown","extralife"]

        for row in range(self.ROWS):
            for col in range(self.COLS):
                x = self.LEFT_MARGIN + col * (self.WIDTH + self.PADDING)
                y = self.TOP_MARGIN + row * (self.HEIGHT + self.PADDING)
                rect = pygame.Rect(x, y, self.WIDTH, self.HEIGHT)
                self.bricks.append({
                    "rect": rect,
                    "color": random.choice(self.color),
                    "active": True,
                    "powerup": None
                })
                if random.random() > 0.9:
                    power = random.choice(self.powerups)
                    self.bricks[-1]["powerup"] = power
                    self.bricks[-1]["color"] = (92, 46, 166)
                    # print(power)

    def draw(self, screen):
        for brick in self.bricks:
            if brick["active"]:
                pygame.draw.rect(screen, brick["color"], brick["rect"])
                pygame.draw.rect(screen, (255, 255, 255), brick["rect"], 2)

