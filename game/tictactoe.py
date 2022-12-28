#!/usr/bin/env python3

from enum import Enum
from collections import deque
from collections.abc import Generator

from game_abc import Game


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

        >>> str(Piece.O.other())
        'X'
        >>> str(Piece.X.other())
        'O'
        >>> str(Piece.S.other())
        ' '
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

    def allowed_moves(self, player: Piece) -> Generator:
        """
        Get all allowed moves for `player`

        >>> game = TicTacToe()
        >>> game._board = [[Piece.X, Piece.S, Piece.S], [Piece.S, Piece.X, Piece.S], [Piece.S, Piece.S, Piece.O]]
        >>> list(game.allowed_moves(None))
        [(0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1)]
        >>> game._board = [[Piece.O, Piece.X, Piece.S], [Piece.S, Piece.X, Piece.S], [Piece.S, Piece.S, Piece.S]]
        >>> list(game.allowed_moves(None))
        [(0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)]
        """
        for (i, row) in enumerate(self._board):
            for (j, col) in enumerate(row):
                if col == Piece.S:
                    yield (i, j)

    def move(self, player: Piece, move: tuple, enqueue=False):
        """
        Makes move for `player` at position `move_pos`
        (assumes move at `move_pos` is allowed)

        >>> game = TicTacToe()
        >>> game.move(Piece.O, (0, 0), enqueue=True)
        >>> str(game._board[0][0])
        'O'
        >>> len(game._moves_queue)
        1
        >>> game._moves_queue.popleft()
        (0, 0)
        """
        if enqueue:
            self._moves_queue.appendleft(move)

        self._board[move[0]][move[1]] = player

    def can_win(self, player: Enum):
        """
        Checks if `player` is able to win in one move 
        with the current board state

        >>> game = TicTacToe()
        >>> game._board = [[Piece.X, Piece.X, Piece.S], [Piece.S, Piece.S, Piece.S], [Piece.S, Piece.S, Piece.S]]
        >>> game.can_win(Piece.X)
        True
        >>> game._board = [[Piece.X, Piece.X, Piece.S], [Piece.S, Piece.S, Piece.S], [Piece.S, Piece.S, Piece.S]]
        >>> game.can_win(Piece.O)
        False
        """
        for (i, row) in enumerate(self._board):
            for (j, col) in enumerate(row):
                if col != Piece.S:
                    continue

                self._board[i][j] = player
                winner = self.is_winner(player)
                self._board[i][j] = Piece.S

                if winner:
                    return True

        return False

    def undo_move(self):
        """
        Takes back most recent move in queue

        >>> game = TicTacToe()
        >>> game.move(Piece.O, (0, 0), enqueue=True)
        >>> str(game._board[0][0])
        'O'
        >>> game.undo_move()
        >>> str(game._board[0][0])
        ' '
        """
        if len(self._moves_queue) == 0:
            return
        
        move = self._moves_queue.popleft()
        self._board[move[0]][move[1]] = Piece.S

    def other(self, player: Piece) -> Piece:
        """
        Inverse piece from `self`

        >>> game = TicTacToe()
        >>> str(game.other(Piece.X))
        'O'
        >>> str(game.other(Piece.O))
        'X'
        >>> str(game.other(Piece.S))
        ' '
        """
        return player.other()

    def score(self, player: Piece, depth: int) -> float:
        """
        Score of `piece` at search depth `depth` for current game state

        >>> game = TicTacToe()
        >>> game._board = [[Piece.X, Piece.X, Piece.X], [Piece.S, Piece.S, Piece.S], [Piece.S, Piece.S, Piece.S]]
        >>> game.score(Piece.X, 2)
        500.0
        >>> game._board = [[Piece.X, Piece.O, Piece.X], [Piece.X, Piece.O, Piece.X], [Piece.O, Piece.X, Piece.O]]
        >>> game.score(Piece.X, 2)
        0
        >>> game._board = [[Piece.O, Piece.O, Piece.O], [Piece.S, Piece.S, Piece.S], [Piece.S, Piece.S, Piece.S]]
        >>> game.score(Piece.X, 2)
        -500.0
        """
        allowed_moves = len(list(self.allowed_moves(None)))

        if self.is_winner(player):
            return 1000 / depth
        elif allowed_moves == 0:
            return 0
        else:
            return -1000 / depth

    def is_over(self) -> bool:
        """
        Checks if game is at a terminal state

        >>> game = TicTacToe()
        >>> game._board = [[Piece.X, Piece.X, Piece.X], [Piece.S, Piece.S, Piece.S], [Piece.S, Piece.S, Piece.S]]
        >>> game.is_over()
        True
        >>> game._board = [[Piece.O, Piece.O, Piece.O], [Piece.S, Piece.S, Piece.S], [Piece.S, Piece.S, Piece.S]]
        >>> game.is_over()
        True
        >>> game._board = [[Piece.X, Piece.O, Piece.X], [Piece.X, Piece.O, Piece.X], [Piece.O, Piece.X, Piece.O]]
        >>> game.is_over()
        True
        >>> game._board = [[Piece.X, Piece.X, Piece.O], [Piece.S, Piece.S, Piece.S], [Piece.S, Piece.S, Piece.S]]
        >>> game.is_over()
        False
        """
        spaces_left = any([any([col == Piece.S for col in row]) for row in self._board])
        return self.is_winner(Piece.X) or self.is_winner(Piece.O) or not spaces_left

    def is_winner(self, player: Piece) -> bool:
        """
        Checks if `player` has won

        >>> game = TicTacToe()
        >>> game.is_winner(Piece.S)
        False
        >>> game.is_winner(None)
        False
        >>> game._board = [[Piece.X, Piece.X, Piece.X], [Piece.S, Piece.S, Piece.S], [Piece.S, Piece.S, Piece.S]]
        >>> game.is_winner(Piece.X)
        True
        >>> game._board = [[Piece.S, Piece.S, Piece.S], [Piece.X, Piece.X, Piece.X], [Piece.S, Piece.S, Piece.S]]
        >>> game.is_winner(Piece.X)
        True
        >>> game._board = [[Piece.S, Piece.S, Piece.S], [Piece.S, Piece.S, Piece.S], [Piece.X, Piece.X, Piece.X]]
        >>> game.is_winner(Piece.X)
        True
        >>> game._board = [[Piece.X, Piece.S, Piece.S], [Piece.X, Piece.S, Piece.S], [Piece.X, Piece.S, Piece.S]]
        >>> game.is_winner(Piece.X)
        True
        >>> game._board = [[Piece.S, Piece.X, Piece.S], [Piece.S, Piece.X, Piece.S], [Piece.S, Piece.X, Piece.S]]
        >>> game.is_winner(Piece.X)
        True
        >>> game._board = [[Piece.S, Piece.S, Piece.X], [Piece.S, Piece.S, Piece.X], [Piece.S, Piece.S, Piece.X]]
        >>> game.is_winner(Piece.X)
        True
        >>> game._board = [[Piece.X, Piece.S, Piece.S], [Piece.S, Piece.X, Piece.S], [Piece.S, Piece.S, Piece.X]]
        >>> game.is_winner(Piece.X)
        True
        >>> game._board = [[Piece.S, Piece.S, Piece.X], [Piece.S, Piece.X, Piece.S], [Piece.X, Piece.S, Piece.S]]
        >>> game.is_winner(Piece.X)
        True
        """
        if player == None or player == Piece.S:
            return False

        magic_number = player.value * 3
        
        for win_check in self._win_checks:
            if sum((self._board[i][j].value for (i, j) in win_check)) == magic_number:
                return True

        return False

    def __str__(self):
        sep = '-----------\n'
        rows = (f' {row[0]} | {row[1]} | {row[2]}\n' for row in self._board)
        return sep.join(rows)

    __repr__ = __str__


if __name__ == "__main__":
    import doctest
    doctest.testmod()
