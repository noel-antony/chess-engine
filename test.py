from chess.board import Board
from chess.move import Move
from chess.piece import Piece

board = Board()

def clear_board():
    board.position = [[None for _ in range(8)] for _ in range(8)]

def add_piece(row, col, color, piece_type):
    board.position[row][col] = Piece(color, piece_type)

def print_moves(moves):
    for move in moves:
        print(f"{move.start} -> {move.end}")

def print_moves_from(row, col):
    moves = board.generate_moves((row, col))
    print(f"Moves from ({row}, {col}):")
    print_moves(moves)



# Test 1 — make move
# move = Move((6, 4), (4, 4))
# board.make_move(move)
#
# print("After move:")
# print("e2:", board.position[6][4])
# print("e4:", board.position[4][4])


# Test 2 — undo move
# move = Move((6, 4), (4, 4))
# board.make_move(move)
# board.undo_move()
#
# print("After undo:")
# print("e2:", board.position[6][4])
# print("e4:", board.position[4][4])


# Test 3 — capture + undo
# add_piece(4, 4, "black", "pawn")
#
# move = Move((6, 4), (4, 4))
# board.make_move(move)
#
# print("After capture:")
# print("e2:", board.position[6][4])
# print("e4:", board.position[4][4])
# print("Captured:", move.captured_piece)
#
# board.undo_move()
#
# print("After undo:")
# print("e2:", board.position[6][4])
# print("e4:", board.position[4][4])


# Test 4 — starting position
# print_moves_from(7, 6)  # knight
# print_moves_from(6, 4)  # pawn
# print_moves_from(7, 0)  # rook


# Test 5 — rook blocking + capture
# clear_board()

# add_piece(4, 3, "white", "rook")
# add_piece(2, 3, "black", "pawn")
# add_piece(6, 3, "white", "pawn")

# print_moves_from(4, 3)


# Test 6 — pawn capture
# clear_board()

# add_piece(4, 4, "white", "pawn")
# add_piece(3, 3, "black", "pawn")

# print_moves_from(4, 4)


# Test 7

# clear_board()

# add_piece(7, 4, "white", "king")
# add_piece(7, 0, "white", "rook")
# add_piece(7, 7, "white", "rook")

# moves = board.generate_legal_moves(7, 4)

# for move in moves:
#     print(move.start, "->", move.end, move.special)


# Test 8

# castle = next(
#     move for move in moves
#     if move.special == "castle_kingside"
# )

# board.make_move(castle)


# Test 9 - All special moves

# clear_board()

# add_piece(1, 4, "white", "pawn")
# add_piece(7, 7, "white", "king")
# add_piece(0, 0, "black", "king")

# moves = board.generate_moves(1, 4)

# assert {m.promotion for m in moves} == {
#     "queen", "rook", "bishop", "knight"
# }

# m = next(m for m in moves if m.promotion == "queen")
# board.make_move(m)
# assert board.position[0][4].piece_type == "queen"
# board.undo_move()
# assert board.position[1][4].piece_type == "pawn"

# clear_board()
# add_piece(7, 4, "white", "king")
# add_piece(7, 0, "white", "rook")
# add_piece(7, 7, "white", "rook")
# add_piece(0, 4, "black", "king")

# moves = board.generate_moves(7, 4)
# ks = next(m for m in moves if m.special == "castle_kingside")
# qs = next(m for m in moves if m.special == "castle_queenside")

# board.make_move(ks)
# assert board.position[7][6].piece_type == "king"
# assert board.position[7][5].piece_type == "rook"
# board.undo_move()

# board.make_move(qs)
# assert board.position[7][2].piece_type == "king"
# assert board.position[7][3].piece_type == "rook"
# board.undo_move()

# clear_board()
# add_piece(3, 4, "white", "pawn")
# add_piece(1, 3, "black", "pawn")
# add_piece(7, 4, "white", "king")
# add_piece(0, 4, "black", "king")

# board.make_move(Move((1, 3), (3, 3)))

# moves = board.generate_moves(3, 4)
# ep = next(m for m in moves if m.special == "en_passant")

# board.make_move(ep)
# assert board.position[2][3].piece_type == "pawn"
# assert board.position[3][3] is None
# board.undo_move()

# assert board.position[3][4].piece_type == "pawn"
# assert board.position[3][3].piece_type == "pawn"

# board.undo_move()

# print("ALL SPECIAL MOVE TESTS PASSED")