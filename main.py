import pygame, time, random
import paddle as pdl
import ball
import brick

pygame.init()
pygame.mixer.init()
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
ACT_POWERUP = [""]

# Store original ball speeds for proper slowdown effect
ORIGINAL_BALL_SPEED_X = 12
ORIGINAL_BALL_SPEED_Y = 12

POWERUP_Y_START = min(100, 200) + 400
FONT = pygame.font.SysFont(None, 48)

brick_hit_sound = pygame.mixer.Sound("assets/pong2.wav")
paddle_hit_sound = pygame.mixer.Sound("assets/pong3.wav")
powerup_sound = pygame.mixer.Sound("assets/power-up.wav")

brick_hit_sound.set_volume(0.4)
paddle_hit_sound.set_volume(0.6)
powerup_sound.set_volume(0.7)

l = ["assets/bg1.mp3","assets/bg2.mp3"]
pygame.mixer.music.load(random.choice(l))
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

player = pdl.paddle(SCREEN_WIDTH,SCREEN_HEIGHT)
balls = [ball.ball(SCREEN_WIDTH, SCREEN_HEIGHT)]
bricks_map = brick.bricks(SCREEN_WIDTH,SCREEN_HEIGHT)

active_effects = {}

def powerup_activater():
    global LIVES, flash_message, flash_timer
    new_powerups = [p for p in ACT_POWERUP if p]
    ACT_POWERUP.clear()
    if new_powerups:
        powerup_sound.play()
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
        elif powerup == "Dash":
            active_effects["Dash"] = time.time()
            for b in balls:
                b.VELOCITY_X *= 1.5
                b.VELOCITY_Y *= 1.5
                b.dashing = True

def apply_slowdown_effect():
    import math
    for b in balls:
        current_speed = math.sqrt(b.VELOCITY_X**2 + b.VELOCITY_Y**2)
        if current_speed > 0:
            direction_x = b.VELOCITY_X / current_speed
            direction_y = b.VELOCITY_Y / current_speed
            b.VELOCITY_X = direction_x * 7
            b.VELOCITY_Y = direction_y * 7

def remove_slowdown_effect():
    import math
    for b in balls:
        current_speed = math.sqrt(b.VELOCITY_X**2 + b.VELOCITY_Y**2)
        if current_speed > 0:
            direction_x = b.VELOCITY_X / current_speed
            direction_y = b.VELOCITY_Y / current_speed
            b.VELOCITY_X = direction_x * 12
            b.VELOCITY_Y = direction_y * 12

