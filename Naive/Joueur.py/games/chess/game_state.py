from numpy import full


class GameState:
    def __init__(self, board, active_color, castling, en_passant, halfmove, fullmove):
        self.board = board
        self.active_color = active_color
        self.castling = castling
        self.en_passant = en_passant
        self.halfmove = int(halfmove)
        self.fullmove = int(fullmove)