import pygame
import random

pygame.init()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (100, 100, 255)
RED = (255, 0, 0)
LIGHT_RED = (255, 100, 100)
GRAY = (150, 150, 150)
DARK_GRAY = (50, 50, 50)
YELLOW = (255, 255, 0)

# Screen dimensions
WIDTH = 800
HEIGHT = 600

# Paddle dimensions
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 100
PADDLE_SPEED = 7

# Ball dimensions
BALL_SIZE = 15
BALL_SPEED_X = 5
BALL_SPEED_Y = 5

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong Game")

# Font for score display
font = pygame.font.SysFont("arial", 50, bold=True)
controls_font = pygame.font.SysFont("arial", 24)
title_font = pygame.font.SysFont("arial", 28, bold=True)

def draw_paddle(x, y, color, highlight_color):
    # Draw main paddle
    pygame.draw.rect(screen, color, [x, y, PADDLE_WIDTH, PADDLE_HEIGHT])
    
    # Add highlight for 3D effect
    pygame.draw.rect(screen, highlight_color, [x, y, PADDLE_WIDTH, 5])
    pygame.draw.rect(screen, highlight_color, [x, y, 5, PADDLE_HEIGHT])

def draw_ball(x, y):
    # Draw ball with gradient effect
    pygame.draw.circle(screen, WHITE, (int(x + BALL_SIZE/2), int(y + BALL_SIZE/2)), int(BALL_SIZE/2))
    pygame.draw.circle(screen, GRAY, (int(x + BALL_SIZE/2 - 2), int(y + BALL_SIZE/2 - 2)), int(BALL_SIZE/4))