def main_menu():
    menu_font = pygame.font.SysFont(None, 72)
    title_text = menu_font.render("BRICK BREAKER", True, (255, 255, 255))
    start_text = FONT.render("Press SPACE to Start", True, (200, 200, 200))
    quit_text = FONT.render("Press ESC to Quit", True, (200, 200, 200))

    while True:
        DISPLAYSURF.fill((0, 0, 0))
        DISPLAYSURF.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 300))
        DISPLAYSURF.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, 450))
        DISPLAYSURF.blit(quit_text, (SCREEN_WIDTH // 2 - quit_text.get_width() // 2, 520))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

main_menu()
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
    brick_left = bricks_map.LEFT_MARGIN
    brick_right = SCREEN_WIDTH - bricks_map.LEFT_MARGIN
    if player.rect.left < brick_left:
        player.rect.left = brick_left
    if player.rect.right > brick_right:
        player.rect.right = brick_right
    
    # Fill background with dark gray
    DISPLAYSURF.fill((30, 30, 30))

    # Create playfield area with distinct styling
    playfield_rect = pygame.Rect(
        bricks_map.LEFT_MARGIN,
        bricks_map.TOP_MARGIN,
        SCREEN_WIDTH - 2 * bricks_map.LEFT_MARGIN,
        bricks_map.ROWS * (bricks_map.HEIGHT + bricks_map.PADDING) - bricks_map.PADDING
    )
    
    # Draw playfield background (lighter color to stand out)
    pygame.draw.rect(DISPLAYSURF, (50, 50, 60), playfield_rect)
    
    # Add a border around the playfield for even more distinction
    pygame.draw.rect(DISPLAYSURF, (100, 100, 120), playfield_rect, 3)

    # Handle slowdown effect expiration
    if "Speeddown" in active_effects:
        if time.time() - active_effects["Speeddown"] >= 5:
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
            paddle_hit_sound.play()

        if b.RECT.left < brick_left:
            b.RECT.left = brick_left
            b.flip_horizontally()

        if b.RECT.right > brick_right:
            b.RECT.right = brick_right
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

        for brc in bricks_map.bricks:
            if brc["active"] and b.RECT.colliderect(brc["rect"]):
                if not getattr(b, "dashing", False):
                    dx = b.RECT.centerx - brc["rect"].centerx
                    dy = b.RECT.centery - brc["rect"].centery
                    overlap_x = (brc["rect"].width // 2 + b.RECT.width // 2) - abs(dx)
                    overlap_y = (brc["rect"].height // 2 + b.RECT.height // 2) - abs(dy)
                    if overlap_x < overlap_y:
                        b.flip_horizontally()
                    else:
                        b.flip_vertically()
                brc["active"] = False
                brick_hit_sound.play()
                SCORE += 10
                if brc["powerup"] != None:
                    power = brc["powerup"]
                    ACT_POWERUP.append(power)
        b.draw(DISPLAYSURF)

    player.draw(DISPLAYSURF)
    bricks_map.draw(DISPLAYSURF)

    score_label = FONT.render(f"Score: {SCORE}", True, (255, 255, 255))
    DISPLAYSURF.blit(score_label, (50, 1000))
    lives_label = FONT.render(f"Lives: {LIVES}", True, (255, 0, 0))
    DISPLAYSURF.blit(lives_label, (SCREEN_WIDTH - 200, 50))

    for idx, (effect, start_time) in enumerate(active_effects.items()):
        remaining = max(0, int(5 - (time.time() - start_time)))
        label = FONT.render(f"{effect} ({remaining}s)", True, (255, 255, 255))
        DISPLAYSURF.blit(label, (SCREEN_WIDTH - 300, POWERUP_Y_START + idx * 40))
    
    # Display flash message
    if time.time() - flash_timer < 2:
        flash_text = FONT.render(flash_message, True, (255, 255, 0))
        text_rect = flash_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
        DISPLAYSURF.blit(flash_text, text_rect)

    if "Dash" in active_effects:
        if time.time() - active_effects["Dash"] >= 10:
            for b in balls:
                b.VELOCITY_X /= 1.5
                b.VELOCITY_Y /= 1.5
                b.dashing = False
            del active_effects["Dash"]

    # Check if all bricks are destroyed
    if all(not brick["active"] for brick in bricks_map.bricks):
        flash_text = FONT.render("You Win!", True, (0, 255, 0))
        text_rect = flash_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        DISPLAYSURF.blit(flash_text, text_rect)
        pygame.display.update()
        time.sleep(2)

        # Reset everything
        SCORE = 0
        LIVES = 3
        ACT_POWERUP.clear()
        active_effects.clear()
        balls = [ball.ball(SCREEN_WIDTH, SCREEN_HEIGHT)]
        bricks_map = brick.bricks(SCREEN_WIDTH, SCREEN_HEIGHT)
        BALL_ON_PADDLE = True
        player = pdl.paddle(SCREEN_WIDTH, SCREEN_HEIGHT)

        main_menu()

    if LIVES < 1:
        game_over_text = FONT.render(f"Game Over! Score: {SCORE}", True, (255, 0, 0))
        DISPLAYSURF.blit(game_over_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2))
        pygame.display.update()
        time.sleep(2)
        
        # Reset game state
        SCORE = 0
        LIVES = 3
        ACT_POWERUP.clear()
        active_effects.clear()
        balls = [ball.ball(SCREEN_WIDTH, SCREEN_HEIGHT)]
        bricks_map = brick.bricks(SCREEN_WIDTH, SCREEN_HEIGHT)
        BALL_ON_PADDLE = True
        player = pdl.paddle(SCREEN_WIDTH, SCREEN_HEIGHT)
        
        main_menu()  # Go back to menu instead of quitting

    pygame.display.update()
pygame.quit()
exit()