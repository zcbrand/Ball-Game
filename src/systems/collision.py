"""
Collision detection system.

Handles all collision detection between game entities including
player-obstacle collisions and boundary collisions.
"""

import pygame
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from src.entities.player import Player
    from src.entities.obstacle import Obstacle


class CollisionSystem:
    """
    Collision detection system.

    Detects collisions between the player and obstacles,
    as well as boundary collisions (ceiling and ground).
    """

    def __init__(self, ceiling_y: float = 0, ground_y: float = 400) -> None:
        """
        Initialize the collision system.

        Args:
            ceiling_y: Y position of the ceiling (top boundary)
            ground_y: Y position of the ground (bottom boundary)
        """
        self.ceiling_y = ceiling_y
        self.ground_y = ground_y

    def check_obstacle_collision(self, player: 'Player', obstacles: List['Obstacle']) -> bool:
        """
        Check if player collides with any obstacle.

        Args:
            player: Player entity to check
            obstacles: List of obstacles to check against

        Returns:
            True if collision detected, False otherwise
        """
        player_rect = player.get_rect()

        for obstacle in obstacles:
            obstacle_rect = obstacle.get_rect()

            if player_rect.colliderect(obstacle_rect):
                return True

        return False

    def check_boundary_collision(self, player: 'Player') -> bool:
        """
        Check if player collides with ceiling or ground boundaries.

        Args:
            player: Player entity to check

        Returns:
            True if collision detected, False otherwise
        """
        # Check ceiling collision
        if player.position.y - player.radius <= self.ceiling_y:
            return True

        # Check ground collision
        if player.position.y + player.radius >= self.ground_y:
            return True

        return False

    def check_all_collisions(self, player: 'Player', obstacles: List['Obstacle']) -> bool:
        """
        Check all collision types for the player.

        Convenience method that checks both obstacle and boundary collisions.

        Args:
            player: Player entity to check
            obstacles: List of obstacles to check against

        Returns:
            True if any collision detected, False otherwise
        """
        # Check obstacle collisions
        if self.check_obstacle_collision(player, obstacles):
            return True

        # Check boundary collisions
        if self.check_boundary_collision(player):
            return True

        return False
