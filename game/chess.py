from game_abc import Game


class Chess(Game):
    def allowed_moves(self, player: Enum) -> Generator:
        """
        Get all allowed moves for `player`
        """
        pass

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