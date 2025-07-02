import pygame, time
import paddle as pdl
import ball
import brick

pygame.init()

pygame.display.set_caption('Brick Breaker')

clock = pygame.time.Clock()

flash_message = ""
flash_timer = 0

DISPLAYSURF = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
FPS = 60
RUNNING = True

SCREEN_WIDTH = DISPLAYSURF.get_width()
SCREEN_HEIGHT = DISPLAYSURF.get_height()

VELOCITY_MAIN = 30
VELOCITY_X = 0
BALL_ON_PADDLE = True

SCORE = 0
LIVES = 3
ACT_POWERUP = []

# Store original ball speeds for proper slowdown effect
ORIGINAL_BALL_SPEED_X = 12
ORIGINAL_BALL_SPEED_Y = 12

POWERUP_Y_START = min(100, 200) + 400
FONT = pygame.font.SysFont(None, 48)

player = pdl.paddle(SCREEN_WIDTH,SCREEN_HEIGHT)
balls = [ball.ball(SCREEN_WIDTH, SCREEN_HEIGHT)]
bricks = brick.bricks(SCREEN_WIDTH,SCREEN_HEIGHT)

active_effects = {}

def powerup_activater():
    global LIVES, flash_message, flash_timer
    new_powerups = ACT_POWERUP.copy()
    ACT_POWERUP.clear()
    for powerup in new_powerups:
        flash_message = f"{powerup} activated!"
        flash_timer = time.time()
        if powerup == "Extra Life":
            LIVES += 1
        elif powerup == "Speeddown":
            active_effects["Speeddown"] = time.time()
            apply_slowdown_effect()
        elif powerup == "Extra Balls":
            if len(balls) < 5:
                new_ball = ball.ball(SCREEN_WIDTH, SCREEN_HEIGHT)
                new_ball.RECT.centerx = balls[0].RECT.centerx
                new_ball.RECT.centery = balls[0].RECT.centery
                new_ball.flip_horizontally() 
                balls.append(new_ball)
        
        elif powerup == "Long Reach":
            player.WIDTH += 5

def apply_slowdown_effect():
    import math
    for b in balls:
        current_speed = math.sqrt(b.VELOCITY_X**2 + b.VELOCITY_Y**2)
        if current_speed > 0:
            direction_x = b.VELOCITY_X / current_speed
            direction_y = b.VELOCITY_Y / current_speed
            b.VELOCITY_X = direction_x * 5
            b.VELOCITY_Y = direction_y * 5

def remove_slowdown_effect():
    import math
    for b in balls:
        current_speed = math.sqrt(b.VELOCITY_X**2 + b.VELOCITY_Y**2)
        if current_speed > 0:
            direction_x = b.VELOCITY_X / current_speed
            direction_y = b.VELOCITY_Y / current_speed
            b.VELOCITY_X = direction_x * 12
            b.VELOCITY_Y = direction_y * 12

while RUNNING:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT :
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                RUNNING = False
            if event.key == pygame.K_SPACE and BALL_ON_PADDLE:
                BALL_ON_PADDLE = False
    keys = pygame.key.get_pressed()
    powerup_activater()
    VELOCITY_X = 0
    if keys[pygame.K_LEFT]:
        VELOCITY_X = -VELOCITY_MAIN
    if keys[pygame.K_RIGHT]:
        VELOCITY_X = VELOCITY_MAIN
    player.rect.x += VELOCITY_X
    if player.rect.left < 0:
        player.rect.left = 0
    if player.rect.right > SCREEN_WIDTH:
        player.rect.right = SCREEN_WIDTH
    DISPLAYSURF.fill((0, 0, 0))

    # Handle slowdown effect expiration
    if "Speeddown" in active_effects:
        if time.time() - active_effects["Speeddown"] >= 10:
            remove_slowdown_effect()
            del active_effects["Speeddown"]

    if not BALL_ON_PADDLE:
        for b in balls:
            b.move()

    for b in balls:
        if BALL_ON_PADDLE:
            b.RECT.centerx = player.rect.centerx
            b.RECT.bottom = player.rect.top

        if b.RECT.colliderect(player.rect) and b.VELOCITY_Y > 0:
            b.VELOCITY_Y *= -1
            offset = (b.RECT.centerx - player.rect.centerx) / (player.rect.width / 2)
            b.VELOCITY_X += offset * 2
            b.RECT.bottom = player.rect.top

        if b.RECT.left < 0:
            b.RECT.left = 0
            b.flip_horizontally()

        if b.RECT.right > SCREEN_WIDTH:
            b.RECT.right = SCREEN_WIDTH
            b.flip_horizontally()

        if b.RECT.top <= 0:
            b.RECT.top = 0
            b.flip_vertically()

        if b.RECT.bottom > SCREEN_HEIGHT:
            balls.remove(b)
            if len(balls) == 0:
                LIVES -= 1
                BALL_ON_PADDLE = True
                balls.append(ball.ball(SCREEN_WIDTH, SCREEN_HEIGHT))
                break

        for brick in bricks.bricks:
            if brick["active"] and b.RECT.colliderect(brick["rect"]):
                dx = b.RECT.centerx - brick["rect"].centerx
                dy = b.RECT.centery - brick["rect"].centery
                overlap_x = (brick["rect"].width // 2 + b.RECT.width // 2) - abs(dx)
                overlap_y = (brick["rect"].height // 2 + b.RECT.height // 2) - abs(dy)
                if overlap_x < overlap_y:
                    b.flip_horizontally()
                else:
                    b.flip_vertically()
                brick["active"] = False
                SCORE += 10
                if brick["powerup"] != None:
                    power = brick["powerup"]
                    ACT_POWERUP.append(power)
                    print(power)
        b.draw(DISPLAYSURF)

    
    player.draw(DISPLAYSURF)
    bricks.draw(DISPLAYSURF)
    
    score_label = FONT.render(f"Score: {SCORE}", True, (255, 255, 255))
    DISPLAYSURF.blit(score_label, (50, 1000))
    lives_label = FONT.render(f"Lives: {LIVES}", True, (255, 0, 0))
    DISPLAYSURF.blit(lives_label, (SCREEN_WIDTH - 200, 50))

    for idx, (effect, start_time) in enumerate(active_effects.items()):
        remaining = max(0, int(10 - (time.time() - start_time)))
        label = FONT.render(f"{effect} ({remaining}s)", True, (255, 255, 255))
        DISPLAYSURF.blit(label, (SCREEN_WIDTH - 300, POWERUP_Y_START + idx * 40))
    
    # Display flash message
    if time.time() - flash_timer < 2:  # Show message for 2 seconds
        flash_text = FONT.render(flash_message, True, (255, 255, 0))
        text_rect = flash_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
        DISPLAYSURF.blit(flash_text, text_rect)

    if LIVES < 1:
        game_over_text = FONT.render("Game Over!", True, (255, 0, 0))
        DISPLAYSURF.blit(game_over_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2))
        pygame.display.update()
        time.sleep(2)
        RUNNING = False

    pygame.display.update()
pygame.quit()
exit()