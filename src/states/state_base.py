"""
Base class for all game states.

All game states (Title, Play, GameOver) inherit from this base class
and implement their own specific behavior.
"""

from abc import ABC, abstractmethod
from typing import Optional
import pygame


class State(ABC):
    """
    Abstract base class for game states.

    Each state must implement handle_events, update, and draw methods.
    States can request transitions to other states by returning the next state name.
    """

    def __init__(self, state_manager: 'StateManager') -> None:
        """
        Initialize the state.

        Args:
            state_manager: Reference to the state manager
        """
        self.state_manager = state_manager
        self.next_state: Optional[str] = None

    @abstractmethod
    def handle_events(self, events: list[pygame.event.Event]) -> None:
        """
        Handle pygame events for this state.

        Args:
            events: List of pygame events to process
        """
        pass

    @abstractmethod
    def update(self, dt: float) -> None:
        """
        Update state logic.

        Args:
            dt: Delta time in seconds since last frame
        """
        pass

    @abstractmethod
    def draw(self, surface: pygame.Surface) -> None:
        """
        Draw this state to the screen.

        Args:
            surface: Pygame surface to draw on
        """
        pass

    def on_enter(self) -> None:
        """Called when entering this state. Override if needed."""
        pass

    def on_exit(self) -> None:
        """Called when exiting this state. Override if needed."""
        pass

    def change_state(self, state_name: str) -> None:
        """
        Request a state transition.

        Args:
            state_name: Name of the state to transition to
        """
        self.next_state = state_name
