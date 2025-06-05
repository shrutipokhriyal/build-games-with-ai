import pygame
import random
import math
import os

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH = 800
HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
DARK_BLUE = (0, 0, 50)

# Create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

# Background with stars
def create_starfield():
    starfield = pygame.Surface((WIDTH, HEIGHT))
    starfield.fill(DARK_BLUE)  # Dark blue background
    
    # Add stars of different sizes
    for _ in range(200):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        size = random.randint(1, 3)
        brightness = random.randint(180, 255)
        color = (brightness, brightness, brightness)
        pygame.draw.circle(starfield, color, (x, y), size)
    
    return starfield

background = create_starfield()

# Create spaceship
def create_spaceship():
    ship = pygame.Surface((50, 50), pygame.SRCALPHA)
    
    # Main body
    pygame.draw.polygon(ship, GREEN, [(25, 0), (0, 50), (50, 50)])
    
    # Cockpit
    pygame.draw.polygon(ship, BLUE, [(25, 15), (15, 40), (35, 40)])
    
    # Engines
    pygame.draw.rect(ship, RED, (5, 40, 10, 10))
    pygame.draw.rect(ship, RED, (35, 40, 10, 10))
    
    # Engine flames (animated later)
    pygame.draw.polygon(ship, YELLOW, [(10, 50), (5, 60), (15, 60)])
    pygame.draw.polygon(ship, YELLOW, [(40, 50), (35, 60), (45, 60)])
    
    return ship

# Create enemy ship
def create_enemy():
    enemy = pygame.Surface((40, 40), pygame.SRCALPHA)
    
    # Main body
    pygame.draw.ellipse(enemy, PURPLE, (0, 10, 40, 20))
    
    # Top dome
    pygame.draw.ellipse(enemy, RED, (10, 0, 20, 20))
    
    # Bottom lights
    pygame.draw.circle(enemy, YELLOW, (10, 20), 5)
    pygame.draw.circle(enemy, YELLOW, (30, 20), 5)
    
    return enemy

# Create bullet
def create_bullet():
    bullet = pygame.Surface((10, 20), pygame.SRCALPHA)
    
    # Laser beam
    pygame.draw.rect(bullet, BLUE, (0, 0, 10, 20))
    
    # Glow effect
    pygame.draw.rect(bullet, WHITE, (2, 0, 6, 5))
    
    return bullet

# Create explosion animation frames
def create_explosion_frames():
    frames = []
    sizes = [20, 30, 40, 30, 20]
    colors = [(255, 255, 0), (255, 165, 0), (255, 69, 0), (255, 0, 0), (100, 0, 0)]
    
    for i in range(5):
        frame = pygame.Surface((50, 50), pygame.SRCALPHA)
        pygame.draw.circle(frame, colors[i], (25, 25), sizes[i])
        if i > 0:  # Add some random particles
            for _ in range(i * 5):
                x = random.randint(5, 45)
                y = random.randint(5, 45)
                size = random.randint(1, 3)
                pygame.draw.circle(frame, WHITE, (x, y), size)
        frames.append(frame)
    
    return frames

# Load all game assets
player_img = create_spaceship()
enemy_img = create_enemy()
bullet_img = create_bullet()
explosion_frames = create_explosion_frames()

# Player variables
player_x = WIDTH // 2 - 25
player_y = HEIGHT - 100
player_speed = 5
player_dx = 0
player_dy = 0  # Added for vertical movement

# Enemy variables
enemy_x = []
enemy_y = []
enemy_dx = []
enemy_dy = []
enemy_alive = []
num_of_enemies = 8

for i in range(num_of_enemies):
    enemy_x.append(random.randint(0, WIDTH - 40))
    enemy_y.append(random.randint(50, 200))
    enemy_dx.append(random.choice([-3, -2, 2, 3]))
    enemy_dy.append(40)
    enemy_alive.append(True)

# Bullet variables
bullet_x = 0
bullet_y = HEIGHT - 100
bullet_dy = 10
bullet_state = "ready"  # ready - can't see bullet, fire - bullet is moving
bullet_cooldown = 0     # Cooldown timer for bullet firing
bullet_cooldown_max = 10  # Maximum cooldown time (lower = faster firing)

# Multiple bullets system
bullets = []  # List of active bullets [x, y]
max_bullets = 3  # Maximum number of bullets on screen

# Explosion variables
explosions = []  # List of [x, y, frame_index, timer]

# Score
score_value = 0
font = pygame.font.SysFont("arial", 36)
controls_font = pygame.font.SysFont("arial", 24)
title_font = pygame.font.SysFont("arial", 28, bold=True)

# Game over text
game_over_font = pygame.font.SysFont("arial", 72, bold=True)

