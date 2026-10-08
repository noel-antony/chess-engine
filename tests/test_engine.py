from chess.board import Board
from engine.agent import ChessAgent
from engine.evaluation import Evaluator

def test_initial_state():
    b = Board()
    assert b.current_turn == "white"
    assert b.is_in_check("white") == False
    assert b.is_in_check("black") == False
    print("PASS: Initial state is correct.")

def test_move_generation_count():
    b = Board()
    # white moves
    moves = []
    for r in range(8):
        for c in range(8):
            p = b.position[r][c]
            if p and p.color == "white":
                moves.extend(b.generate_legal_moves(r, c))
    assert len(moves) == 20
    print("PASS: Initial legal moves count (20) is correct.")

def test_checkmate():
    b = Board()
    # Fool's mate
    # 1. f3
    m1 = next((m for m in b.generate_legal_moves(6, 5) if m.end == (5, 5)), None)
    b.make_move(m1)
    b.current_turn = "black"
    # 1... e5
    m2 = next((m for m in b.generate_legal_moves(1, 4) if m.end == (3, 4)), None)
    b.make_move(m2)
    b.current_turn = "white"
    # 2. g4
    m3 = next((m for m in b.generate_legal_moves(6, 6) if m.end == (4, 6)), None)
    b.make_move(m3)
    b.current_turn = "black"
    # 2... Qh4#
    m4 = next((m for m in b.generate_legal_moves(0, 3) if m.end == (4, 7)), None)
    b.make_move(m4)
    b.current_turn = "white"
    
    assert b.is_in_check("white") == True
    assert b.is_checkmate("white") == True
    print("PASS: Checkmate detected successfully (Fool's Mate).")

def test_en_passant():
    b = Board()
    # 1. e4
    b.make_move(next((m for m in b.generate_legal_moves(6, 4) if m.end == (4, 4)), None))
    b.current_turn = "black"
    # 1... a6
    b.make_move(next((m for m in b.generate_legal_moves(1, 0) if m.end == (2, 0)), None))
    b.current_turn = "white"
    # 2. e5
    b.make_move(next((m for m in b.generate_legal_moves(4, 4) if m.end == (3, 4)), None))
    b.current_turn = "black"
    # 2... d5
    b.make_move(next((m for m in b.generate_legal_moves(1, 3) if m.end == (3, 3)), None))
    b.current_turn = "white"
    
    # Check en passant
    moves = b.generate_legal_moves(3, 4) # white pawn on e5
    ep_move = next((m for m in moves if m.special == "en_passant"), None)
    assert ep_move is not None
    assert ep_move.end == (2, 3)
    print("PASS: En Passant move generated correctly.")
    
def test_evaluation():
    b = Board()
    evaluator = Evaluator()
    score = evaluator.evaluate(b)
    assert score == 0 # initial board is symmetric
    print("PASS: Evaluation function works and is symmetric.")

def test_minimax():
    b = Board()
    # White has Mate in 1 (Scholar's mate)
    # Setup: 1. e4 e5 2. Bc4 Nc6 3. Qh5 Nf6??
    b.make_move(next((m for m in b.generate_legal_moves(6, 4) if m.end == (4, 4)))) # e4
    b.current_turn = "black"
    b.make_move(next((m for m in b.generate_legal_moves(1, 4) if m.end == (3, 4)))) # e5
    b.current_turn = "white"
    b.make_move(next((m for m in b.generate_legal_moves(7, 5) if m.end == (4, 2)))) # Bc4
    b.current_turn = "black"
    b.make_move(next((m for m in b.generate_legal_moves(0, 1) if m.end == (2, 2)))) # Nc6
    b.current_turn = "white"
    b.make_move(next((m for m in b.generate_legal_moves(7, 3) if m.end == (3, 7)))) # Qh5
    b.current_turn = "black"
    b.make_move(next((m for m in b.generate_legal_moves(0, 6) if m.end == (2, 5)))) # Nf6
    b.current_turn = "white"
    
    ai = ChessAgent(depth=2)
    best_move = ai.get_move(b)
    # White should play Qxf7#
    assert best_move.start == (3, 7) # Qh5
    assert best_move.end == (1, 5) # f7
    print("PASS: Minimax correctly finds Mate in 1.")

def run_all():
    print("Running Automated Engine Tests...")
    print("=================================")
    tests = [test_initial_state, test_move_generation_count, test_checkmate, test_en_passant, test_evaluation, test_minimax]
    passed = 0
    for t in tests:
        try:
            t()
            passed += 1
        except AssertionError:
            print(f"FAIL: {t.__name__}")
        except Exception as e:
            print(f"ERROR in {t.__name__}: {e}")
    
    print("=================================")
    print(f"--- Test Results: {passed}/{len(tests)} PASS ---")

if __name__ == '__main__':
    run_all()
