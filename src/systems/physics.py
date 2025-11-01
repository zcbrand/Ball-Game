"""
Physics system for game entities.

Handles gravity, jumping, and boundary constraints for game objects.
Uses delta-time based physics for frame-rate independence.
"""

import pygame
from src.config import GRAVITY, JUMP_DECAY, FPS
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.entities.player import Player


class PhysicsSystem:
    """
    Physics engine for the game.

    Applies gravity, jump mechanics, and enforces world boundaries
    on game entities.
    """

    def __init__(self, ground_y: float) -> None:
        """
        Initialize the physics system.

        Args:
            ground_y: Y position of the ground (bottom boundary)
        """
        self.ground_y = ground_y

    def apply_gravity(self, player: 'Player', dt: float) -> None:
        """
        Apply gravity to the player.

        Only applies gravity if player is above ground.
        Uses delta-time for frame-rate independence while maintaining
        the feel of the original Flash game.

        Args:
            player: Player entity to apply gravity to
            dt: Delta time in seconds since last frame
        """
        if player.position.y < self.ground_y:
            # Convert frame-based gravity to time-based
            # Multiply by FPS to maintain original game feel
            player.position.y += GRAVITY * dt * FPS

    def apply_jump(self, player: 'Player', dt: float) -> None:
        """
        Apply jump force to the player.

        The jump power decays over time, creating an arc trajectory.

        Args:
            player: Player entity to apply jump to
            dt: Delta time in seconds since last frame
        """
        if player.is_jumping and player.jump_power > 0:
            # Move player upward by jump power
            player.position.y -= player.jump_power * dt * FPS

            # Decay jump power to create arc
            player.jump_power -= JUMP_DECAY

    def clamp_to_ground(self, player: 'Player') -> None:
        """
        Prevent player from falling through the ground.

        When player reaches or passes the ground, snap to ground position
        and disable jumping state.

        Args:
            player: Player entity to constrain
        """
        if player.position.y >= self.ground_y:
            player.position.y = self.ground_y
            player.is_jumping = False
            player.jump_power = 0

    def clamp_to_ceiling(self, player: 'Player', ceiling_y: float = 0) -> None:
        """
        Prevent player from going above the ceiling.

        When player hits the ceiling, cancel upward momentum.

        Args:
            player: Player entity to constrain
            ceiling_y: Y position of the ceiling (top boundary, default 0)
        """
        if player.position.y - player.radius <= ceiling_y:
            player.position.y = ceiling_y + player.radius
            player.jump_power = 0

    def update(self, player: 'Player', dt: float) -> None:
        """
        Apply all physics to the player.

        Convenience method that applies gravity, jump, and constraints
        in the correct order.

        Args:
            player: Player entity to update
            dt: Delta time in seconds since last frame
        """
        # Apply forces
        self.apply_gravity(player, dt)
        self.apply_jump(player, dt)

        # Enforce boundaries
        self.clamp_to_ceiling(player)
        self.clamp_to_ground(player)
