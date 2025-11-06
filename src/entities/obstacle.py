"""
Obstacle class for pipe obstacles.

Represents a single pipe obstacle that scrolls across the screen.
"""

import pygame
from src.entities.sprite_base import SpriteBase
from src.config import (
    OBSTACLE_WIDTH,
    OBSTACLE_MIN_HEIGHT,
    OBSTACLE_SPEED,
    COLOR_PIPE,
    SCREEN_HEIGHT,
    GROUND_HEIGHT,
    FPS
)


class Obstacle(SpriteBase):
    """
    Pipe obstacle that scrolls horizontally.

    Can be either a top pipe (hangs from ceiling) or bottom pipe
    (rises from ground).
    """

    def __init__(self, x: float, y: float, height: float, is_top: bool = False) -> None:
        """
        Initialize an obstacle.

        Args:
            x: Starting x position
            y: Y position (top of pipe for bottom pipes, bottom of pipe for top pipes)
            height: Height of the pipe
            is_top: True if this is a top pipe (hangs from ceiling)
        """
        super().__init__(x, y)
        self.width = OBSTACLE_WIDTH
        self.height = height
        self.is_top = is_top

        # Adjust position based on pipe orientation
        if is_top:
            # For top pipes, y is the bottom edge
            # Position stores top-left, so subtract height
            self.position.y = y - height

    def update(self, dt: float) -> None:
        """
        Update obstacle position (scroll left).

        Args:
            dt: Delta time in seconds since last frame
        """
        # Scroll left at constant speed
        self.position.x -= OBSTACLE_SPEED * dt * FPS

    def draw(self, surface: pygame.Surface) -> None:
        """
        Draw the pipe obstacle.

        Args:
            surface: Pygame surface to draw on
        """
        # Draw main pipe body
        pipe_rect = pygame.Rect(
            int(self.position.x),
            int(self.position.y),
            self.width,
            int(self.height)
        )
        pygame.draw.rect(surface, COLOR_PIPE, pipe_rect)

        # Draw pipe border for depth
        border_color = (40, 165, 40)  # Darker green
        pygame.draw.rect(surface, border_color, pipe_rect, 3)

        # Draw pipe cap (the wider part at the opening)
        cap_width = self.width + 8
        cap_height = 30

        if self.is_top:
            # Cap at bottom for top pipes
            cap_rect = pygame.Rect(
                int(self.position.x - 4),
                int(self.position.y + self.height - cap_height),
                cap_width,
                cap_height
            )
        else:
            # Cap at top for bottom pipes
            cap_rect = pygame.Rect(
                int(self.position.x - 4),
                int(self.position.y),
                cap_width,
                cap_height
            )

        pygame.draw.rect(surface, COLOR_PIPE, cap_rect)
        pygame.draw.rect(surface, border_color, cap_rect, 3)

    def get_rect(self) -> pygame.Rect:
        """
        Get collision rectangle for the pipe.

        Returns:
            pygame.Rect representing the pipe's bounding box
        """
        return pygame.Rect(
            int(self.position.x),
            int(self.position.y),
            self.width,
            int(self.height)
        )

    def is_offscreen(self) -> bool:
        """
        Check if obstacle is completely off the left side of screen.

        Returns:
            True if obstacle is off-screen and can be removed
        """
        return self.position.x + self.width < 0


class ScoreCheckpoint(SpriteBase):
    """
    Invisible checkpoint between pipe pairs for scoring.

    When player passes through this, score increments.
    """

    def __init__(self, x: float) -> None:
        """
        Initialize score checkpoint.

        Args:
            x: X position (between pipe pair)
        """
        super().__init__(x, 0)
        self.width = 5
        self.height = SCREEN_HEIGHT - GROUND_HEIGHT
        self.scored = False  # Track if already scored

    def update(self, dt: float) -> None:
        """
        Update checkpoint position (scroll left).

        Args:
            dt: Delta time in seconds since last frame
        """
        self.position.x -= OBSTACLE_SPEED * dt * FPS

    def draw(self, surface: pygame.Surface) -> None:
        """
        Draw checkpoint (invisible in normal gameplay).

        Args:
            surface: Pygame surface to draw on
        """
        # Normally invisible
        # Uncomment for debugging:
        # debug_rect = self.get_rect()
        # pygame.draw.rect(surface, (255, 0, 0, 128), debug_rect, 1)
        pass

    def get_rect(self) -> pygame.Rect:
        """
        Get collision rectangle for score checking.

        Returns:
            pygame.Rect representing the checkpoint area
        """
        return pygame.Rect(
            int(self.position.x),
            0,
            self.width,
            self.height
        )

    def is_offscreen(self) -> bool:
        """
        Check if checkpoint is off-screen.

        Returns:
            True if checkpoint is off-screen
        """
        return self.position.x + self.width < 0
