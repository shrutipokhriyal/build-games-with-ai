# Arcade Games Collection

A collection of classic arcade games built with Python and Pygame.

## Games Included

1. **Snake Game** - A classic snake game with realistic graphics and screen wrapping
2. **Pong Game** - A classic pong game with 3-consecutive-misses rule
3. **Space Invaders** - A space shooter game with full directional movement

## Project Structure

```
arcade_games/
├── run_arcade.py        # Main launcher script
├── main_menu.py         # Main menu interface
├── snake/               # Snake game folder
│   ├── __init__.py      # Makes the directory a Python package
│   └── snake_game.py    # Snake game implementation
├── pong/                # Pong game folder
│   ├── __init__.py      # Makes the directory a Python package
│   └── pong_game.py     # Pong game implementation
├── space_invaders/      # Space Invaders game folder
│   ├── __init__.py      # Makes the directory a Python package
│   └── space_invaders.py # Space Invaders game implementation
└── venv/                # Python virtual environment
```

## Controls

### Common Controls
- **ESC**: Return to main menu
- **R**: Replay game (when game over)

### Snake Game
- **Arrow Keys**: Control snake direction

### Pong Game
- **Up/Down Arrow Keys**: Move paddle up/down

### Space Invaders
- **Arrow Keys**: Move spaceship
- **Space**: Shoot

## Requirements

- Python 3.x
- Pygame

## Installation

1. Clone this repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`
4. Install dependencies: `pip install pygame`
5. Run the game: `python run_arcade.py`

## Features

### Snake Game
- Realistic snake graphics with proper head, body, and tail
- Screen wrapping (snake appears on opposite side when it reaches the edge)
- Enemy snake with AI movement
- Collision detection

### Pong Game
- Single player against AI
- 3-consecutive-misses rule (game ends after 3 consecutive misses)
- Score tracking
- Visual effects

### Space Invaders
- Full directional movement (up, down, left, right)
- Multiple bullets system
- Enemy ships with movement patterns
- Collision detection
- Explosion animations

# This Game Collection has been created with Amazaon Q CLI, including this readme file.