from negamax import Ai
from game.tictactoe import TicTacToe, Piece


def main(game, ai):
    """
    Main game loop
    """
    player_turn = True
    player_piece = ai.piece.other()

    while True:
        print(game)
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

    print(game)


def player_move(game, piece):
    """
    Get player input from command line for player move
    """
    player_input = input('Player move: ')
    (x, y) = map(lambda s: int(s.strip()), player_input.split(','))

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
    print('AI moved!')

    if ai.best_move is None:
        print('AI Forfeits!')
        return False
    
    move = ai.get_best_move()
    game.move(ai.piece, move)

    if game.is_winner(ai.piece):
        print('AI wins!')
        return False

    return True


_game = TicTacToe()
_ai = Ai(Piece.O)

main(_game, _ai)