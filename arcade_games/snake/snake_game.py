import pygame
import time
import random
import math
import os

pygame.init()

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
dark_green = (0, 100, 0)
blue = (50, 153, 213)
purple = (128, 0, 128)
dark_purple = (64, 0, 64)
brown = (165, 42, 42)

# Display dimensions
display_width = 800
display_height = 600

# Game window
game_display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Realistic Snake Game')

clock = pygame.time.Clock()

snake_block = 30  # Increased from 20 to 30
snake_speed = 10  # Reduced from 15 to 10 for slower gameplay

font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)
controls_font = pygame.font.SysFont("arial", 18)

# Create textures for background, snake, enemy, and food
def create_grass_texture():
    texture = pygame.Surface((display_width, display_height))
    texture.fill((50, 50, 50))  # Dark gray background
    
    # Add subtle texture
    for _ in range(300):
        x = random.randint(0, display_width - 10)
        y = random.randint(0, display_height - 10)
        size = random.randint(3, 8)
        shade = random.randint(40, 60)
        color = (shade, shade, shade)
        pygame.draw.circle(texture, color, (x, y), size)
    
    return texture

# Create snake textures
def create_snake_head_texture(color, dark_color):
    head = pygame.Surface((snake_block, snake_block), pygame.SRCALPHA)
    
    # Base color
    pygame.draw.rect(head, color, (0, 0, snake_block, snake_block))
    
    # Add some texture/pattern
    for i in range(0, snake_block, 4):
        pygame.draw.line(head, dark_color, (i, 0), (i, snake_block), 1)
    
    # Eyes - positioned at the front of the head (will be rotated based on direction)
    eye_size = snake_block // 5
    pygame.draw.circle(head, white, (3*snake_block//4, snake_block//3), eye_size)
    pygame.draw.circle(head, white, (3*snake_block//4, 2*snake_block//3), eye_size)
    
    # Pupils
    pupil_size = eye_size // 2
    pygame.draw.circle(head, black, (3*snake_block//4, snake_block//3), pupil_size)
    pygame.draw.circle(head, black, (3*snake_block//4, 2*snake_block//3), pupil_size)
    
    # Tongue
    pygame.draw.line(head, red, (snake_block, snake_block//2), (snake_block+5, snake_block//2), 2)
    pygame.draw.line(head, red, (snake_block+5, snake_block//2), (snake_block+8, snake_block//3), 2)
    pygame.draw.line(head, red, (snake_block+5, snake_block//2), (snake_block+8, 2*snake_block//3), 2)
    
    return head

def create_snake_body_texture(color, dark_color, is_corner=False):
    body = pygame.Surface((snake_block, snake_block), pygame.SRCALPHA)
    
    # Base color
    pygame.draw.rect(body, color, (0, 0, snake_block, snake_block))
    
    # Add some texture/pattern
    for i in range(0, snake_block, 4):
        pygame.draw.line(body, dark_color, (i, 0), (i, snake_block), 1)
    
    # Add a pattern to distinguish corners if needed
    if is_corner:
        pygame.draw.circle(body, dark_color, (snake_block//2, snake_block//2), snake_block//4)
    
    return body

def create_snake_tail_texture(color, dark_color):
    tail = pygame.Surface((snake_block, snake_block), pygame.SRCALPHA)
    
    # Base color
    pygame.draw.rect(tail, color, (0, 0, snake_block, snake_block))
    
    # Add some texture/pattern
    for i in range(0, snake_block, 4):
        pygame.draw.line(tail, dark_color, (i, 0), (i, snake_block), 1)
    
    # Make it pointy
    pygame.draw.polygon(tail, dark_color, [(snake_block//2, snake_block), 
                                          (0, snake_block//2), 
                                          (snake_block//2, 0), 
                                          (snake_block, snake_block//2)])
    
    return tail

def create_apple_texture():
    apple = pygame.Surface((snake_block, snake_block), pygame.SRCALPHA)
    
    # Apple body
    pygame.draw.circle(apple, red, (snake_block//2, snake_block//2), snake_block//2)
    
    # Highlight
    pygame.draw.circle(apple, (255, 150, 150), (snake_block//3, snake_block//3), snake_block//6)
    
    # Stem
    pygame.draw.rect(apple, brown, (snake_block//2 - 2, 0, 4, 5))
    
    # Leaf
    pygame.draw.polygon(apple, green, [(snake_block//2, 5), 
                                      (snake_block//2 + 8, 0), 
                                      (snake_block//2 + 4, 8)])
    
    return apple

# Create all textures
grass_texture = create_grass_texture()
snake_head_texture = create_snake_head_texture(green, dark_green)
snake_body_texture = create_snake_body_texture(green, dark_green)
snake_corner_texture = create_snake_body_texture(green, dark_green, True)
snake_tail_texture = create_snake_tail_texture(green, dark_green)

enemy_head_texture = create_snake_head_texture(purple, dark_purple)
enemy_body_texture = create_snake_body_texture(purple, dark_purple)
enemy_corner_texture = create_snake_body_texture(purple, dark_purple, True)
enemy_tail_texture = create_snake_tail_texture(purple, dark_purple)

apple_texture = create_apple_texture()

def your_score(score):
    value = score_font.render("Your Score: " + str(score), True, white)
    game_display.blit(value, [10, 10])

def get_segment_direction(current, next_segment):
    if next_segment[0] > current[0]:
        return "right"
    elif next_segment[0] < current[0]:
        return "left"
    elif next_segment[1] > current[1]:
        return "down"
    else:
        return "up"

def our_snake(snake_block, snake_list):
    if not snake_list:
        return
    
    # Draw head with proper rotation
    if len(snake_list) > 1:
        head_direction = get_segment_direction(snake_list[0], snake_list[1])
        rotated_head = pygame.transform.rotate(
            snake_head_texture,
            {"right": 0, "left": 180, "down": 270, "up": 90}[head_direction]
        )
    else:
        rotated_head = snake_head_texture
    
    game_display.blit(rotated_head, (snake_list[0][0], snake_list[0][1]))
    
    # Draw body segments
    for i in range(1, len(snake_list) - 1):
        prev_segment = snake_list[i-1]
        current = snake_list[i]
        next_segment = snake_list[i+1]
        
        # Determine if this is a corner piece
        prev_dir = get_segment_direction(current, prev_segment)
        next_dir = get_segment_direction(current, next_segment)
        
        if prev_dir != next_dir:  # It's a corner
            # Determine rotation for corner piece
            if (prev_dir == "up" and next_dir == "right") or (prev_dir == "left" and next_dir == "down"):
                rotation = 0
            elif (prev_dir == "right" and next_dir == "up") or (prev_dir == "down" and next_dir == "left"):
                rotation = 90
            elif (prev_dir == "down" and next_dir == "right") or (prev_dir == "left" and next_dir == "up"):
                rotation = 180
            else:
                rotation = 270
                
            rotated_segment = pygame.transform.rotate(snake_corner_texture, rotation)
        else:  # Straight piece
            if prev_dir in ["left", "right"]:
                rotation = 0
            else:
                rotation = 90
                
            rotated_segment = pygame.transform.rotate(snake_body_texture, rotation)
            
        game_display.blit(rotated_segment, (current[0], current[1]))
    
    # Draw tail if there's more than one segment
    if len(snake_list) > 1:
        tail = snake_list[-1]
        prev_to_tail = snake_list[-2]
        tail_direction = get_segment_direction(tail, prev_to_tail)
        
        rotated_tail = pygame.transform.rotate(
            snake_tail_texture,
            {"right": 0, "left": 180, "down": 90, "up": 270}[tail_direction]
        )
        
        game_display.blit(rotated_tail, (tail[0], tail[1]))

def enemy_snake(snake_block, enemy_list):
    if not enemy_list:
        return
    
    # Draw head with proper rotation
    if len(enemy_list) > 1:
        head_direction = get_segment_direction(enemy_list[0], enemy_list[1])
        rotated_head = pygame.transform.rotate(
            enemy_head_texture,
            {"right": 0, "left": 180, "down": 270, "up": 90}[head_direction]
        )
    else:
        rotated_head = enemy_head_texture
    
    game_display.blit(rotated_head, (enemy_list[0][0], enemy_list[0][1]))
    
    # Draw body segments
    for i in range(1, len(enemy_list) - 1):
        prev_segment = enemy_list[i-1]
        current = enemy_list[i]
        next_segment = enemy_list[i+1]
        
        # Determine if this is a corner piece
        prev_dir = get_segment_direction(current, prev_segment)
        next_dir = get_segment_direction(current, next_segment)
        
        if prev_dir != next_dir:  # It's a corner
            # Determine rotation for corner piece
            if (prev_dir == "up" and next_dir == "right") or (prev_dir == "left" and next_dir == "down"):
                rotation = 0
            elif (prev_dir == "right" and next_dir == "up") or (prev_dir == "down" and next_dir == "left"):
                rotation = 90
            elif (prev_dir == "down" and next_dir == "right") or (prev_dir == "left" and next_dir == "up"):
                rotation = 180
            else:
                rotation = 270
                
            rotated_segment = pygame.transform.rotate(enemy_corner_texture, rotation)
        else:  # Straight piece
            if prev_dir in ["left", "right"]:
                rotation = 0
            else:
                rotation = 90
                
            rotated_segment = pygame.transform.rotate(enemy_body_texture, rotation)
            
        game_display.blit(rotated_segment, (current[0], current[1]))
    
    # Draw tail if there's more than one segment
    if len(enemy_list) > 1:
        tail = enemy_list[-1]
        prev_to_tail = enemy_list[-2]
        tail_direction = get_segment_direction(tail, prev_to_tail)
        
        rotated_tail = pygame.transform.rotate(
            enemy_tail_texture,
            {"right": 0, "left": 180, "down": 90, "up": 270}[tail_direction]
        )
        
        game_display.blit(rotated_tail, (tail[0], tail[1]))

def message(msg, color):
    # Create a semi-transparent background for the message
    msg_bg = pygame.Surface((display_width * 2/3, 80), pygame.SRCALPHA)
    msg_bg.fill((0, 0, 0, 180))
    game_display.blit(msg_bg, [display_width / 6, display_height / 3 - 10])
    
    # Display the message
    mesg = font_style.render(msg, True, color)
    game_display.blit(mesg, [display_width / 6 + 20, display_height / 3])
    
    # Add ESC instruction
    esc_text = controls_font.render("Press ESC to return to main menu or R to replay", True, white)
    game_display.blit(esc_text, [display_width / 6 + 20, display_height / 3 + 40])

def show_controls():
    # Create a semi-transparent background for controls
    controls_bg = pygame.Surface((150, 200), pygame.SRCALPHA)
    controls_bg.fill((0, 0, 0, 150))
    game_display.blit(controls_bg, (display_width - 160, 40))
    
    controls = [
        "Controls:",
        "↑ Up",
        "↓ Down",
        "← Left",
        "→ Right",
        "ESC: Menu",
        "R: Replay"
    ]
    
    y_offset = 50
    for line in controls:
        control_text = controls_font.render(line, True, white)
        game_display.blit(control_text, [display_width - 150, y_offset])
        y_offset += 25

def game_loop():
    game_over = False
    game_close = False
    return_to_menu = False

    # Initial snake position
    x1 = display_width / 2
    y1 = display_height / 2

    # Change in position
    x1_change = 0
    y1_change = 0
    last_direction = "right"  # Default starting direction

    # Snake body
    snake_list = []
    length_of_snake = 1
    
    # Enemy snake
    enemy_snake_list = []
    enemy_length = 5
    enemy_x = round(random.randrange(0, display_width - snake_block) / snake_block) * snake_block
    enemy_y = round(random.randrange(0, display_height - snake_block) / snake_block) * snake_block
    
    # Initialize enemy snake body
    for i in range(enemy_length):
        enemy_snake_list.append([enemy_x - (i * snake_block), enemy_y])
    
    # Enemy movement direction (initially random)
    enemy_directions = ["up", "down", "left", "right"]
    enemy_direction = random.choice(enemy_directions)
    enemy_change_counter = 0

    # Food position
    foodx = round(random.randrange(0, display_width - snake_block) / snake_block) * snake_block
    foody = round(random.randrange(0, display_height - snake_block) / snake_block) * snake_block

    while not game_over and not return_to_menu:

        while game_close and not return_to_menu:
            game_display.blit(grass_texture, (0, 0))
            message("You Lost!", red)
            your_score(length_of_snake - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                    return_to_menu = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        return game_loop()
                    if event.key == pygame.K_ESCAPE:
                        return_to_menu = True
                        return  # Return to main menu

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                    last_direction = "left"
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                    last_direction = "right"
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                    last_direction = "up"
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0
                    last_direction = "down"
                elif event.key == pygame.K_ESCAPE:
                    return_to_menu = True
                    return  # Return to main menu

        # Check if snake hits the boundary - wrap around instead of ending game
        if x1 >= display_width:
            x1 = 0
        elif x1 < 0:
            x1 = display_width - snake_block
        
        if y1 >= display_height:
            y1 = 0
        elif y1 < 0:
            y1 = display_height - snake_block

        x1 += x1_change
        y1 += y1_change
        
        # Draw background
        game_display.blit(grass_texture, (0, 0))
        
        # Draw food (apple)
        game_display.blit(apple_texture, (foodx, foody))
        
        snake_head = []
        snake_head.append(x1)
        snake_head.append(y1)
        snake_list.append(snake_head)
        
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        # Check if snake hits itself - improved collision detection
        for segment in snake_list[:-1]:
            distance = math.sqrt((segment[0] - snake_head[0])**2 + (segment[1] - snake_head[1])**2)
            if distance < snake_block * 0.8:
                game_close = True
        
        # Move enemy snake
        enemy_change_counter += 1
        if enemy_change_counter > 15:  # Change direction occasionally
            enemy_direction = random.choice(enemy_directions)
            enemy_change_counter = 0
        
        # Get enemy head position
        enemy_head = enemy_snake_list[0].copy()
        
        # Move enemy based on direction
        if enemy_direction == "up":
            enemy_head[1] -= snake_block
        elif enemy_direction == "down":
            enemy_head[1] += snake_block
        elif enemy_direction == "left":
            enemy_head[0] -= snake_block
        elif enemy_direction == "right":
            enemy_head[0] += snake_block
        
        # Check if enemy would hit wall - wrap around instead of changing direction
        if enemy_head[0] >= display_width:
            enemy_head[0] = 0
        elif enemy_head[0] < 0:
            enemy_head[0] = display_width - snake_block
        
        if enemy_head[1] >= display_height:
            enemy_head[1] = 0
        elif enemy_head[1] < 0:
            enemy_head[1] = display_height - snake_block
        
        # Update enemy snake
        enemy_snake_list.insert(0, enemy_head)
        if len(enemy_snake_list) > enemy_length:
            enemy_snake_list.pop()
        
        # Check collision with enemy snake - improved collision detection
        for segment in enemy_snake_list:
            # Use distance-based collision detection instead of exact position matching
            distance = math.sqrt((segment[0] - x1)**2 + (segment[1] - y1)**2)
            if distance < snake_block * 0.8:  # Slightly smaller than block size for better feel
                game_close = True
        
        # Draw snakes
        our_snake(snake_block, snake_list)
        enemy_snake(snake_block, enemy_snake_list)
        
        # Show score and controls
        your_score(length_of_snake - 1)
        show_controls()

        pygame.display.update()

        # Check if snake eats food - improved collision detection
        distance_to_food = math.sqrt((x1 - foodx)**2 + (y1 - foody)**2)
        if distance_to_food < snake_block * 0.8:
            foodx = round(random.randrange(0, display_width - snake_block) / snake_block) * snake_block
            foody = round(random.randrange(0, display_height - snake_block) / snake_block) * snake_block
            length_of_snake += 1

        clock.tick(snake_speed)

    # Pygame quit at the end of the game loop
    # We don't actually want to quit pygame here, just return to the main menu
    # pygame.quit()
    # quit()
    return

if __name__ == "__main__":
    game_loop()
