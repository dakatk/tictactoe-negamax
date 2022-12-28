#!/usr/bin/env python3

from enum import Enum
from collections import deque

from game.game_abc import Game


class GameEnd(Enum):
    WIN = 3
    LOSE = -1
    DRAW = 1


class Menace(object):
    _matchboxes = dict()
    _history = deque()

    def __init__(self, default_beads=3):
        self._default_beads = default_beads

    def best_move(game: Game, player: Enum) -> object:
        """
        Get best move based on number of beads
        """
        game_state = str(game)

        if game_state not in self._matchboxes:
            self._matchboxes[game_state] = dict()
            allowed_moves = game.allowed_moves(player)

            for move in allowed_moves:
                self._matchboxes[game_state][move] = self._default_beads
            
        current_matchbox = self._matchboxes[game_state]
        if len(current_matchbox) == 0:
            return None
        
        best_move = max(current_matchbox, key=current_matchbox.get)
        self._history.appendleft((game_state, best_move))

        return best_move

    def update(game_end: GameEnd):
        """
        Update number of beads in used matchboxes after game is over
        """
        for (game_state, best_move) in self._history:
            self._matchboxes[game_state][best_move] += game_end.value
