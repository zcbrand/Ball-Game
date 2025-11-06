"""Game entities package."""

from src.entities.sprite_base import SpriteBase
from src.entities.player import Player
from src.entities.obstacle import Obstacle, ScoreCheckpoint

__all__ = ['SpriteBase', 'Player', 'Obstacle', 'ScoreCheckpoint']
