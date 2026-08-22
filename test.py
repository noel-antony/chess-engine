from chess.board import Board
from chess.move import Move
from chess.piece import Piece

# test 1

# board = Board()

# print("Before:")
# print("e2:", board.position[6][4])
# print("e4:", board.position[4][4])

# move = Move((6, 4), (4, 4))
# board.make_move(move)

# print("\nAfter:")
# print("e2:", board.position[6][4])
# print("e4:", board.position[4][4])


# test 2

# board = Board()

# move = Move((6, 4), (4, 4))

# board.make_move(move)

# print("After move:")
# print("e2:", board.position[6][4])
# print("e4:", board.position[4][4])

# board.undo_move()

# print("After undo:")
# print("e2:", board.position[6][4])
# print("e4:", board.position[4][4])


# test 3

# board = Board()

# board.position[4][4] = Piece("black", "pawn")

# move = Move((6, 4), (4, 4))

# board.make_move(move)

# print("After capture:")
# print("e2:", board.position[6][4])
# print("e4:", board.position[4][4])
# print("Captured:", move.captured_piece)

# board.undo_move()

# print("After undo:")
# print("e2:", board.position[6][4])
# print("e4:", board.position[4][4])


# test 4

board = Board()

moves = board.generate_moves((7, 6)) 

for move in moves:
    print(move.start, "->", move.end)