import pygame
import sys
import os
import importlib

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
BLUE = (50, 153, 213)
PURPLE = (128, 0, 128)
YELLOW = (255, 255, 0)

# Create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Arcade Games Collection")

# Fonts
title_font = pygame.font.SysFont("comicsansms", 60)
menu_font = pygame.font.SysFont("arial", 40)
info_font = pygame.font.SysFont("arial", 20)

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
        
    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, WHITE, self.rect, 3, border_radius=10)
        
        text_surf = menu_font.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
        
    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        
    def is_clicked(self, mouse_pos, mouse_click):
        return self.rect.collidepoint(mouse_pos) and mouse_click

def draw_title():
    title_surf = title_font.render("ARCADE GAMES", True, YELLOW)
    title_rect = title_surf.get_rect(center=(WIDTH//2, 100))
    screen.blit(title_surf, title_rect)
    
    subtitle_surf = menu_font.render("Select a game to play", True, WHITE)
    subtitle_rect = subtitle_surf.get_rect(center=(WIDTH//2, 160))
    screen.blit(subtitle_surf, subtitle_rect)

def draw_info():
    info_text = "Press ESC during any game to return to this menu"
    info_surf = info_font.render(info_text, True, WHITE)
    info_rect = info_surf.get_rect(center=(WIDTH//2, HEIGHT-20))
    screen.blit(info_surf, info_rect)

def main_menu():
    global screen
    
    # Ensure we have a valid display
    if pygame.display.get_surface() is None:
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Arcade Games Collection")
    
    # Create game buttons
    snake_button = Button(WIDTH//2-150, 220, 300, 70, "Snake Game", GREEN, (0, 200, 0))
    pong_button = Button(WIDTH//2-150, 320, 300, 70, "Pong Game", BLUE, (0, 100, 200))
    space_button = Button(WIDTH//2-150, 420, 300, 70, "Space Invaders", RED, (200, 0, 0))
    quit_button = Button(WIDTH//2-100, 500, 200, 50, "Quit", PURPLE, (100, 0, 100))
    
    buttons = [snake_button, pong_button, space_button, quit_button]
    
    clock = pygame.time.Clock()
    running = True
    
    while running:
        screen.fill(BLACK)
        
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    mouse_click = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        
        # Draw title and info
        draw_title()
        draw_info()
        
        # Draw and check buttons
        for button in buttons:
            button.check_hover(mouse_pos)
            button.draw(screen)
            
            if button.is_clicked(mouse_pos, mouse_click):
                if button == snake_button:
                    run_game("snake.snake_game")
                elif button == pong_button:
                    run_game("pong.pong_game")
                elif button == space_button:
                    run_game("space_invaders.space_invaders")
                elif button == quit_button:
                    pygame.quit()
                    sys.exit()
        
        pygame.display.update()
        clock.tick(60)

def run_game(game_module):
    # Import the game module dynamically
    try:
        # First, try to import the module
        game = importlib.import_module(game_module)
        
        # Run the game's game_loop function
        if hasattr(game, 'game_loop'):
            game.game_loop()
            # After the game loop ends, reinitialize the display for the main menu
            global screen
            screen = pygame.display.set_mode((WIDTH, HEIGHT))
            pygame.display.set_caption("Arcade Games Collection")
        else:
            print(f"Error: {game_module} does not have a game_loop function")
    except ImportError:
        print(f"Error: Could not import {game_module}")
    except Exception as e:
        print(f"Error running {game_module}: {e}")

if __name__ == "__main__":
    main_menu()