def show_score():
    # Create a semi-transparent background for score
    score_bg = pygame.Surface((150, 40), pygame.SRCALPHA)
    score_bg.fill((0, 0, 0, 150))
    screen.blit(score_bg, (10, 10))
    
    score = font.render("Score: " + str(score_value), True, WHITE)
    screen.blit(score, (20, 15))

def show_controls():
    # Create a semi-transparent control panel
    controls_bg = pygame.Surface((200, 220), pygame.SRCALPHA)
    controls_bg.fill((0, 0, 0, 180))
    screen.blit(controls_bg, (WIDTH - 220, 10))
    
    # Draw controls text with better styling
    title = title_font.render("CONTROLS", True, YELLOW)
    left_text = controls_font.render("← : Move Left", True, WHITE)
    right_text = controls_font.render("→ : Move Right", True, WHITE)
    up_text = controls_font.render("↑ : Move Up", True, WHITE)
    down_text = controls_font.render("↓ : Move Down", True, WHITE)
    space_text = controls_font.render("SPACE : Shoot", True, WHITE)
    r_text = controls_font.render("R : Replay", True, WHITE)
    esc_text = controls_font.render("ESC : Menu", True, WHITE)
    
    screen.blit(title, (WIDTH - 190, 20))
    pygame.draw.line(screen, YELLOW, (WIDTH - 190, 50), (WIDTH - 40, 50), 2)
    
    screen.blit(left_text, (WIDTH - 190, 60))
    screen.blit(right_text, (WIDTH - 190, 85))
    screen.blit(up_text, (WIDTH - 190, 110))
    screen.blit(down_text, (WIDTH - 190, 135))
    screen.blit(space_text, (WIDTH - 190, 160))
    screen.blit(r_text, (WIDTH - 190, 185))
    screen.blit(esc_text, (WIDTH - 190, 210))