def show_score(player_score, ai_score):
    # Create score backgrounds
    player_bg = pygame.Surface((80, 60), pygame.SRCALPHA)
    player_bg.fill((0, 0, 100, 150))
    ai_bg = pygame.Surface((80, 60), pygame.SRCALPHA)
    ai_bg.fill((100, 0, 0, 150))
    
    screen.blit(player_bg, (WIDTH // 4 - 40, 10))
    screen.blit(ai_bg, (3 * WIDTH // 4 - 40, 10))
    
    player_text = font.render(str(player_score), True, BLUE)
    ai_text = font.render(str(ai_score), True, RED)
    
    screen.blit(player_text, (WIDTH // 4 - player_text.get_width()//2, 20))
    screen.blit(ai_text, (3 * WIDTH // 4 - ai_text.get_width()//2, 20))

def show_controls():
    # Create a semi-transparent background for controls in the center
    controls_bg = pygame.Surface((300, 180), pygame.SRCALPHA)
    controls_bg.fill((0, 0, 0, 180))
    screen.blit(controls_bg, (WIDTH // 2 - 150, 20))
    
    # Draw controls text with better styling
    title = title_font.render("CONTROLS", True, YELLOW)
    up_text = controls_font.render("↑ : Move Up", True, WHITE)
    down_text = controls_font.render("↓ : Move Down", True, WHITE)
    r_text = controls_font.render("R : Replay (when game over)", True, WHITE)
    esc_text = controls_font.render("ESC : Return to Menu", True, WHITE)
    
    # Center the text
    title_width = title.get_width()
    screen.blit(title, (WIDTH // 2 - title_width // 2, 30))
    
    # Add a decorative line
    pygame.draw.line(screen, YELLOW, (WIDTH // 2 - 100, 65), (WIDTH // 2 + 100, 65), 2)
    
    # Center the control instructions
    screen.blit(up_text, (WIDTH // 2 - 80, 80))
    screen.blit(down_text, (WIDTH // 2 - 80, 110))
    screen.blit(r_text, (WIDTH // 2 - 110, 140))
    screen.blit(esc_text, (WIDTH // 2 - 110, 170))

def create_background():
    # Create a gradient background
    background = pygame.Surface((WIDTH, HEIGHT))
    for y in range(HEIGHT):
        # Gradient from dark to slightly lighter
        color_value = 20 + (y / HEIGHT) * 30
        pygame.draw.line(background, (0, 0, color_value), (0, y), (WIDTH, y))
    
    # Add some subtle patterns
    for _ in range(50):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        size = random.randint(5, 20)
        alpha = random.randint(10, 30)
        s = pygame.Surface((size, size), pygame.SRCALPHA)
        s.fill((255, 255, 255, alpha))
        background.blit(s, (x, y))
    
    return background

background = create_background()

def draw_court():
    # Draw center line
    for y in range(0, HEIGHT, 30):
        pygame.draw.rect(screen, WHITE, (WIDTH // 2 - 2, y, 4, 15))
    
    # Draw center circle
    pygame.draw.circle(screen, WHITE, (WIDTH // 2, HEIGHT // 2), 50, 2)
    
    # Draw court boundaries
    pygame.draw.rect(screen, WHITE, (0, 0, WIDTH, HEIGHT), 4)

def game_loop():
    # Game variables
    player_paddle_y = HEIGHT // 2 - PADDLE_HEIGHT // 2
    ai_paddle_y = HEIGHT // 2 - PADDLE_HEIGHT // 2
    
    ball_x = WIDTH // 2 - BALL_SIZE // 2
    ball_y = HEIGHT // 2 - BALL_SIZE // 2
    ball_dx = BALL_SPEED_X * random.choice([-1, 1])
    ball_dy = BALL_SPEED_Y * random.choice([-1, 1])
    
    player_score = 0
    ai_score = 0
    
    # Track consecutive misses
    player_consecutive_misses = 0
    ai_consecutive_misses = 0
    
    # Game state
    game_over = False
    winner = None
    
    clock = pygame.time.Clock()
    running = True
    return_to_menu = False
    
    while running and not return_to_menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return_to_menu = True
                if event.key == pygame.K_r and game_over:
                    # Reset and restart the game
                    return game_loop()
        
        # Only process game logic if not game over
        if not game_over:
            # Player paddle movement
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP] and player_paddle_y > 0:
                player_paddle_y -= PADDLE_SPEED
            if keys[pygame.K_DOWN] and player_paddle_y < HEIGHT - PADDLE_HEIGHT:
                player_paddle_y += PADDLE_SPEED
            
            # AI paddle movement (simple AI)
            if ai_paddle_y + PADDLE_HEIGHT // 2 < ball_y and ai_paddle_y < HEIGHT - PADDLE_HEIGHT:
                ai_paddle_y += min(PADDLE_SPEED - 1, ball_y - (ai_paddle_y + PADDLE_HEIGHT // 2))
            elif ai_paddle_y + PADDLE_HEIGHT // 2 > ball_y and ai_paddle_y > 0:
                ai_paddle_y -= min(PADDLE_SPEED - 1, (ai_paddle_y + PADDLE_HEIGHT // 2) - ball_y)
            
            # Ball movement
            ball_x += ball_dx
            ball_y += ball_dy
        
        # Ball collision with top and bottom
        if ball_y <= 0 or ball_y >= HEIGHT - BALL_SIZE:
            ball_dy *= -1
            # Add sound effect here if desired
        
        # Ball collision with paddles
        if ball_x <= PADDLE_WIDTH and player_paddle_y < ball_y < player_paddle_y + PADDLE_HEIGHT:
            ball_dx = abs(ball_dx) * 1.05  # Speed up slightly
            # Add some randomness to the bounce
            ball_dy += random.uniform(-1, 1)
            # Add sound effect here if desired
        
        if ball_x >= WIDTH - PADDLE_WIDTH - BALL_SIZE and ai_paddle_y < ball_y < ai_paddle_y + PADDLE_HEIGHT:
            ball_dx = -abs(ball_dx) * 1.05  # Speed up slightly
            # Add some randomness to the bounce
            ball_dy += random.uniform(-1, 1)
            # Add sound effect here if desired
        
        # Score points
        if ball_x < 0:
            ai_score += 1
            player_consecutive_misses += 1
            ai_consecutive_misses = 0
            
            # Check for game over (3 consecutive misses)
            if player_consecutive_misses >= 3:
                game_over = True
                winner = "ai"
            
            ball_x = WIDTH // 2 - BALL_SIZE // 2
            ball_y = HEIGHT // 2 - BALL_SIZE // 2
            ball_dx = BALL_SPEED_X * random.choice([-1, 1])
            ball_dy = BALL_SPEED_Y * random.choice([-1, 1])
        
        if ball_x > WIDTH:
            player_score += 1
            ai_consecutive_misses += 1
            player_consecutive_misses = 0
            
            # Check for game over (3 consecutive misses)
            if ai_consecutive_misses >= 3:
                game_over = True
                winner = "player"
            
            ball_x = WIDTH // 2 - BALL_SIZE // 2
            ball_y = HEIGHT // 2 - BALL_SIZE // 2
            ball_dx = BALL_SPEED_X * random.choice([-1, 1])
            ball_dy = BALL_SPEED_Y * random.choice([-1, 1])
        
        # Drawing
        screen.blit(background, (0, 0))
        
        # Draw court
        draw_court()
        
        # Draw paddles with 3D effect
        draw_paddle(0, player_paddle_y, BLUE, LIGHT_BLUE)
        draw_paddle(WIDTH - PADDLE_WIDTH, ai_paddle_y, RED, LIGHT_RED)
        
        # Draw ball
        draw_ball(ball_x, ball_y)
        
        # Show score
        show_score(player_score, ai_score)
        
        # Show controls
        show_controls()
        
        # Show game over if needed
        if game_over:
            show_game_over(winner)
        
        pygame.display.update()
        clock.tick(60)
    
    # We don't actually want to quit pygame here, just return to the main menu
    return

if __name__ == "__main__":
    game_loop()
def show_game_over(winner):
    # Create a semi-transparent background
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))
    
    # Show game over message
    game_over_font = pygame.font.SysFont("arial", 60, bold=True)
    if winner == "player":
        text = game_over_font.render("YOU WIN!", True, BLUE)
    else:
        text = game_over_font.render("YOU LOSE!", True, RED)
    
    screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - 50))
    
    # Show instruction to return to menu or replay
    instruction = controls_font.render("Press R to replay or ESC for menu", True, WHITE)
    screen.blit(instruction, (WIDTH//2 - instruction.get_width()//2, HEIGHT//2 + 30))
