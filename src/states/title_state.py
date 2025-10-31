"""
Title screen state.

Displays the game title and a "Click to Play" message.
For Phase 1, this is a simple placeholder to test the state system.
"""

import pygame
from src.states.state_base import State
from src.config import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    COLOR_SKY, COLOR_WHITE, COLOR_BLACK,
    FONT_SIZE_LARGE, FONT_SIZE_MEDIUM
)


class TitleState(State):
    """
    Title screen state.

    Displays the game title and waits for user input to start the game.
    """

    def __init__(self, state_manager: 'StateManager') -> None:
        """
        Initialize the title state.

        Args:
            state_manager: Reference to the state manager
        """
        super().__init__(state_manager)

        # Initialize fonts (will be created on_enter to ensure pygame is initialized)
        self.title_font: Optional[pygame.font.Font] = None
        self.subtitle_font: Optional[pygame.font.Font] = None

    def on_enter(self) -> None:
        """Called when entering the title state."""
        # Create fonts
        self.title_font = pygame.font.Font(None, FONT_SIZE_LARGE)
        self.subtitle_font = pygame.font.Font(None, FONT_SIZE_MEDIUM)

    def handle_events(self, events: list[pygame.event.Event]) -> None:
        """
        Handle input events.

        Args:
            events: List of pygame events to process
        """
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                # TODO: Change to 'playing' state in Phase 2
                # For Phase 1, just acknowledge the click
                print("Click detected - game would start (Phase 2)")

    def update(self, dt: float) -> None:
        """
        Update title state logic.

        Args:
            dt: Delta time in seconds since last frame
        """
        # No logic needed for static title screen
        pass

    def draw(self, surface: pygame.Surface) -> None:
        """
        Draw the title screen.

        Args:
            surface: Pygame surface to draw on
        """
        # Clear screen with sky color
        surface.fill(COLOR_SKY)

        # Render title
        title_text = self.title_font.render("BALL GAME", True, COLOR_WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))

        # Add shadow for title
        title_shadow = self.title_font.render("BALL GAME", True, COLOR_BLACK)
        shadow_rect = title_shadow.get_rect(center=(SCREEN_WIDTH // 2 + 2, SCREEN_HEIGHT // 3 + 2))
        surface.blit(title_shadow, shadow_rect)
        surface.blit(title_text, title_rect)

        # Render subtitle
        subtitle_text = self.subtitle_font.render("Click to Play", True, COLOR_WHITE)
        subtitle_rect = subtitle_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 2 // 3))

        # Add shadow for subtitle
        subtitle_shadow = self.subtitle_font.render("Click to Play", True, COLOR_BLACK)
        subtitle_shadow_rect = subtitle_shadow.get_rect(center=(SCREEN_WIDTH // 2 + 2, SCREEN_HEIGHT * 2 // 3 + 2))
        surface.blit(subtitle_shadow, subtitle_shadow_rect)
        surface.blit(subtitle_text, subtitle_rect)
