from enum import Enum


class Piece(Enum):
    EMPTY = 0
    PAWN = 1
    LANCE = 2
    KNIGHT = 3
    SILVER_GENERAL = 4
    GOLD_GENERAL = 5
    BISHOP = 6
    ROOK = 7
    KING = 8


def initialize_board():

    # Sente (Player 1) pieces
    board = [[0 for _ in range(9)] for _ in range(9)]
    board[0] = [
        Piece.LANCE.value,
        Piece.KNIGHT.value,
        Piece.SILVER_GENERAL.value,
        Piece.GOLD_GENERAL.value,
        Piece.KING.value,
        Piece.GOLD_GENERAL.value,
        Piece.SILVER_GENERAL.value,
        Piece.KNIGHT.value,
        Piece.LANCE.value,
    ]
    board[1][1] = Piece.BISHOP.value
    board[1][-2] = Piece.ROOK.value
    board[2] = [Piece.PAWN.value] * 9

    # Gote (Player 2) pieces
    board[-1] = [-piece for piece in board[0]]
    board[-2][-2] = -Piece.BISHOP.value
    board[-2][1] = -Piece.ROOK.value
    board[-3] = [-Piece.PAWN.value] * 9

    return board


class ShogiGame:
    def __init__(self):
        self.board = initialize_board()
        self.current_player = 1
        self.sente_captured = {}
        self.gote_captured = {}

    def get_piece_at(self, row, col):
        return self.board[row][col]

    def generate_legal_moves(self, row, col):
        piece = self.get_piece_at(row, col)
        player = 1 if piece > 0 else -1
        piece_type = abs(piece)
        moves = []
        # logic based on piece_type and player
        return moves

    def make_move(self, start_row, start_col, end_row, end_col, promote=False):
        # Update board, handle captures, promotion, and switch players
        pass

    def is_king_in_check(self, player):
        # check if king is under attack
        pass

    def is_checkmate(self, player):
        pass

    def is_game_over(self):
        return self.is_checkmate(1) or self.is_checkmate(-1)

    def play_game(self):
        while not self.is_game_over():
            pass