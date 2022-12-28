from collections.abc import Generator
from abc import ABC, abstractmethod
from enum import Enum


class Game(ABC):
    """
    Base class for game logic
    """
    @abstractmethod
    def allowed_moves(self, player: Enum) -> Generator:
        """
        Get all allowed moves for `player`
        """
        pass

    @abstractmethod
    def move(self, player: Enum, move_pos: object, enqueue=False):
        """
        Makes move for `player` at position `move_pos`
        (assumes move at `move_pos` is allowed)
        """
        pass

    @abstractmethod
    def can_win(self, player: Enum):
        """
        Checks if `player` is able to win in one move 
        with the current board state
        """
        pass

    @abstractmethod
    def undo_move(self):
        """
        Takes back most recent move in queue
        """
        pass

    @abstractmethod
    def other(self, player: Enum) -> Enum:
        """
        Inverse player from `player`
        """
        pass

    @abstractmethod
    def score(self, player: Enum, depth: int) -> float:
        """
        Score for `player` at search depth `depth` for current game state
        """
        pass

    @abstractmethod
    def is_over(self) -> bool:
        """
        Checks if game is at a terminal state
        """
        pass

    @abstractmethod
    def is_winner(self, player: Enum) -> bool:
        """
        Checks if `player` has won
        """
        pass
