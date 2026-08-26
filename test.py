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