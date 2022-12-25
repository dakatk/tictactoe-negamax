from collections.abc import Generator
from abc import ABC, abstractmethod
from enum import Enum


class Game(ABC):
    """
    Base class for game logic
    """
    @abstractmethod
    def allowed_moves(self, piece: Enum) -> Generator:
        """
        Get all allowed moves for `piece`
        """
        pass

    @abstractmethod
    def move(self, piece: Enum, move_pos: object, enqueue=False):
        """
        Moves `piece` to position `move_pos`
        (assumes the move is allowed)
        """
        pass

    @abstractmethod
    def undo_move(self):
        """
        Takes back most recent move in queue
        """
        pass

    @abstractmethod
    def other(self, piece: Enum) -> Enum:
        """
        Inverse piece from `self`
        """
        pass

    @abstractmethod
    def score(self, piece: Enum, depth: int) -> float:
        """
        Score of `piece` at search depth `depth` for current game state
        """
        pass

    @abstractmethod
    def is_over(self):
        """
        Checks if game is at a terminal state
        """
        pass

    @abstractmethod
    def is_winner(self, piece):
        """
        Checks if `piece` has won
        """
