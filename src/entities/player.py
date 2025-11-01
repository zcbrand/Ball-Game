"""
Player character class.

Represents the player-controlled ball with physics-based movement.
"""

import pygame
from src.entities.sprite_base import SpriteBase
from src.config import (
    PLAYER_RADIUS,
    PLAYER_START_X,
    PLAYER_START_Y,
    COLOR_PLAYER,
    JUMP_POWER
)


class Player(SpriteBase):
    """
    Player character - a ball that responds to gravity and jump input.

    The player continuously falls due to gravity and can jump when
    the user clicks/taps.
    """

    def __init__(self, x: float = PLAYER_START_X, y: float = PLAYER_START_Y) -> None:
        """
        Initialize the player.

        Args:
            x: Starting x position (defaults to config value)
            y: Starting y position (defaults to config value)
        """
        super().__init__(x, y)
        self.radius = PLAYER_RADIUS
        self.jump_power = 0.0
        self.is_jumping = False

    def jump(self) -> None:
        """
        Apply jump force to the player.

        Sets the jump power to the configured jump burst value,
        causing the player to move upward.
        """
        self.jump_power = JUMP_POWER
        self.is_jumping = True

    def update(self, dt: float) -> None:
        """
        Update player state.

        Note: Physics (gravity, jump) are applied by the PhysicsSystem.
        This method is for any player-specific update logic.

        Args:
            dt: Delta time in seconds since last frame
        """
        # Player physics are handled by PhysicsSystem
        # This is available for player-specific logic if needed
        pass

    def draw(self, surface: pygame.Surface) -> None:
        """
        Draw the player as a circle.

        Args:
            surface: Pygame surface to draw on
        """
        # Draw player as a filled circle
        pygame.draw.circle(
            surface,
            COLOR_PLAYER,
            (int(self.position.x), int(self.position.y)),
            self.radius
        )

        # Optional: Add a border for better visibility
        pygame.draw.circle(
            surface,
            (255, 255, 255),  # White border
            (int(self.position.x), int(self.position.y)),
            self.radius,
            2  # Border width
        )

    def get_rect(self) -> pygame.Rect:
        """
        Get collision rectangle for the player.

        Returns a square bounding box around the circular player
        for collision detection.

        Returns:
            pygame.Rect representing the player's bounding box
        """
        return pygame.Rect(
            self.position.x - self.radius,
            self.position.y - self.radius,
            self.radius * 2,
            self.radius * 2
        )

    def reset(self) -> None:
        """
        Reset player to starting position and state.

        Useful for restarting the game.
        """
        self.position.x = PLAYER_START_X
        self.position.y = PLAYER_START_Y
        self.jump_power = 0.0
        self.is_jumping = False
