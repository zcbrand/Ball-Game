"""
Main game class.

This module contains the core Game class that manages the main game loop,
including initialization, event handling, updates, and rendering.
"""

import pygame
import sys
from src.config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, WINDOW_TITLE
from src.states import StateManager, TitleState, PlayState


class Game:
    """
    Main game class.

    Handles pygame initialization, the main game loop, and coordinates
    between different game states through the StateManager.
    """

    def __init__(self) -> None:
        """Initialize the game."""
        # Initialize pygame
        pygame.init()

        # Create display
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(WINDOW_TITLE)

        # Create clock for framerate control
        self.clock = pygame.time.Clock()

        # Initialize state manager
        self.state_manager = StateManager()

        # Create and add states
        self._setup_states()

        # Game running flag
        self.running = True

    def _setup_states(self) -> None:
        """Set up all game states."""
        # Create states
        title_state = TitleState(self.state_manager)
        play_state = PlayState(self.state_manager)

        # Add states to manager
        self.state_manager.add_state('title', title_state)
        self.state_manager.add_state('play', play_state)

        # Set initial state
        self.state_manager.change_state('title')

    def run(self) -> None:
        """
        Main game loop.

        Runs the game loop at target FPS, handling events, updating game logic,
        and rendering to the screen.
        """
        while self.running:
            # Calculate delta time in seconds
            dt = self.clock.tick(FPS) / 1000.0

            # Handle events
            self._handle_events()

            # Update game state
            self._update(dt)

            # Draw everything
            self._draw()

            # Update display
            pygame.display.flip()

        # Clean up
        self._quit()

    def _handle_events(self) -> None:
        """Process pygame events."""
        events = pygame.event.get()

        for event in events:
            # Handle quit event
            if event.type == pygame.QUIT:
                self.running = False
            # Handle escape key to quit
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

        # Pass events to current state
        self.state_manager.handle_events(events)

    def _update(self, dt: float) -> None:
        """
        Update game logic.

        Args:
            dt: Delta time in seconds since last frame
        """
        self.state_manager.update(dt)

    def _draw(self) -> None:
        """Render the current frame."""
        # State manager handles drawing the current state
        self.state_manager.draw(self.screen)

    def _quit(self) -> None:
        """Clean up and quit the game."""
        pygame.quit()
        sys.exit()


def main() -> None:
    """Entry point for the game."""
    game = Game()
    game.run()


if __name__ == '__main__':
    main()
