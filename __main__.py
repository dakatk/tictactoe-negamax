#!/usr/bin/env python3

import time
import sys

from ai.negamax import Ai
from game.tictactoe import TicTacToe, Piece

#from game.chess import Chess


PLAYER_MOVE_SEP = ','


def main(game, ai):
    """
    Main game loop
    """
    player_turn = True
    player_piece = ai.player.other()

    while True:
        print(f'\n{game}')
        if player_turn:
            if not player_move(game, player_piece):
                break
        else:
            if not ai_move(game, ai):
                break

        if game.is_over():
            print('Tie game!')
            break
        
        player_turn = not player_turn

    print(f'\n{game}')


def player_move(game, piece):
    """
    Get player input from command line for player move
    """
    player_input = input('Player move: ')
    if player_input.lower() == 'q':
        sys.exit(0)
    
    (x, y) = map(lambda s: int(s.strip()), player_input.split(PLAYER_MOVE_SEP))

    game.move(piece, (x, y))

    if game.is_winner(piece):
        print('Player wins!')
        return False

    return True


def ai_move(game, ai):
    """
    AI chooses best move using Negamax algorithm
    """
    print("AI's turn")
    # start_time = time.time()
    ai.negamax(game)
    move = ai.get_best_move()
    # print(time.time() - start_time)

    if move is None:
        print('AI Forfeits!')
        return False
    else:
        game.move(ai.player, move)

    if game.is_winner(ai.player):
        print('AI wins!')
        return False

    return True


sys.setrecursionlimit(31)

_game = TicTacToe()
_ai = Ai(Piece.O)

main(_game, _ai)
