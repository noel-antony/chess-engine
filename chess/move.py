class Move:
    def __init__(self, start, end, promotion=None, special=None):
        self.start = start
        self.end = end

        self.moved_piece = None
        self.moved_piece_previous_has_moved = False

        self.promotion = promotion
        self.special = special

        self.castle_rook = None
        self.castle_rook_previous_has_moved = False

        self.captured_piece = None
        self.captured_position = None