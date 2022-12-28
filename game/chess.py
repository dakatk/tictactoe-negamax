#!/usr/bin/env python3

from enum import Enum
from collections import deque
from collections.abc import Generator

from game_abc import Game


class Player(Enum):
    """
    Player representation (black or white)
    """
    B = 1
    W = -1

    def other(self):
        """
        Inverse player from `self`

        >>> str(Player.B.other())
        'W'
        >>> str(Player.W.other())
        'B'
        """
        return { 
            Player.B: Player.W,
            Player.W: Player.B
        }[self]

    def __str__(self):
        return {
            Player.B: 'B',
            Player.W: 'W'
        }[self]


class PieceType(Enum):
    """
    Representation and score for each piece type
    """
    PAWN = 1
    ROOK = 2
    KNIGHT = 3
    BISHOP = 4
    KING = 5
    QUEEN = 6

    def __str__(self):
        return {
            PieceType.PAWN: 'P',
            PieceType.ROOK: 'R',
            PieceType.KNIGHT: 'N',
            PieceType.BISHOP: 'B',
            PieceType.KING: 'K',
            PieceType.QUEEN: 'Q'
        }[self]


class Piece(object):
    """
    Parent class for piece movement logic
    """
    def __init__(self, player: Player, piece_type: PieceType):
        self._player = player
        self._piece_type = piece_type

    def allowed_moves(self, board):
        """
        All allowed moves for `self` in the given board state
        """
        pass

    @property
    def player(self):
        return self._player

    @property
    def piece_type(self):
        return self._piece_type

    def __str__(self):
        return f'{str(self._player)}{str(self._piece_type)}'


class Pawn(Piece):
    """
    Pawn
    """
    def __init__(self, player: Player):
        super().__init__(player, PieceType.PAWN)

    def allowed_moves(self, board):
        """
        All allowed moves for `self` in the given board state
        """
        pass


class Rook(Piece):
    """
    Rook
    """
    def __init__(self, player: Player):
        super().__init__(player, PieceType.ROOK)

    def allowed_moves(self, board):
        """
        All allowed moves for `self` in the given board state
        """
        pass


class Knight(Piece):
    """
    Knight
    """
    def __init__(self, player: Player):
        super().__init__(player, PieceType.KNIGHT)

    def allowed_moves(self, board):
        """
        All allowed moves for `self` in the given board state
        """
        pass


class Bishop(Piece):
    """
    Bishop
    """
    def __init__(self, player: Player):
        super().__init__(player, PieceType.BISHOP)

    def allowed_moves(self, board):
        """
        All allowed moves for `self` in the given board state
        """
        pass


class King(Piece):
    """
    King
    """
    def __init__(self, player: Player):
        super().__init__(player, PieceType.KING)

    def allowed_moves(self, board):
        """
        All allowed moves for `self` in the given board state
        """
        pass


class Queen(Piece):
    """
    Queen
    """
    def __init__(self, player: Player):
        super().__init__(player, PieceType.QUEEN)

    def allowed_moves(self, board):
        """
        All allowed moves for `self` in the given board state
        """
        pass


class Chess(Game):
    """
    Chess game
    """
    _board = [
        [Rook(Player.B), Knight(Player.B), Bishop(Player.B), Queen(Player.B), King(Player.B), Bishop(Player.B), Knight(Player.B), Rook(Player.B)],
        [Pawn(Player.B), Pawn(Player.B), Pawn(Player.B), Pawn(Player.B), Pawn(Player.B), Pawn(Player.B), Pawn(Player.B), Pawn(Player.B)],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [Pawn(Player.W), Pawn(Player.W), Pawn(Player.W), Pawn(Player.W), Pawn(Player.W), Pawn(Player.W), Pawn(Player.W), Pawn(Player.W)],
        [Rook(Player.W), Knight(Player.W), Bishop(Player.W), Queen(Player.W), King(Player.W), Bishop(Player.W), Knight(Player.W), Rook(Player.W)]
    ]
    _moves_queue = deque()

    def allowed_moves(self, player: Enum) -> Generator:
        """
        Get all allowed moves for `player`
        """
        pieces = list()
        for row in self._board:
            pieces.extend((col for col in row if col is not None and col.player == player))

        for piece in pieces:
            for move in piece.allowed_moves(self._board):
                yield move


    def move(self, player: Enum, move_pos: object, enqueue=False):
        """
        Makes move for `player` at position `move_pos`
        (assumes move at `move_pos` is allowed)
        """
        pass

    def undo_move(self):
        """
        Takes back most recent move in queue
        """
        pass

    def other(self, player: Enum) -> Enum:
        """
        Inverse player from `player`
        """
        pass

    def score(self, player: Enum, depth: int) -> float:
        """
        Score for `player` at search depth `depth` for current game state
        """
        pass

    def is_over(self) -> bool:
        """
        Checks if game is at a terminal state
        """
        pass

    def is_winner(self, player: Enum) -> bool:
        """
        Checks if `player` has won
        """
        pass

    def __str__(self):
        sep = '  -------------------------\n'
        footer = '   A  B  C  D  E  F  G  H'

        piece_str = lambda p: '  ' if p is None else str(p)
        rows = (f'{8 - i} |' + '|'.join([piece_str(col) for col in row]) + '|\n' for (i, row) in enumerate(self._board))

        return sep + sep.join(rows) + sep + footer

    __repr__ = __str__


if __name__ == '__main__':
    import doctest
    doctest.testmod()