def game_over_text():
    # Create a semi-transparent background
    over_bg = pygame.Surface((400, 100), pygame.SRCALPHA)
    over_bg.fill((0, 0, 0, 200))
    screen.blit(over_bg, (WIDTH // 2 - 200, HEIGHT // 2 - 50))
    
    over_text = game_over_font.render("GAME OVER", True, RED)
    screen.blit(over_text, (WIDTH // 2 - 180, HEIGHT // 2 - 40))
    
    # Add instruction to return to menu or replay
    restart_text = controls_font.render("Press R to replay or ESC for menu", True, WHITE)
    screen.blit(restart_text, (WIDTH // 2 - 140, HEIGHT // 2 + 30))
    
    # Hide player ship when game is over
    # (The player ship will be hidden naturally since we don't draw it when game_is_over)

def player(x, y):
    screen.blit(player_img, (x, y))

def enemy(x, y, i):
    if enemy_alive[i]:
        screen.blit(enemy_img, (x, y))

def fire_bullet(x, y):
    global bullets
    # Add a new bullet to the list
    bullets.append([x + 20, y - 20])  # Adjust to fire from top of ship

def update_bullets():
    global bullets
    new_bullets = []
    
    # Update position of all bullets and draw them
    for bullet in bullets:
        bullet[1] -= bullet_dy  # Move bullet up
        if bullet[1] > 0:  # If bullet is still on screen
            screen.blit(bullet_img, (bullet[0], bullet[1]))
            new_bullets.append(bullet)
    
    bullets = new_bullets

def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt((enemy_x + 20 - bullet_x) ** 2 + (enemy_y + 20 - bullet_y) ** 2)
    return distance < 25

def update_explosions():
    # Update and draw all active explosions
    global explosions
    new_explosions = []
    
    for exp in explosions:
        x, y, frame_idx, timer = exp
        if frame_idx < len(explosion_frames):
            screen.blit(explosion_frames[frame_idx], (x, y))
            if timer <= 0:
                new_explosions.append([x, y, frame_idx + 1, 5])  # Next frame with 5 ticks delay
            else:
                new_explosions.append([x, y, frame_idx, timer - 1])
    
    explosions = new_explosions

def game_loop():
    global player_x, player_y, bullet_x, bullet_y, score_value, explosions, bullet_cooldown, bullets
    
    player_dx = 0  # Initialize player movement variable
    player_dy = 0  # Initialize vertical movement
    running = True
    return_to_menu = False
    clock = pygame.time.Clock()
    game_is_over = False
    
    # Reset game state
    score_value = 0
    explosions = []
    bullet_cooldown = 0
    bullets = []
    for i in range(num_of_enemies):
        enemy_alive[i] = True
        enemy_x[i] = random.randint(0, WIDTH - 40)
        enemy_y[i] = random.randint(50, 200)
    
    while running and not return_to_menu:
        # Draw background with stars
        screen.blit(background, (0, 0))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Player movement with keyboard
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player_dx = -player_speed
                if event.key == pygame.K_RIGHT:
                    player_dx = player_speed
                if event.key == pygame.K_UP:
                    player_dy = -player_speed
                if event.key == pygame.K_DOWN:
                    player_dy = player_speed
                if event.key == pygame.K_ESCAPE:
                    return_to_menu = True
                if event.key == pygame.K_r and game_is_over:
                    # Reset the game
                    return game_loop()
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player_dx < 0:
                    player_dx = 0
                if event.key == pygame.K_RIGHT and player_dx > 0:
                    player_dx = 0
                if event.key == pygame.K_UP and player_dy < 0:
                    player_dy = 0
                if event.key == pygame.K_DOWN and player_dy > 0:
                    player_dy = 0
        
        # Check for spacebar separately to allow simultaneous movement and shooting
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and not game_is_over:
            if bullet_cooldown <= 0 and len(bullets) < max_bullets:
                fire_bullet(player_x, player_y)
                bullet_cooldown = bullet_cooldown_max
        
        # Update bullet cooldown
        if bullet_cooldown > 0:
            bullet_cooldown -= 1
        
        # Player movement
        if not game_is_over:
            player_x += player_dx
            player_y += player_dy
        
        # Boundary check for player
        if player_x <= 0:
            player_x = 0
        elif player_x >= WIDTH - 50:
            player_x = WIDTH - 50
            
        # Boundary check for vertical movement
        if player_y <= 0:  # Allow player to go all the way to the top of the screen
            player_y = 0
        elif player_y >= HEIGHT - 60:  # Keep player from going off bottom
            player_y = HEIGHT - 60
        
        # Enemy movement
        all_enemies_dead = True
        for i in range(num_of_enemies):
            if enemy_alive[i]:
                all_enemies_dead = False
                
                # Game over condition
                if enemy_y[i] > HEIGHT - 150:
                    for j in range(num_of_enemies):
                        if enemy_alive[j]:
                            enemy_alive[j] = False
                            explosions.append([enemy_x[j], enemy_y[j], 0, 5])
                    game_is_over = True
                    break
                
                enemy_x[i] += enemy_dx[i]
                
                # Boundary check for enemies
                if enemy_x[i] <= 0:
                    enemy_dx[i] = abs(enemy_dx[i])
                    enemy_y[i] += enemy_dy[i]
                elif enemy_x[i] >= WIDTH - 40:
                    enemy_dx[i] = -abs(enemy_dx[i])
                    enemy_y[i] += enemy_dy[i]
                
                # Check collision with player ship
                if not game_is_over and is_player_collision(player_x, player_y, enemy_x[i], enemy_y[i]):
                    # Create explosion at player position
                    explosions.append([player_x, player_y, 0, 5])
                    game_is_over = True
                    break
                
                # Check collision with all bullets
                for bullet in bullets[:]:  # Use a copy for safe iteration
                    collision = is_collision(enemy_x[i], enemy_y[i], bullet[0], bullet[1])
                    if collision:
                        # Create explosion
                        explosions.append([enemy_x[i], enemy_y[i], 0, 5])
                        
                        # Remove bullet
                        if bullet in bullets:
                            bullets.remove(bullet)
                        
                        score_value += 1
                        enemy_alive[i] = False
                        break
                
                enemy(enemy_x[i], enemy_y[i], i)
        
        # Respawn enemies if all are dead
        if all_enemies_dead and not game_is_over:
            for i in range(num_of_enemies):
                enemy_alive[i] = True
                enemy_x[i] = random.randint(0, WIDTH - 40)
                enemy_y[i] = random.randint(50, 200)
                enemy_dx[i] = random.choice([-3, -2, 2, 3])
        
        # Update and draw bullets
        update_bullets()
        
        # Update and draw explosions
        update_explosions()
        
        # Draw player only if not game over
        if not game_is_over:
            player(player_x, player_y)
        
        # Show score
        show_score()
        
        # Show controls
        show_controls()
        
        # Show game over if needed
        if game_is_over:
            game_over_text()
        
        pygame.display.update()
        clock.tick(60)
    
    # We don't actually want to quit pygame here, just return to the main menu
    return

if __name__ == "__main__":
    game_loop()
def is_player_collision(player_x, player_y, enemy_x, enemy_y):
    # Check if player ship collides with enemy ship
    distance = math.sqrt((player_x + 25 - enemy_x - 20) ** 2 + (player_y + 25 - enemy_y - 20) ** 2)
    return distance < 35  # Slightly smaller than the sum of ship radii for better gameplay
