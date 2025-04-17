from enum import Enum
import tkinter as tk


class Piece(Enum):
    EMPTY = "", 0
    KING = "玉", 1
    ROOK = "飛", 2
    BISHOP = "角", 3
    GOLD_GENERAL = "金", 4
    SILVER_GENERAL = "銀", 5
    KNIGHT = "桂", 6
    LANCE = "香", 7
    PAWN = "歩", 8
    PROMOTED_ROOK = "竜", 9
    PROMOTED_BISHOP = "馬", 10
    PROMOTED_SILVER = "全", 11
    PROMOTED_KNIGHT = "圭", 12
    PROMOTED_LANCE = "杏", 13
    PROMOTED_PAWN = "と", 14

    def __init__(self, kanji, numeric):
        self.kanji = kanji
        self.numeric = numeric

    def __str__(self):
        return self.kanji


def initialize_board():

    # Sente (Player 1) pieces
    board = [[0 for _ in range(9)] for _ in range(9)]
    board[0] = [
        Piece.LANCE.numeric,
        Piece.KNIGHT.numeric,
        Piece.SILVER_GENERAL.numeric,
        Piece.GOLD_GENERAL.numeric,
        Piece.KING.numeric,
        Piece.GOLD_GENERAL.numeric,
        Piece.SILVER_GENERAL.numeric,
        Piece.KNIGHT.numeric,
        Piece.LANCE.numeric,
    ]
    board[1][1] = Piece.BISHOP.numeric
    board[1][-2] = Piece.ROOK.numeric
    board[2] = [Piece.PAWN.numeric] * 9

    # Gote (Player 2) pieces
    board[-1] = [-piece for piece in board[0]]
    board[-2][-2] = -Piece.BISHOP.numeric
    board[-2][1] = -Piece.ROOK.numeric
    board[-3] = [-Piece.PAWN.numeric] * 9

    return board


class ShogiGame:

    def __init__(self):
        self.board = initialize_board()
        self.current_player = 1
        self.sente_captured = []
        self.gote_captured = []

    def get_board(self):
        return self.board

    def get_piece_at(self, row, col):
        return self.board[row][col]

    def generate_legal_moves(self, row, col):
        piece = self.get_piece_at(row, col)
        player = 1 if piece > 0 else -1
        piece_type = abs(piece)
        moves = []

        # One step forwards
        if piece_type in {
            Piece.PAWN.numeric,
            Piece.PROMOTED_PAWN.numeric,
            Piece.SILVER_GENERAL.numeric,
            Piece.PROMOTED_SILVER.numeric,
            Piece.GOLD_GENERAL.numeric,
            Piece.PROMOTED_KNIGHT.numeric,
            Piece.PROMOTED_LANCE.numeric,
            Piece.PROMOTED_BISHOP.numeric,
            Piece.KING.numeric
        }:
            forward_row = row + player
            if 0 <= forward_row < 9:
                target_square = self.get_piece_at(forward_row, col)
                if target_square == 0 or target_square * player < 0:
                    moves.append((forward_row, col))

        # One step backwards
        if piece_type in {
            Piece.PROMOTED_PAWN.numeric,
            Piece.PROMOTED_LANCE.numeric,
            Piece.PROMOTED_KNIGHT.numeric,
            Piece.PROMOTED_SILVER.numeric,
            Piece.GOLD_GENERAL.numeric,
            Piece.PROMOTED_BISHOP.numeric,
            Piece.KING.numeric
        }:
            backward_row = row - player
            if 0 <= backward_row < 9:
                target_square = self.get_piece_at(backward_row, col)
                if target_square == 0 or target_square * player < 0:
                    moves.append((backward_row, col))

        # One step sideways
        if piece_type in {
            Piece.PROMOTED_PAWN.numeric,
            Piece.PROMOTED_LANCE.numeric,
            Piece.PROMOTED_KNIGHT.numeric,
            Piece.PROMOTED_SILVER.numeric,
            Piece.GOLD_GENERAL.numeric,
            Piece.PROMOTED_BISHOP.numeric,
            Piece.KING.numeric
        }:
            target_cols = [col + 1, col - 1]
            for target_col in target_cols:
                if 0 <= target_col < 9:
                    target_square = self.get_piece_at(row, target_col)
                    if target_square == 0 or target_square * player < 0:
                        moves.append((target_col, col))

        # One step forward-diagonal
        if piece_type in {
            Piece.SILVER_GENERAL.numeric,
            Piece.PROMOTED_PAWN.numeric,
            Piece.PROMOTED_LANCE.numeric,
            Piece.PROMOTED_KNIGHT.numeric,
            Piece.PROMOTED_SILVER.numeric,
            Piece.GOLD_GENERAL.numeric,
            Piece.PROMOTED_ROOK.numeric,
            Piece.KING.numeric
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
            Piece.SILVER_GENERAL.numeric,
            Piece.PROMOTED_ROOK.numeric,
            Piece.KING.numeric
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
            Piece.LANCE.numeric,
            Piece.ROOK.numeric,
            Piece.PROMOTED_ROOK.numeric
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
            Piece.ROOK.numeric,
            Piece.PROMOTED_ROOK.numeric
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
            Piece.ROOK.numeric,
            Piece.PROMOTED_ROOK.numeric
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
            Piece.BISHOP.numeric,
            Piece.PROMOTED_BISHOP.numeric
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
        if piece_type == Piece.KNIGHT.numeric:
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
            self.current_player *= -1

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


class ShogiGUI:
    def __init__(self, main, shogi_game):
        self.main = main
        main.title("Shogi Board")
        self.shogi_game = shogi_game
        self.board_size = 60
        self.buttons = [[None for _ in range(9)] for _ in range(9)]
        self.selected_piece_position = None

        self._create_board()
        self._update_board()

    def _create_board(self):
        for row in range(9):
            for col in range(9):
                button = tk.Button(
                    self.main,
                    text="",
                    width=2,
                    height=1,
                    font=("Arial", 20),
                    command=lambda r=row, c=col: self._handle_click(r, c)
                )
                button.grid(row=row, column=col)
                self.buttons[row][col] = button

    def _update_board(self):
        board_state = self.shogi_game.get_board()
        for row in range(9):
            for col in range(9):
                piece = board_state[row][col]
                self.buttons[row][col].config(text=self._get_piece_representation(piece))

    def _get_piece_representation(self, piece):
        for p in Piece:
            if p.numeric == abs(piece):
                return str(p)
        return None

    def _handle_click(self, row, col):
        if self.selected_piece_position is None:
            piece = self.shogi_game.get_piece_at(row, col)
            if piece is not None and self.shogi_game.get_piece_at(row, col) * self.shogi_game.current_player > 0:
                self.selected_piece_position = (row, col)

        else:
            start_row, start_col = self.selected_piece_position
            if (row, col) in self.shogi_game.generate_legal_moves(start_row, start_col):
                self.shogi_game.make_move(start_row, start_col, row, col)
                self._update_board()
                self.selected_piece_position = None

            else:
                self.selected_piece_position = None
                print("Invalid Move")


if __name__ == "__main__":
    root = tk.Tk()
    game = ShogiGame()
    gui = ShogiGUI(root, game)
    root.mainloop()