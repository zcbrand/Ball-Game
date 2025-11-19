"""
Play state - active gameplay.

Handles the main game loop where the player controls the ball,
avoiding obstacles and scoring points.
"""

import pygame
from src.states.state_base import State
from src.entities import Player
from src.systems import PhysicsSystem, ObstacleManager, CollisionSystem
from src.config import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    COLOR_SKY, COLOR_GROUND, COLOR_WHITE, COLOR_BLACK,
    GROUND_HEIGHT, FONT_SIZE_SMALL
)


class PlayState(State):
    """
    Active gameplay state.

    Manages the player, physics, obstacles (Phase 3), and scoring.
    Handles input for jumping and game logic.
    """

    def __init__(self, state_manager: 'StateManager') -> None:
        """
        Initialize the play state.

        Args:
            state_manager: Reference to the state manager
        """
        super().__init__(state_manager)

        # Will be initialized in on_enter
        self.player: Player = None
        self.physics: PhysicsSystem = None
        self.obstacle_manager: ObstacleManager = None
        self.collision: CollisionSystem = None
        self.ground_y: float = 0
        self.score: int = 0
        self.font: pygame.font.Font = None

    def on_enter(self) -> None:
        """Called when entering the play state."""
        # Calculate ground position
        # Ground is at bottom of screen minus ground height minus player radius
        self.ground_y = SCREEN_HEIGHT - GROUND_HEIGHT - 20  # 20 = player radius

        # Create player
        self.player = Player()

        # Create physics system
        self.physics = PhysicsSystem(self.ground_y)

        # Create obstacle manager
        self.obstacle_manager = ObstacleManager()

        # Create collision system
        self.collision = CollisionSystem(ceiling_y=0, ground_y=self.ground_y + 20)

        # Initialize score
        self.score = 0

        # Create font for score display
        self.font = pygame.font.Font(None, FONT_SIZE_SMALL)

        # Start player in jumping state so they fall at start
        self.player.is_jumping = True

    def handle_events(self, events: list[pygame.event.Event]) -> None:
        """
        Handle input events during gameplay.

        Args:
            events: List of pygame events to process
        """
        for event in events:
            # Jump on mouse click or spacebar
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.player.jump()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.jump()

    def update(self, dt: float) -> None:
        """
        Update gameplay logic.

        Args:
            dt: Delta time in seconds since last frame
        """
        # Update player with physics
        self.physics.update(self.player, dt)

        # Update obstacles (spawning, movement, cleanup)
        self.obstacle_manager.update(dt)

        # Check if player passed through checkpoint (score)
        score_gained = self.obstacle_manager.check_score(self.player.get_rect())
        self.score += score_gained

        # Check for collisions (obstacles and boundaries)
        obstacles = self.obstacle_manager.get_obstacles()
        if self.collision.check_all_collisions(self.player, obstacles):
            self._game_over()

    def _game_over(self) -> None:
        """Handle game over - transition to game over state."""
        # Get game over state and set the final score
        gameover_state = self.state_manager.states.get('gameover')
        if gameover_state:
            gameover_state.set_score(self.score)

        # Transition to game over state
        self.change_state('gameover')

    def draw(self, surface: pygame.Surface) -> None:
        """
        Draw the game world.

        Args:
            surface: Pygame surface to draw on
        """
        # Clear screen with sky color
        surface.fill(COLOR_SKY)

        # Draw ground
        self._draw_ground(surface)

        # Draw obstacles
        self.obstacle_manager.draw(surface)

        # Draw player (on top of obstacles for visibility)
        self.player.draw(surface)

        # Draw score (on top of everything)
        self._draw_score(surface)

    def _draw_ground(self, surface: pygame.Surface) -> None:
        """
        Draw the ground at the bottom of the screen.

        Args:
            surface: Pygame surface to draw on
        """
        ground_rect = pygame.Rect(
            0,
            SCREEN_HEIGHT - GROUND_HEIGHT,
            SCREEN_WIDTH,
            GROUND_HEIGHT
        )
        pygame.draw.rect(surface, COLOR_GROUND, ground_rect)

    def _draw_score(self, surface: pygame.Surface) -> None:
        """
        Draw the current score.

        Args:
            surface: Pygame surface to draw on
        """
        # Render score text
        score_text = self.font.render(f"Score: {self.score}", True, COLOR_WHITE)
        score_rect = score_text.get_rect(topleft=(10, 10))

        # Add shadow for visibility
        score_shadow = self.font.render(f"Score: {self.score}", True, COLOR_BLACK)
        shadow_rect = score_shadow.get_rect(topleft=(11, 11))

        surface.blit(score_shadow, shadow_rect)
        surface.blit(score_text, score_rect)

    def on_exit(self) -> None:
        """Called when exiting the play state."""
        # Clean up resources if needed
        pass
