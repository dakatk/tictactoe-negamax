from enum import Enum
from collections import deque

from .game_abc import Game


class Piece(Enum):
    """
    Tic-Tac-Toe piece types and values
    """
    X = -1
    O = 1
    S = 0

    def other(self):
        """
        Inverse piece from `self`
        """
        return {
            Piece.X: Piece.O,
            Piece.O: Piece.X,
            Piece.S: Piece.S
        }[self]

    def __str__(self):
        return {
            Piece.X: 'X',
            Piece.O: 'O',
            Piece.S: ' '
        }[self]


class TicTacToe(Game):
    """
    TicTacToe game
    """
    _board = [
        [Piece.S, Piece.S, Piece.S],
        [Piece.S, Piece.S, Piece.S],
        [Piece.S, Piece.S, Piece.S]
    ]
    _win_checks = [
        # Rows
        [(0, 0), (0, 1), (0, 2)],
        [(1, 0), (1, 1), (1, 2)],
        [(2, 0), (2, 1), (2, 2)],
        # Cols
        [(0, 0), (1, 0), (2, 0)],
        [(0, 1), (1, 1), (2, 1)],
        [(0, 2), (1, 2), (2, 2)],
        # Diags
        [(0, 0), (1, 1), (2, 2)],
        [(0, 2), (1, 1), (2, 0)]
    ]
    _moves_queue = deque()

    def allowed_moves(self, piece):
        """
        Get all allowed moves for `piece`
        """
        allowed_moves = list()
        for (i, row) in enumerate(self._board):
            allowed_moves.extend([(i, j) for (j, col) in enumerate(row) if col == Piece.S])
        
        return allowed_moves

    def move(self, piece, move, enqueue=False):
        """
        Moves `piece` from `from_pos` to `to_pos`
        (assumes the move is allowed)
        """
        if enqueue:
            self._moves_queue.appendleft(move)

        self._board[move[0]][move[1]] = piece

    def undo_move(self):
        """
        Takes back most recent move in queue
        """
        move = self._moves_queue.popleft()
        self._board[move[0]][move[1]] = Piece.S

    def other(self, piece):
        """
        Inverse piece from `self`
        """
        return piece.other()

    def score(self, piece, depth):
        """
        Score of `piece` at search depth `depth` for current game state
        """
        if self.is_winner(piece):
            return 1000 / depth
        elif self.allowed_moves(piece) == 0:
            return 0
        else:
            return -1000 / depth

    def is_over(self):
        """
        Checks if game is at a terminal state
        """
        allowed_moves = len(list(self.allowed_moves(None)))
        return self.is_winner(Piece.X) or self.is_winner(Piece.O) or allowed_moves == 0

    def is_winner(self, piece):
        """
        Checks if `piece` has won
        """
        for win_check in self._win_checks:
            if all([self._board[i][j] == piece for (i, j) in win_check]):
                return True

        return False

    def __str__(self):
        s = ''

        for (i, row) in enumerate(self._board):
            s += f' {row[0]} | {row[1]} | {row[2]}\n'

            if i < 2:
                s += '-----------\n'

        return s

    __repr__ = __str__
