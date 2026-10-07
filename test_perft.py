from chess.board import Board
from chess.piece import Piece


def perft(board, depth, color):

    if depth == 0:
        return 1

    moves = board.get_all_legal_moves(color)

    next_color = (
        "black"
        if color == "white"
        else "white"
    )

    nodes = 0

    for move in moves:

        board.make_move(move)

        nodes += perft(
            board,
            depth - 1,
            next_color
        )

        board.undo_move()

    return nodes


def load_fen(fen, board):

    parts = fen.split()

    # --------------------------------------------------
    # BOARD
    # --------------------------------------------------

    board.position = [
        [None for _ in range(8)]
        for _ in range(8)
    ]

    # --------------------------------------------------
    # TURN
    # --------------------------------------------------

    board.current_turn = (
        "white"
        if parts[1] == "w"
        else "black"
    )

    # --------------------------------------------------
    # MOVE HISTORY / STATE
    # --------------------------------------------------

    board.move_history = []
    board.state_stack = []

    # --------------------------------------------------
    # CASTLING RIGHTS
    # --------------------------------------------------

    rights = parts[2]

    board.castling_rights = {
        "white_kingside": "K" in rights,
        "white_queenside": "Q" in rights,
        "black_kingside": "k" in rights,
        "black_queenside": "q" in rights
    }

    # --------------------------------------------------
    # EN PASSANT
    # --------------------------------------------------

    if parts[3] == "-":

        board.en_passant_square = None

    else:

        file = ord(parts[3][0]) - ord("a")
        rank = int(parts[3][1])

        row = 8 - rank

        board.en_passant_square = (
            row,
            file
        )

    # --------------------------------------------------
    # PIECES
    # --------------------------------------------------

    piece_map = {
        "p": "pawn",
        "n": "knight",
        "b": "bishop",
        "r": "rook",
        "q": "queen",
        "k": "king"
    }

    for row, rank in enumerate(
        parts[0].split("/")
    ):

        col = 0

        for char in rank:

            if char.isdigit():

                col += int(char)

            else:

                color = (
                    "white"
                    if char.isupper()
                    else "black"
                )

                piece_type = piece_map[
                    char.lower()
                ]

                board.position[row][col] = Piece(
                    color,
                    piece_type
                )

                col += 1


# ======================================================
# STARTING POSITION
# ======================================================

board = Board()

for depth in range(1, 4):

    nodes = perft(
        board,
        depth,
        "white"
    )

    print(
        f"Depth {depth}: {nodes}"
    )


# ======================================================
# KIWIPETE
# ======================================================

KIWIPETE = (
    "r3k2r/"
    "p1ppqpb1/"
    "bn2pnp1/"
    "3PN3/"
    "1p2P3/"
    "2N2Q1p/"
    "PPPBBPPP/"
    "R3K2R "
    "w KQkq - 0 1"
)

board = Board()

load_fen(
    KIWIPETE,
    board
)

for depth in range(1, 4):

    nodes = perft(
        board,
        depth,
        board.current_turn
    )

    print(
        f"Kiwipete Depth {depth}: {nodes}"
    )