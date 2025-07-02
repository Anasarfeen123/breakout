import pygame, random

class bricks:
    def __init__(self, screen_width, screen_height):
        self.WIDTH = 80
        self.HEIGHT = 30
        self.PADDING = 10
        self.ROWS = 6
        self.COLS = 16
        total_width = self.COLS * (self.WIDTH + self.PADDING) - self.PADDING
        self.LEFT_MARGIN = (screen_width - total_width) // 2

        self.TOP_MARGIN = 50
        palette = [
    (255, 69, 0),     # Red-Orange (like Fire)
    (0, 255, 0),      # Neon Green
    (0, 191, 255),    # Deep Sky Blue
    (255, 20, 147),   # Hot Pink
    (255, 255, 0),    # Bright Yellow
    (138, 43, 226),   # Electric Purple (Blue Violet)
    (255, 105, 180),  # Vivid Pink (Hot Pinkish)
]

        # self.color_pal = [[(255, 0, 110), (0, 255, 200), (255, 255, 0), (0, 120, 255)],[(255, 204, 204), (204, 229, 255), (204, 255, 229), (255, 255, 204)]]
        self.color = palette
        self.bricks = []
        self.powerups = ["Extra Balls","Speeddown","Extra Life","Dash"] 


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
                    self.bricks[-1]["color"] = (255, 94, 87)

    def draw(self, screen):
        for brick in self.bricks:
            if brick["active"]:
                pygame.draw.rect(screen, brick["color"], brick["rect"], border_radius = 6)

                if brick["powerup"] is not None:
                    # Draw powerup symbol
                    font = pygame.font.SysFont(None, 24)
                    powerup_symbol = "P"
                    text = font.render(powerup_symbol, True, (255, 255, 255))
                    text_rect = text.get_rect(center=brick["rect"].center)
                    screen.blit(text, text_rect)
