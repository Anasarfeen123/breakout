import pygame
import paddle as pdl
import ball

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

player = pdl.paddle(SCREEN_WIDTH,SCREEN_HEIGHT)
ball = ball.ball(SCREEN_WIDTH,SCREEN_HEIGHT)

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
        ball.VELOCITY_Y *= -1
    if ball.RECT.left < 0:
        ball.RECT.left = 0
        ball.VELOCITY_X *= -1
    if ball.RECT.right > SCREEN_WIDTH:
        ball.RECT.right = SCREEN_WIDTH
        ball.VELOCITY_X *= -1
    if ball.RECT.top <= 0:
        ball.RECT.top = 0
        ball.VELOCITY_Y *= -1
    if ball.RECT.bottom > SCREEN_HEIGHT:
        RUNNING = False
        
    player.draw(DISPLAYSURF)
    ball.draw(DISPLAYSURF)

    pygame.display.update()

pygame.quit()
exit()
