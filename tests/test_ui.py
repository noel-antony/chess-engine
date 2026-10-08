from chess.board import Board

b = Board()
moves = b.generate_legal_moves(6, 4) # e2 pawn
for m in moves:
    print(m.start, m.end, m.promotion)

end = (4, 4)
move = next((m for m in moves if m.end == end and m.promotion == None), None)
print("Found move:", move)

b.make_move(move)
print("Move made!")
