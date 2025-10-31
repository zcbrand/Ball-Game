"""
State manager for handling game state transitions.

The StateManager maintains a dictionary of available states and handles
transitions between them.
"""

from typing import Dict, Optional
import pygame
from src.states.state_base import State


class StateManager:
    """
    Manages game states and transitions between them.

    The StateManager maintains a collection of states and handles
    the current active state, processing its events, updates, and rendering.
    """

    def __init__(self) -> None:
        """Initialize the state manager."""
        self.states: Dict[str, State] = {}
        self.current_state: Optional[State] = None
        self.current_state_name: Optional[str] = None

    def add_state(self, name: str, state: State) -> None:
        """
        Add a state to the manager.

        Args:
            name: Unique identifier for the state
            state: State instance to add
        """
        self.states[name] = state

    def change_state(self, name: str) -> None:
        """
        Transition to a different state.

        Args:
            name: Name of the state to transition to

        Raises:
            KeyError: If the specified state doesn't exist
        """
        if name not in self.states:
            raise KeyError(f"State '{name}' not found in state manager")

        # Exit current state
        if self.current_state:
            self.current_state.on_exit()

        # Change to new state
        self.current_state = self.states[name]
        self.current_state_name = name

        # Enter new state
        self.current_state.on_enter()

    def handle_events(self, events: list[pygame.event.Event]) -> None:
        """
        Pass events to the current state.

        Args:
            events: List of pygame events to process
        """
        if self.current_state:
            self.current_state.handle_events(events)
            self._check_state_transition()

    def update(self, dt: float) -> None:
        """
        Update the current state.

        Args:
            dt: Delta time in seconds since last frame
        """
        if self.current_state:
            self.current_state.update(dt)
            self._check_state_transition()

    def draw(self, surface: pygame.Surface) -> None:
        """
        Draw the current state.

        Args:
            surface: Pygame surface to draw on
        """
        if self.current_state:
            self.current_state.draw(surface)

    def _check_state_transition(self) -> None:
        """Check if current state has requested a transition."""
        if self.current_state and self.current_state.next_state:
            next_state_name = self.current_state.next_state
            self.current_state.next_state = None  # Reset the flag
            self.change_state(next_state_name)
