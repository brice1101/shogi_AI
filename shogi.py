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
    PROMOTED_PAWN = 9
    PROMOTED_LANCE = 10
    PROMOTED_KNIGHT = 11
    PROMOTED_SILVER = 12
    PROMOTED_BISHOP = 13
    PROMOTED_ROOK = 14


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
        self.sente_captured = []
        self.gote_captured = []

    def get_piece_at(self, row, col):
        return self.board[row][col]

    def generate_legal_moves(self, row, col):
        print("Generating...")
        piece = self.get_piece_at(row, col)
        player = 1 if piece > 0 else -1
        piece_type = abs(piece)
        moves = []

        # One step forwards
        if piece_type in {
            Piece.PAWN.value,
            Piece.PROMOTED_PAWN.value,
            Piece.SILVER_GENERAL.value,
            Piece.PROMOTED_SILVER.value,
            Piece.GOLD_GENERAL.value,
            Piece.PROMOTED_KNIGHT.value,
            Piece.PROMOTED_LANCE.value,
            Piece.PROMOTED_BISHOP.value,
            Piece.KING.value
        }:
            forward_row = row + player
            if 0 <= forward_row < 9:
                target_square = self.get_piece_at(forward_row, col)
                if target_square == 0 or target_square * player < 0:
                    moves.append((forward_row, col))

        # One step backwards
        if piece_type in {
            Piece.PROMOTED_PAWN.value,
            Piece.PROMOTED_LANCE.value,
            Piece.PROMOTED_KNIGHT.value,
            Piece.PROMOTED_SILVER.value,
            Piece.GOLD_GENERAL.value,
            Piece.PROMOTED_BISHOP.value,
            Piece.KING.value
        }:
            backward_row = row - player
            if 0 <= backward_row < 9:
                target_square = self.get_piece_at(backward_row, col)
                if target_square == 0 or target_square * player < 0:
                    moves.append((backward_row, col))

        # One step sideways
        if piece_type in {
            Piece.PROMOTED_PAWN.value,
            Piece.PROMOTED_LANCE.value,
            Piece.PROMOTED_KNIGHT.value,
            Piece.PROMOTED_SILVER.value,
            Piece.GOLD_GENERAL.value,
            Piece.PROMOTED_BISHOP.value,
            Piece.KING.value
        }:
            target_cols = [col + 1, col - 1]
            for target_col in target_cols:
                if 0 <= target_col < 9:
                    target_square = self.get_piece_at(row, target_col)
                    if target_square == 0 or target_square * player < 0:
                        moves.append((target_col, col))

        # One step forward-diagonal
        if piece_type in {
            Piece.SILVER_GENERAL.value,
            Piece.PROMOTED_PAWN.value,
            Piece.PROMOTED_LANCE.value,
            Piece.PROMOTED_KNIGHT.value,
            Piece.PROMOTED_SILVER.value,
            Piece.GOLD_GENERAL.value,
            Piece.PROMOTED_ROOK.value,
            Piece.KING.value
        }:
            forward_row = row + player
            if 0 <= forward_row < 9:
                target_cols = [col + 1, col - 1]
                for target_col in target_cols:
                    if 0 <= target_col < 9:
                        target_square = self.get_piece_at(forward_row, target_col)
                        if target_square == 0 or target_square * player < 0:
                            moves.append((forward_row, target_col))

        # One step backward-diagonal
        if piece_type in {
            Piece.SILVER_GENERAL.value,
            Piece.PROMOTED_ROOK.value,
            Piece.KING.value
        }:
            backward_row = row - player
            if 0 <= backward_row < 9:
                target_cols = [col + 1, col - 1]
                for target_col in target_cols:
                    if 0 <= target_col < 9:
                        target_square = self.get_piece_at(backward_row, target_col)
                        if target_square == 0 or target_square * player < 0:
                            moves.append((backward_row, target_col))

        # Freely forwards
        if piece_type in {
            Piece.LANCE.value,
            Piece.ROOK.value,
            Piece.PROMOTED_ROOK.value
        }:
            forward_row = row + player
            while 0 <= forward_row < 9:
                target_square = self.get_piece_at(forward_row, col)
                if target_square == 0:
                    moves.append((forward_row, col))
                elif target_square * player < 0:
                    moves.append((forward_row, col))
                    break
                else:
                    break
                forward_row += player

        # Freely backwards
        if piece_type in {
            Piece.ROOK.value,
            Piece.PROMOTED_ROOK.value
        }:
            backward_row = row - player
            while 0 <= backward_row < 9:
                target_square = self.get_piece_at(backward_row, col)
                if target_square == 0:
                    moves.append((backward_row, col))
                elif target_square * player < 0:
                    moves.append((backward_row, col))
                    break
                else:
                    break
                backward_row += player

        # Freely sideways
        if piece_type in {
            Piece.ROOK.value,
            Piece.PROMOTED_ROOK.value
        }:
            target_cols = [col+1, col-1]
            directions = [1, -1]
            for target_col, direction in zip(target_cols, directions):
                while 0 <= target_col < 9:
                    target_square = self.get_piece_at(row, target_col)
                    if target_square == 0:
                        moves.append((row, target_col))
                    elif target_square * player < 0:
                        moves.append((row, target_col))
                        break
                    else:
                        break
                    target_col += direction

        # Freely diagonally
        if piece_type in {
            Piece.BISHOP.value,
            Piece.PROMOTED_BISHOP.value
        }:
            target_rows = [row+1, row-1]
            target_cols = [col + 1, col - 1]
            directions = [1, -1]
            for target_row, vertical_direction in zip(target_rows, directions):
                for target_col, horizontal_direction in zip(target_cols, directions):
                    while 0 <= target_row < 9 and 0 <= target_col < 9:
                        target_square = self.get_piece_at(target_row, target_col)
                        if target_square == 0:
                            moves.append((target_row, target_col))
                        elif target_square * player < 0:
                            moves.append((target_row, target_col))
                            break
                        else:
                            break
                        target_row += vertical_direction
                        target_col += horizontal_direction

        # SPECIAL CASE Knight movement
        if piece_type == Piece.KNIGHT.value:
            target_row = row + (2 * player)
            if 0 <= target_row <= 9:
                target_cols = [col + 1, col - 1]
                for target_col in target_cols:
                    if 0 <= target_col < 9:
                        target_square = self.get_piece_at(target_row, target_col)
                        if target_square == 0 or target_square * player < 0:
                            moves.append((target_row, target_col))

        return moves

    def make_move(self, start_row, start_col, end_row, end_col):
        if (
            self.current_player * self.get_piece_at(start_row, start_col) > 0 and
            (end_row, end_col) in self.generate_legal_moves(start_row, start_col)
        ):
            if self.board[end_row][end_col] != 0:
                if self.current_player == 1:
                    self.sente_captured.append(self.get_piece_at(end_row, end_col))
            promote = False
            if (self.current_player == 1 and end_row >= 6) or (self.current_player == -1 and end_row <= 2):
                promote = True
            self.board[end_row][end_col] = self.board[start_row][start_col]
            self.board[start_row][start_col] = 0

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
