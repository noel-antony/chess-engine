from chess.board import Board
from chess.piece import Piece


board = Board()

# Clear board
board.position = [
    [None for _ in range(8)]
    for _ in range(8)
]

# Kings far apart
board.position[7][4] = Piece("white", "king")   # e1
board.position[0][4] = Piece("black", "king")   # e8

# White rook
board.position[4][0] = Piece("white", "rook")   # a4

# Black bishop that rook can capture
board.position[4][5] = Piece("black", "bishop") # f4

# White knight
board.position[5][2] = Piece("white", "knight") # c3

# Black pawn the knight can capture
board.position[3][3] = Piece("black", "pawn")   # d5


captures = board.get_all_capture_moves("white")

print("White captures:")

for move in captures:
    captured = (
        move.captured_piece.piece_type
        if move.captured_piece is not None
        else "en passant"
    )

    print(
        move.start,
        "->",
        move.end,
        "captured:",
        captured
    )
