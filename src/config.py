"""
Game configuration constants.

This module contains all constant values used throughout the game,
including screen settings, physics parameters, and gameplay constants.
"""

# Screen settings
SCREEN_WIDTH = 550
SCREEN_HEIGHT = 400
FPS = 60
WINDOW_TITLE = "Ball Game"

# Physics constants (converted from ActionScript frame-based to time-based)
GRAVITY = 10  # Pixels per frame (will be multiplied by dt * FPS for consistency)
JUMP_POWER = 25  # Initial jump velocity
JUMP_DECAY = 2  # Decay rate per frame

# Gameplay constants
OBSTACLE_SPEED = 10  # Pixels per frame
OBSTACLE_SPAWN_INTERVAL = 1500  # milliseconds
PIPE_GAP_MULTIPLIER = 4  # Times player height
GROUND_HEIGHT = 50  # Height of the ground bar

# Player settings
PLAYER_RADIUS = 20  # Player ball radius
PLAYER_START_X = 100  # Starting X position
PLAYER_START_Y = 200  # Starting Y position

# Obstacle settings
OBSTACLE_WIDTH = 80
OBSTACLE_MIN_HEIGHT = 50
OBSTACLE_START_X = 650  # Spawn position (off-screen right)

# Colors (RGB tuples)
COLOR_SKY = (135, 206, 235)  # Light blue
COLOR_GROUND = (34, 139, 34)  # Green
COLOR_PIPE = (50, 205, 50)  # Lime green
COLOR_PLAYER = (255, 215, 0)  # Gold
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_TEXT = (255, 255, 255)

# Font settings
FONT_SIZE_LARGE = 48
FONT_SIZE_MEDIUM = 32
FONT_SIZE_SMALL = 24
