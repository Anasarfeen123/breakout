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
ACT_POWERUP = ["Hi"]

player = pdl.paddle(SCREEN_WIDTH,SCREEN_HEIGHT)
ball = ball.ball(SCREEN_WIDTH,SCREEN_HEIGHT)
bricks = brick.bricks(SCREEN_WIDTH,SCREEN_HEIGHT)

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
        if ball.RECT.top < player.rect.bottom or ball.RECT.bottom > player.rect.top:
            ball.flip_vertically()
        else:
            ball.flip_vertically()
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
        RUNNING = False

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
                ACT_POWERUP.append(brick["powerup"])

    player.draw(DISPLAYSURF)
    ball.draw(DISPLAYSURF)
    bricks.draw(DISPLAYSURF)
    
    score = pygame.font.SysFont(None, 48)
    score_label = score.render(f"Score: {SCORE}", True, (255, 255, 255))
    DISPLAYSURF.blit(score_label, (50, 1000))
    
    font = pygame.font.SysFont(None, 36)
    for idx, power in enumerate(ACT_POWERUP):
        label = font.render(f"Powerup: {power}", True, (255, 255, 255))
        DISPLAYSURF.blit(label, (SCREEN_WIDTH - 500, 1100 + idx * 40))
    pygame.display.update()

pygame.quit()
exit()
