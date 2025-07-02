import pygame
import paddle as pdl
import ball
import brick

pygame.init()

DISPLAYSURF = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
FPS = 60
clock = pygame.time.Clock()
RUNNING = True
SCREEN_WIDTH = DISPLAYSURF.get_width()
SCREEN_HEIGHT = DISPLAYSURF.get_height()
pygame.display.set_caption('Brick Breaker')
VELOCITY_Main = 30
VELOCITY_X = 0
SCORE = 0
ACT_POWERUP = []
powerup_y_start = min(100, 200) + 400
LIVES = 3
player = pdl.paddle(SCREEN_WIDTH,SCREEN_HEIGHT)
ball = ball.ball(SCREEN_WIDTH,SCREEN_HEIGHT)
bricks = brick.bricks(SCREEN_WIDTH,SCREEN_HEIGHT)

font = pygame.font.SysFont(None, 48)

while RUNNING:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT :
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                RUNNING = False
    keys = pygame.key.get_pressed()
    VELOCITY_X = 0
    if keys[pygame.K_LEFT]:
        VELOCITY_X = -VELOCITY_Main
    if keys[pygame.K_RIGHT]:
        VELOCITY_X = VELOCITY_Main
    player.rect.x += VELOCITY_X
    if player.rect.left < 0:
        player.rect.left = 0
    if player.rect.right > SCREEN_WIDTH:
        player.rect.right = SCREEN_WIDTH
    DISPLAYSURF.fill((0, 0, 0))
    
    ball.move()

    if ball.RECT.colliderect(player.rect):
        if ball.RECT.bottom > player.rect.top:
            ball.flip_vertically()
            ball.RECT.bottom = player.rect.top 
        elif ball.RECT.top > player.rect.bottom:
            ball.flip_vertically()
            ball.RECT.top = player.rect.bottom
        elif ball.RECT.left > player.rect.right:
            ball.flip_horizontally()
            ball.RECT.left = player.rect.right
        elif ball.RECT.right > player.rect.left:
            ball.flip_horizontally()
            ball.RECT.right = player.rect.left
    if ball.RECT.left < 0:
        ball.RECT.left = 0
        ball.flip_horizontally()
    if ball.RECT.right > SCREEN_WIDTH:
        ball.RECT.right = SCREEN_WIDTH
        ball.flip_horizontally()
    if ball.RECT.top <= 0:
        ball.RECT.top = 0
        ball.flip_vertically()
    if ball.RECT.bottom > SCREEN_HEIGHT:
        LIVES -= 1
        ball.flip_vertically()

    for brick in bricks.bricks:
        if brick["active"] and ball.RECT.colliderect(brick["rect"]):
            dx = ball.RECT.centerx - brick["rect"].centerx
            dy = ball.RECT.centery - brick["rect"].centery
            overlap_x = (brick["rect"].width // 2 + ball.RECT.width // 2) - abs(dx)
            overlap_y = (brick["rect"].height // 2 + ball.RECT.height // 2) - abs(dy)
            if overlap_x < overlap_y:
                ball.flip_horizontally()
            else:
                ball.flip_vertically()
            brick["active"] = False
            SCORE += 10
            if brick["powerup"] != None:
                power = brick["powerup"]
                ACT_POWERUP.append(power)
                print(power)
    player.draw(DISPLAYSURF)
    ball.draw(DISPLAYSURF)
    bricks.draw(DISPLAYSURF)
    
    score_label = font.render(f"Score: {SCORE}", True, (255, 255, 255))
    DISPLAYSURF.blit(score_label, (50, 1000))
    
    for idx, power in enumerate(ACT_POWERUP):
        label = font.render(f"{power}", True, (255, 255, 255))
        DISPLAYSURF.blit(label, (SCREEN_WIDTH - 300, powerup_y_start + idx * 40))
    pygame.display.update()

    if LIVES < 1:
        RUNNING = False
pygame.quit()
exit()
