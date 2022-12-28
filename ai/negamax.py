#!/usr/bin/env python3

from enum import Enum

from game.game_abc import Game


class Ai(object):
    """
    AI which uses the Negamax algorithm to pick 
    the best move for a given game state
    """
    _best_moves = dict()

    def __init__(self, player: Enum):
        self._player = player

    def negamax(self, game: Game):
        """
        Use Negamax algorithm to find best move in given game state
        """
        self._best_moves = dict()
        self._negamax_rec(game, 0, -1000, 1000, self._player)

    def _negamax_rec(self, game: Game, depth: int, alpha: int, beta: int, player: Enum):
        """
        Recursive Negamax algorithm at depth of `depth`
        """
        if depth > 10 or game.is_over():
            return player.value * game.score(self._player, depth + 1)

        value = -1000

        for move in game.allowed_moves(player):
            game.move(player, move, enqueue=True)
            next_player = game.other(player)

            if game.can_win(next_player):
                negamax_value = -1000
            else:
                negamax_value = -self._negamax_rec(game, depth + 1, -beta, -alpha, next_player)
        
            value = max(value, negamax_value)
            game.undo_move()

            if depth == 0:
                self._best_moves[move] = value
            
            alpha = max(alpha, negamax_value)
            
            if alpha >= beta:
                return alpha

        return value

    def get_best_move(self):
        """
        Best move based on scores calculated from Negamax algorithm

        >>> ai = Ai(None)
        >>> ai.get_best_move() == None
        True
        >>> ai._best_moves[(0, 0)] = 2
        >>> ai._best_moves[(0, 1)] = 3
        >>> ai.get_best_move()
        (0, 1)
        """
        if len(self._best_moves) == 0:
            return None
        
        return max(self._best_moves, key=self._best_moves.get)

    @property
    def player(self):
        return self._player


if __name__ == '__main__':
    import doctest
    doctest.testmod()
