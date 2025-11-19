"""
Game over state.

Displays the final score and allows the player to restart.
"""

import pygame
from typing import Optional
from src.states.state_base import State
from src.config import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    COLOR_SKY, COLOR_WHITE, COLOR_BLACK, COLOR_GROUND,
    FONT_SIZE_LARGE, FONT_SIZE_MEDIUM, FONT_SIZE_SMALL,
    GROUND_HEIGHT
)


class GameOverState(State):
    """
    Game over state.

    Displays game over message, final score, and restart instructions.
    """

    def __init__(self, state_manager: 'StateManager') -> None:
        """
        Initialize the game over state.

        Args:
            state_manager: Reference to the state manager
        """
        super().__init__(state_manager)

        # Fonts (will be created on_enter to ensure pygame is initialized)
        self.title_font: Optional[pygame.font.Font] = None
        self.score_font: Optional[pygame.font.Font] = None
        self.subtitle_font: Optional[pygame.font.Font] = None

        # Final score (set when entering state)
        self.final_score: int = 0

    def set_score(self, score: int) -> None:
        """
        Set the final score to display.

        Args:
            score: Final score achieved
        """
        self.final_score = score

    def on_enter(self) -> None:
        """Called when entering the game over state."""
        # Create fonts
        self.title_font = pygame.font.Font(None, FONT_SIZE_LARGE)
        self.score_font = pygame.font.Font(None, FONT_SIZE_MEDIUM)
        self.subtitle_font = pygame.font.Font(None, FONT_SIZE_SMALL)

    def handle_events(self, events: list[pygame.event.Event]) -> None:
        """
        Handle input events.

        Args:
            events: List of pygame events to process
        """
        for event in events:
            # Restart on mouse click or spacebar
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.change_state('title')
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    self.change_state('title')

    def update(self, dt: float) -> None:
        """
        Update game over state logic.

        Args:
            dt: Delta time in seconds since last frame
        """
        # No logic needed for static game over screen
        pass

    def draw(self, surface: pygame.Surface) -> None:
        """
        Draw the game over screen.

        Args:
            surface: Pygame surface to draw on
        """
        # Clear screen with sky color
        surface.fill(COLOR_SKY)

        # Draw ground for consistency
        self._draw_ground(surface)

        # Render "GAME OVER" title
        title_text = self.title_font.render("GAME OVER", True, COLOR_WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))

        # Add shadow for title
        title_shadow = self.title_font.render("GAME OVER", True, COLOR_BLACK)
        shadow_rect = title_shadow.get_rect(center=(SCREEN_WIDTH // 2 + 2, SCREEN_HEIGHT // 3 + 2))
        surface.blit(title_shadow, shadow_rect)
        surface.blit(title_text, title_rect)

        # Render final score
        score_text = self.score_font.render(f"Score: {self.final_score}", True, COLOR_WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

        # Add shadow for score
        score_shadow = self.score_font.render(f"Score: {self.final_score}", True, COLOR_BLACK)
        score_shadow_rect = score_shadow.get_rect(center=(SCREEN_WIDTH // 2 + 2, SCREEN_HEIGHT // 2 + 2))
        surface.blit(score_shadow, score_shadow_rect)
        surface.blit(score_text, score_rect)

        # Render restart instructions
        restart_text = self.subtitle_font.render("Click or Press Space to Restart", True, COLOR_WHITE)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 2 // 3))

        # Add shadow for restart text
        restart_shadow = self.subtitle_font.render("Click or Press Space to Restart", True, COLOR_BLACK)
        restart_shadow_rect = restart_shadow.get_rect(center=(SCREEN_WIDTH // 2 + 2, SCREEN_HEIGHT * 2 // 3 + 2))
        surface.blit(restart_shadow, restart_shadow_rect)
        surface.blit(restart_text, restart_rect)

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

    def on_exit(self) -> None:
        """Called when exiting the game over state."""
        # Reset final score
        self.final_score = 0
