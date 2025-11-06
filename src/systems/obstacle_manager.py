"""
Obstacle manager for spawning and managing pipe obstacles.

Handles timer-based spawning, randomized positions, and cleanup.
"""

import random
from typing import List
import pygame
from src.entities import Obstacle, ScoreCheckpoint
from src.config import (
    OBSTACLE_SPAWN_INTERVAL,
    OBSTACLE_START_X,
    SCREEN_HEIGHT,
    GROUND_HEIGHT,
    PLAYER_RADIUS,
    PIPE_GAP_MULTIPLIER,
    OBSTACLE_MIN_HEIGHT
)


class ObstacleManager:
    """
    Manages obstacle spawning, movement, and removal.

    Spawns pipe pairs at regular intervals with randomized gaps,
    handles scrolling movement, and removes off-screen obstacles.
    """

    def __init__(self) -> None:
        """Initialize the obstacle manager."""
        self.obstacles: List[Obstacle] = []
        self.checkpoints: List[ScoreCheckpoint] = []
        self.spawn_timer = 0.0
        self.spawn_interval = OBSTACLE_SPAWN_INTERVAL / 1000.0  # Convert ms to seconds

    def update(self, dt: float) -> int:
        """
        Update all obstacles and spawn timer.

        Args:
            dt: Delta time in seconds since last frame

        Returns:
            Number of points scored this frame
        """
        score_gained = 0

        # Update spawn timer
        self.spawn_timer += dt

        # Spawn new obstacle if timer expired
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_obstacle_pair()
            self.spawn_timer = 0.0

        # Update all obstacles
        for obstacle in self.obstacles:
            obstacle.update(dt)

        # Update all checkpoints
        for checkpoint in self.checkpoints:
            checkpoint.update(dt)

        # Remove off-screen obstacles
        self._cleanup_offscreen()

        return score_gained

    def spawn_obstacle_pair(self) -> None:
        """
        Spawn a pair of pipes (top and bottom) with a gap between them.

        Uses randomization similar to the original Flash game.
        """
        # Calculate safe spawn area
        # minNum: Minimum Y for bottom pipe (must leave gap at top)
        # maxNum: Maximum Y for bottom pipe (must leave gap at bottom)
        player_height = PLAYER_RADIUS * 2
        gap_size = player_height * PIPE_GAP_MULTIPLIER

        # Calculate bounds
        min_y = 0 + player_height * 4.5  # Leave space at top
        max_y = (SCREEN_HEIGHT - GROUND_HEIGHT) - player_height * 3  # Leave space at bottom

        # Random Y position for bottom pipe opening
        bottom_pipe_top_y = random.uniform(min_y, max_y)

        # Top pipe: hangs from ceiling to gap
        top_pipe_height = bottom_pipe_top_y - gap_size
        top_pipe_bottom_y = bottom_pipe_top_y - gap_size

        # Bottom pipe: rises from ground to gap
        bottom_pipe_height = (SCREEN_HEIGHT - GROUND_HEIGHT) - bottom_pipe_top_y

        # Create pipes only if they have valid heights
        if top_pipe_height > OBSTACLE_MIN_HEIGHT:
            top_pipe = Obstacle(
                x=OBSTACLE_START_X,
                y=top_pipe_bottom_y,
                height=top_pipe_height,
                is_top=True
            )
            self.obstacles.append(top_pipe)

        if bottom_pipe_height > OBSTACLE_MIN_HEIGHT:
            bottom_pipe = Obstacle(
                x=OBSTACLE_START_X,
                y=bottom_pipe_top_y,
                height=bottom_pipe_height,
                is_top=False
            )
            self.obstacles.append(bottom_pipe)

        # Create score checkpoint between the pipes
        checkpoint = ScoreCheckpoint(x=OBSTACLE_START_X)
        self.checkpoints.append(checkpoint)

    def _cleanup_offscreen(self) -> None:
        """Remove obstacles and checkpoints that are off-screen."""
        # Remove off-screen obstacles
        self.obstacles = [obs for obs in self.obstacles if not obs.is_offscreen()]

        # Remove off-screen checkpoints
        self.checkpoints = [cp for cp in self.checkpoints if not cp.is_offscreen()]

    def check_score(self, player_rect: pygame.Rect) -> int:
        """
        Check if player passed through any checkpoints.

        Args:
            player_rect: Player's collision rectangle

        Returns:
            Number of points scored (0 or 1)
        """
        score_gained = 0

        for checkpoint in self.checkpoints:
            if not checkpoint.scored:
                if player_rect.colliderect(checkpoint.get_rect()):
                    checkpoint.scored = True
                    score_gained += 1

        return score_gained

    def draw(self, surface: pygame.Surface) -> None:
        """
        Draw all obstacles and checkpoints.

        Args:
            surface: Pygame surface to draw on
        """
        # Draw checkpoints (usually invisible)
        for checkpoint in self.checkpoints:
            checkpoint.draw(surface)

        # Draw obstacles
        for obstacle in self.obstacles:
            obstacle.draw(surface)

    def reset(self) -> None:
        """Reset obstacle manager (clear all obstacles)."""
        self.obstacles.clear()
        self.checkpoints.clear()
        self.spawn_timer = 0.0

    def get_obstacles(self) -> List[Obstacle]:
        """
        Get list of all active obstacles.

        Returns:
            List of Obstacle objects
        """
        return self.obstacles
