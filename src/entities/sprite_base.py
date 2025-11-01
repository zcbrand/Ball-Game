"""
Base sprite class for all game entities.

Provides common functionality for all game objects including
position tracking, update logic, and rendering.
"""

from abc import ABC, abstractmethod
import pygame
from typing import Tuple


class SpriteBase(ABC):
    """
    Abstract base class for all game sprites.

    All game entities (Player, Obstacles, etc.) should inherit from this class
    and implement the required abstract methods.
    """

    def __init__(self, x: float, y: float) -> None:
        """
        Initialize the sprite.

        Args:
            x: Initial x position
            y: Initial y position
        """
        self.position = pygame.Vector2(x, y)

    @abstractmethod
    def update(self, dt: float) -> None:
        """
        Update sprite logic.

        Args:
            dt: Delta time in seconds since last frame
        """
        pass

    @abstractmethod
    def draw(self, surface: pygame.Surface) -> None:
        """
        Draw the sprite to the screen.

        Args:
            surface: Pygame surface to draw on
        """
        pass

    @abstractmethod
    def get_rect(self) -> pygame.Rect:
        """
        Get the collision rectangle for this sprite.

        Returns:
            pygame.Rect representing the sprite's bounding box
        """
        pass
