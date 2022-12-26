#!/usr/bin/env python3

from negamax import Ai
from game.tictactoe import TicTacToe, Piece


PLAYER_MOVE_SEP = ','


def main(game, ai):
    """
    Main game loop
    """
    player_turn = True
    player_piece = ai._player.other()

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
    ai.negamax(game)
    move = ai.get_best_move()

    if move is None:
        print('AI Forfeits!')
        return False
    else:
        game.move(ai._player, move)

    if game.is_winner(ai._player):
        print('AI wins!')
        return False

    return True


_game = TicTacToe()
_ai = Ai(Piece.O)

main(_game, _ai)