from collections import deque
from enum import Enum

from game.game_abc import Game


class Ai(object):
    """
    AI which uses the Negamax algorithm to pick 
    the best move for a given game state
    """
    best_move = dict()

    def __init__(self, piece: Enum):
        self.piece = piece

    def negamax(self, game: Game):
        """
        Use Negamax algorithm to find best move in given game state
        """
        self.best_move = dict()
        self._negamax_rec(game, 0, -1000, 1000, self.piece)

    def _negamax_rec(self, game: Game, depth: int, alpha: int, beta: int, piece: Enum):
        """
        Recursive Negamax algorithm at depth of `depth`
        """
        if depth > 10 or game.is_over():
            return piece.value * game.score(self.piece, depth + 1)

        value = -1000

        for move in game.allowed_moves(piece):
            game.move(piece, move, enqueue=True)

            negamax_value = -self._negamax_rec(game, depth + 1, -beta, -alpha, game.other(piece))
            value = max(value, negamax_value)

            game.undo_move()

            if depth == 0:
                self.best_move[move] = value
            
            alpha = max(alpha, negamax_value)
            
            if alpha >= beta:
                return alpha

        return value

    def get_best_move(self):
        """
        Best move based on scores calculated from Negamax algorithm
        """
        if len(self.best_move) == 0:
            return None
        
        return max(self.best_move, key=self.best_move.get)
