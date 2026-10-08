from chess.board import Board
from chess.piece import Piece


# =========================================================
# TEST 1 — CASTLING RIGHTS
# =========================================================

board = Board()

# Clear the squares around the white king
board.position[6][4] = None   # e2
board.position[6][3] = None   # d2
board.position[6][5] = None   # f2

# Now e1 -> e2 is possible
moves = board.get_all_legal_moves("white")

king_move = None

for move in moves:
    if move.start == (7, 4) and move.end == (6, 4):
        king_move = move
        break

print("Initial castling rights:")
print(board.castling_rights)

if king_move is None:
    print("Could not find e1-e2")
else:
    board.make_move(king_move)

    print("\nAfter king moves:")
    print(board.castling_rights)

    board.undo_move()

    print("\nAfter undo:")
    print(board.castling_rights)


# =========================================================
# TEST 2 — EN PASSANT STATE
# =========================================================

board = Board()

moves = board.get_all_legal_moves("white")

e4_move = None

for move in moves:
    if move.start == (6, 4) and move.end == (4, 4):
        e4_move = move
        break

if e4_move is None:
    print("\nCould not find e2-e4")
else:
    board.make_move(e4_move)

    print("\nAfter e2-e4:")
    print("En passant square:", board.en_passant_square)

    board.undo_move()

    print("\nAfter undo:")
    print("En passant square:", board.en_passant_square)
