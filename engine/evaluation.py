WHITE = "white"
BLACK = "black"

PIECE_VALUES = {
    "pawn": 100,
    "knight": 320,
    "bishop": 330,
    "rook": 500,
    "queen": 900,
    "king": 0,
}

PAWN_TABLE = [
    0, 0, 0, 0, 0, 0, 0, 0,
    50, 50, 50, 50, 50, 50, 50, 50,
    10, 10, 20, 30, 30, 20, 10, 10,
    5, 5, 10, 25, 25, 10, 5, 5,
    0, 0, 0, 20, 20, 0, 0, 0,
    5, -5, -10, 0, 0, -10, -5, 5,
    5, 10, 10, -20, -20, 10, 10, 5,
    0, 0, 0, 0, 0, 0, 0, 0,
]

KNIGHT_TABLE = [
    -50, -40, -30, -30, -30, -30, -40, -50,
    -40, -20, 0, 5, 5, 0, -20, -40,
    -30, 5, 10, 15, 15, 10, 5, -30,
    -30, 0, 15, 20, 20, 15, 0, -30,
    -30, 5, 15, 20, 20, 15, 5, -30,
    -30, 0, 10, 15, 15, 10, 0, -30,
    -40, -20, 0, 0, 0, 0, -20, -40,
    -50, -40, -30, -30, -30, -30, -40, -50,
]

BISHOP_TABLE = [
    -20, -10, -10, -10, -10, -10, -10, -20,
    -10, 5, 0, 0, 0, 0, 5, -10,
    -10, 10, 10, 10, 10, 10, 10, -10,
    -10, 0, 10, 10, 10, 10, 0, -10,
    -10, 5, 5, 10, 10, 5, 5, -10,
    -10, 0, 5, 10, 10, 5, 0, -10,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -20, -10, -10, -10, -10, -10, -10, -20,
]

ROOK_TABLE = [
    0, 0, 0, 5, 5, 0, 0, 0,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    5, 10, 10, 10, 10, 10, 10, 5,
    0, 0, 0, 0, 0, 0, 0, 0,
]

QUEEN_TABLE = [
    -20, -10, -10, -5, -5, -10, -10, -20,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -10, 0, 5, 5, 5, 5, 0, -10,
    -5, 0, 5, 5, 5, 5, 0, -5,
    0, 0, 5, 5, 5, 5, 0, -5,
    -10, 5, 5, 5, 5, 5, 0, -10,
    -10, 0, 5, 0, 0, 0, 0, -10,
    -20, -10, -10, -5, -5, -10, -10, -20,
]

KING_MG_TABLE = [
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -20, -30, -30, -40, -40, -30, -30, -20,
    -10, -20, -20, -20, -20, -20, -20, -10,
    20, 20, 0, 0, 0, 0, 20, 20,
    20, 30, 10, 0, 0, 10, 30, 20,
]

KING_EG_TABLE = [
    -50, -40, -30, -20, -20, -30, -40, -50,
    -30, -20, -10, 0, 0, -10, -20, -30,
    -30, -10, 20, 30, 30, 20, -10, -30,
    -30, -10, 30, 40, 40, 30, -10, -30,
    -30, -10, 30, 40, 40, 30, -10, -30,
    -30, -10, 20, 30, 30, 20, -10, -30,
    -30, -30, 0, 0, 0, 0, -30, -30,
    -50, -30, -30, -30, -30, -30, -30, -50,
]

MG_TABLES = {
    "pawn": PAWN_TABLE,
    "knight": KNIGHT_TABLE,
    "bishop": BISHOP_TABLE,
    "rook": ROOK_TABLE,
    "queen": QUEEN_TABLE,
    "king": KING_MG_TABLE,
}

EG_TABLES = {
    "pawn": PAWN_TABLE,
    "knight": KNIGHT_TABLE,
    "bishop": BISHOP_TABLE,
    "rook": ROOK_TABLE,
    "queen": QUEEN_TABLE,
    "king": KING_EG_TABLE,
}

def _build_pst(tables):
    out = {
        WHITE: {},
        BLACK: {},
    }

    for piece_type, table in tables.items():
        white = [0] * 64
        black = [0] * 64
        value = PIECE_VALUES[piece_type]

        for row in range(8):
            for col in range(8):
                sq = row * 8 + col
                white[sq] = value + table[sq]
                black[sq] = -(value + table[(7 - row) * 8 + col])

        out[WHITE][piece_type] = white
        out[BLACK][piece_type] = black

    return out

PST_MG = _build_pst(MG_TABLES)
PST_EG = _build_pst(EG_TABLES)

PHASE_WEIGHT = {
    "knight": 1,
    "bishop": 1,
    "rook": 2,
    "queen": 4,
}

MAX_PHASE = 24

KNIGHT_OFFSETS = [
    (-2, -1),
    (-2, 1),
    (-1, -2),
    (-1, 2),
    (1, -2),
    (1, 2),
    (2, -1),
    (2, 1),
]

ROOK_DIRS = [
    (-1, 0),
    (1, 0),
    (0, -1),
    (0, 1),
]

BISHOP_DIRS = [
    (-1, -1),
    (-1, 1),
    (1, -1),
    (1, 1),
]

QUEEN_DIRS = ROOK_DIRS + BISHOP_DIRS

SLIDER_DIRS = {
    "bishop": BISHOP_DIRS,
    "rook": ROOK_DIRS,
    "queen": QUEEN_DIRS,
}

MOBILITY = {
    "knight": (4, 4, 4),
    "bishop": (5, 3, 3),
    "rook": (5, 2, 4),
    "queen": (9, 1, 2),
}

ATTACK_WEIGHT = {
    "knight": 2,
    "bishop": 2,
    "rook": 3,
    "queen": 5,
}

PASSED_MG = [0, 2, 5, 10, 20, 35, 60]
PASSED_EG = [0, 5, 12, 25, 45, 75, 110]


class Evaluator:

    TEMPO = 10

    BISHOP_PAIR = (30, 50)

    DOUBLED_PAWN = (10, 20)
    ISOLATED_PAWN = (12, 18)

    SUPPORTED_PAWN = (6, 4)
    PHALANX_PAWN = (4, 3)

    ROOK_OPEN_FILE = (20, 10)
    ROOK_SEMI_OPEN_FILE = (10, 5)

    ROOK_SEVENTH = (10, 20)

    KNIGHT_OUTPOST = (18, 10)

    MAX_KING_DANGER = 300

    def evaluate(self, board, side_to_move=None):
        pos = board.position

        mg = 0
        eg = 0
        phase = 0

        white_pawns = [[] for _ in range(8)]
        black_pawns = [[] for _ in range(8)]

        kings = {
            WHITE: None,
            BLACK: None,
        }

        count = {
            WHITE: {
                "pawn": 0,
                "knight": 0,
                "bishop": 0,
                "rook": 0,
                "queen": 0,
            },
            BLACK: {
                "pawn": 0,
                "knight": 0,
                "bishop": 0,
                "rook": 0,
                "queen": 0,
            },
        }

        bishop_shade = {
            WHITE: [],
            BLACK: [],
        }

        pieces = []

        for row in range(8):
            line = pos[row]

            for col in range(8):
                piece = line[col]

                if piece is None:
                    continue

                color = piece.color
                piece_type = piece.piece_type
                square = row * 8 + col

                mg += PST_MG[color][piece_type][square]
                eg += PST_EG[color][piece_type][square]

                if piece_type == "pawn":
                    if color == WHITE:
                        white_pawns[col].append(row)
                    else:
                        black_pawns[col].append(row)

                    count[color]["pawn"] += 1

                elif piece_type == "king":
                    kings[color] = (row, col)

                else:
                    count[color][piece_type] += 1
                    phase += PHASE_WEIGHT[piece_type]

                    pieces.append(
                        (color, piece_type, row, col)
                    )

                    if piece_type == "bishop":
                        bishop_shade[color].append(
                            (row + col) & 1
                        )

        if self._insufficient_material(count):
            return 0

        pawn_mg, pawn_eg = self._pawn_structure(
            pos,
            white_pawns,
            black_pawns,
            kings
        )

        mg += pawn_mg
        eg += pawn_eg

        white_pawn_attacks = set()
        black_pawn_attacks = set()

        for file in range(8):
            for row in white_pawns[file]:
                if row > 0:
                    if file > 0:
                        white_pawn_attacks.add(
                            (row - 1) * 8 + file - 1
                        )

                    if file < 7:
                        white_pawn_attacks.add(
                            (row - 1) * 8 + file + 1
                        )

            for row in black_pawns[file]:
                if row < 7:
                    if file > 0:
                        black_pawn_attacks.add(
                            (row + 1) * 8 + file - 1
                        )

                    if file < 7:
                        black_pawn_attacks.add(
                            (row + 1) * 8 + file + 1
                        )

        zones = {
            WHITE: self._king_zone(
                WHITE,
                kings[WHITE]
            ),
            BLACK: self._king_zone(
                BLACK,
                kings[BLACK]
            ),
        }

        attackers = {
            WHITE: 0,
            BLACK: 0,
        }

        attack_units = {
            WHITE: 0,
            BLACK: 0,
        }

        zone_hits = {
            WHITE: 0,
            BLACK: 0,
        }

        for color, piece_type, row, col in pieces:
            white = color == WHITE
            enemy = BLACK if white else WHITE

            if white:
                own_pawns = white_pawns
                opp_pawns = black_pawns
                enemy_pawn_attacks = black_pawn_attacks
            else:
                own_pawns = black_pawns
                opp_pawns = white_pawns
                enemy_pawn_attacks = white_pawn_attacks

            enemy_zone = zones[enemy]
            mobility = 0
            hits = 0

            if piece_type == "knight":
                for dr, dc in KNIGHT_OFFSETS:
                    nr = row + dr
                    nc = col + dc

                    if not (0 <= nr < 8 and 0 <= nc < 8):
                        continue

                    square = nr * 8 + nc

                    if (
                        enemy_zone is not None
                        and square in enemy_zone
                    ):
                        hits += 1

                    target = pos[nr][nc]

                    if target is not None and target.color == color:
                        continue

                    if square in enemy_pawn_attacks:
                        continue

                    mobility += 1

            else:
                for dr, dc in SLIDER_DIRS[piece_type]:
                    nr = row + dr
                    nc = col + dc

                    while 0 <= nr < 8 and 0 <= nc < 8:
                        square = nr * 8 + nc

                        if (
                            enemy_zone is not None
                            and square in enemy_zone
                        ):
                            hits += 1

                        target = pos[nr][nc]

                        if target is None:
                            if square not in enemy_pawn_attacks:
                                mobility += 1
                        else:
                            if (
                                target.color != color
                                and square not in enemy_pawn_attacks
                            ):
                                mobility += 1

                            break

                        nr += dr
                        nc += dc

            base, mg_weight, eg_weight = MOBILITY[piece_type]

            score_mg = (
                (mobility - base)
                * mg_weight
            )

            score_eg = (
                (mobility - base)
                * eg_weight
            )

            if piece_type == "rook":
                if not own_pawns[col]:
                    if not opp_pawns[col]:
                        score_mg += self.ROOK_OPEN_FILE[0]
                        score_eg += self.ROOK_OPEN_FILE[1]
                    else:
                        score_mg += self.ROOK_SEMI_OPEN_FILE[0]
                        score_eg += self.ROOK_SEMI_OPEN_FILE[1]

                seventh_rank = 1 if white else 6

                if row == seventh_rank:
                    enemy_king = kings[enemy]
                    enemy_back_rank = 0 if white else 7

                    if (
                        enemy_king is not None
                        and enemy_king[0] == enemy_back_rank
                    ):
                        score_mg += self.ROOK_SEVENTH[0]
                        score_eg += self.ROOK_SEVENTH[1]

                    elif any(
                        seventh_rank in opp_pawns[file]
                        for file in range(8)
                    ):
                        score_mg += self.ROOK_SEVENTH[0]
                        score_eg += self.ROOK_SEVENTH[1]

            elif piece_type == "knight":
                advancement = 7 - row if white else row

                if 3 <= advancement <= 5:
                    adjacent_files = [
                        f
                        for f in (col - 1, col + 1)
                        if 0 <= f < 8
                    ]

                    if white:
                        kickable = any(
                            opp_pawns[f]
                            and opp_pawns[f][0] < row
                            for f in adjacent_files
                        )

                        supported = any(
                            (row + 1) in own_pawns[f]
                            for f in adjacent_files
                        )

                    else:
                        kickable = any(
                            opp_pawns[f]
                            and opp_pawns[f][-1] > row
                            for f in adjacent_files
                        )

                        supported = any(
                            (row - 1) in own_pawns[f]
                            for f in adjacent_files
                        )

                    if supported and not kickable:
                        score_mg += self.KNIGHT_OUTPOST[0]
                        score_eg += self.KNIGHT_OUTPOST[1]

            if hits:
                attackers[color] += 1
                attack_units[color] += ATTACK_WEIGHT[piece_type]
                zone_hits[color] += hits

            if white:
                mg += score_mg
                eg += score_eg
            else:
                mg -= score_mg
                eg -= score_eg

        for defender in (WHITE, BLACK):
            king = kings[defender]

            if king is None:
                continue

            attacker = BLACK if defender == WHITE else WHITE

            if defender == WHITE:
                own_pawns = white_pawns
                opp_pawns = black_pawns
            else:
                own_pawns = black_pawns
                opp_pawns = white_pawns

            safety = self._pawn_shield(
                defender,
                king,
                own_pawns,
                opp_pawns
            )

            if attackers[attacker] >= 2:
                danger = (
                    4 * attack_units[attacker]
                    + 2 * zone_hits[attacker]
                )

                penalty = min(
                    self.MAX_KING_DANGER,
                    danger * danger // 64
                )

                if count[attacker]["queen"] == 0:
                    penalty //= 2

                safety -= penalty

            if defender == WHITE:
                mg += safety
            else:
                mg -= safety

        if count[WHITE]["bishop"] >= 2:
            mg += self.BISHOP_PAIR[0]
            eg += self.BISHOP_PAIR[1]

        if count[BLACK]["bishop"] >= 2:
            mg -= self.BISHOP_PAIR[0]
            eg -= self.BISHOP_PAIR[1]

        eg += self._mop_up(
            count,
            kings
        )

        phase = min(
            MAX_PHASE,
            phase
        )

        score = (
            mg * phase
            + eg * (MAX_PHASE - phase)
        )

        score //= MAX_PHASE

        if (
            count[WHITE]["bishop"] == 1
            and count[BLACK]["bishop"] == 1
            and count[WHITE]["knight"] == 0
            and count[BLACK]["knight"] == 0
            and count[WHITE]["rook"] == 0
            and count[BLACK]["rook"] == 0
            and count[WHITE]["queen"] == 0
            and count[BLACK]["queen"] == 0
            and bishop_shade[WHITE][0]
            != bishop_shade[BLACK][0]
        ):
            score = int(score / 2)

        if side_to_move == WHITE:
            score += self.TEMPO
        elif side_to_move == BLACK:
            score -= self.TEMPO

        return score

    def evaluate_relative(self, board, side_to_move):
        score = self.evaluate(
            board,
            side_to_move
        )

        if side_to_move == WHITE:
            return score

        return -score

    def _insufficient_material(self, count):
        for color in (WHITE, BLACK):
            pieces = count[color]

            if (
                pieces["pawn"]
                or pieces["rook"]
                or pieces["queen"]
            ):
                return False

        white_minor = (
            count[WHITE]["knight"]
            + count[WHITE]["bishop"]
        )

        black_minor = (
            count[BLACK]["knight"]
            + count[BLACK]["bishop"]
        )

        if white_minor <= 1 and black_minor <= 1:
            return True

        if (
            black_minor == 0
            and count[WHITE]["knight"] == 2
            and white_minor == 2
        ):
            return True

        if (
            white_minor == 0
            and count[BLACK]["knight"] == 2
            and black_minor == 2
        ):
            return True

        return False

    def _king_zone(self, color, king):
        if king is None:
            return None

        king_row, king_col = king

        forward = -1 if color == WHITE else 1
        zone = set()

        for row in (
            king_row - 1,
            king_row,
            king_row + 1,
            king_row + 2 * forward
        ):
            if not (0 <= row < 8):
                continue

            for col in range(
                max(0, king_col - 1),
                min(7, king_col + 1) + 1
            ):
                zone.add(row * 8 + col)

        return zone

    def _pawn_shield(
        self,
        color,
        king,
        own_pawns,
        opp_pawns
    ):
        king_row, king_col = king
        white = color == WHITE

        if (
            white and king_row < 6
        ) or (
            not white and king_row > 1
        ):
            return 0

        score = 0

        for file in range(
            max(0, king_col - 1),
            min(7, king_col + 1) + 1
        ):
            rows = own_pawns[file]

            if white:
                ahead = [
                    r
                    for r in rows
                    if r < king_row
                ]

                distance = (
                    king_row - ahead[-1]
                    if ahead
                    else 0
                )

            else:
                ahead = [
                    r
                    for r in rows
                    if r > king_row
                ]

                distance = (
                    ahead[0] - king_row
                    if ahead
                    else 0
                )

            if distance == 1:
                score += 12
            elif distance == 2:
                score += 8
            elif distance == 3:
                score += 2
            else:
                score -= 15

                if not opp_pawns[file]:
                    score -= 10

        return score

    def _pawn_structure(
        self,
        pos,
        white_pawns,
        black_pawns,
        kings
    ):
        mg = 0
        eg = 0

        for color in (WHITE, BLACK):
            white = color == WHITE

            if white:
                own = white_pawns
                opp = black_pawns
                own_king = kings[WHITE]
                enemy_king = kings[BLACK]
                sign = 1
                promotion_row = 0
            else:
                own = black_pawns
                opp = white_pawns
                own_king = kings[BLACK]
                enemy_king = kings[WHITE]
                sign = -1
                promotion_row = 7

            score_mg = 0
            score_eg = 0

            for file in range(8):
                rows = own[file]

                if not rows:
                    continue

                pawn_count = len(rows)

                if pawn_count > 1:
                    score_mg -= (
                        self.DOUBLED_PAWN[0]
                        * (pawn_count - 1)
                    )

                    score_eg -= (
                        self.DOUBLED_PAWN[1]
                        * (pawn_count - 1)
                    )

                left = (
                    own[file - 1]
                    if file > 0
                    else ()
                )

                right = (
                    own[file + 1]
                    if file < 7
                    else ()
                )

                isolated = (
                    not left
                    and not right
                )

                low_file = max(
                    0,
                    file - 1
                )

                high_file = min(
                    7,
                    file + 1
                )

                for row in rows:
                    if isolated:
                        score_mg -= self.ISOLATED_PAWN[0]
                        score_eg -= self.ISOLATED_PAWN[1]

                    behind = (
                        row + 1
                        if white
                        else row - 1
                    )

                    if (
                        behind in left
                        or behind in right
                    ):
                        score_mg += self.SUPPORTED_PAWN[0]
                        score_eg += self.SUPPORTED_PAWN[1]

                    elif (
                        row in left
                        or row in right
                    ):
                        score_mg += self.PHALANX_PAWN[0]
                        score_eg += self.PHALANX_PAWN[1]

                    if white:
                        if row != rows[0]:
                            continue

                        passed = all(
                            (
                                not opp[file_index]
                                or opp[file_index][0] >= row
                            )
                            for file_index in range(
                                low_file,
                                high_file + 1
                            )
                        )

                    else:
                        if row != rows[-1]:
                            continue

                        passed = all(
                            (
                                not opp[file_index]
                                or opp[file_index][-1] <= row
                            )
                            for file_index in range(
                                low_file,
                                high_file + 1
                            )
                        )

                    if not passed:
                        continue

                    advancement = (
                        7 - row
                        if white
                        else row
                    )

                    bonus_mg = PASSED_MG[advancement]
                    bonus_eg = PASSED_EG[advancement]

                    ahead_row = (
                        row - 1
                        if white
                        else row + 1
                    )

                    if 0 <= ahead_row < 8:
                        if pos[ahead_row][file] is not None:
                            bonus_mg //= 2
                            bonus_eg //= 2

                    if (
                        advancement >= 3
                        and own_king is not None
                        and enemy_king is not None
                    ):
                        own_distance = max(
                            abs(
                                own_king[0]
                                - promotion_row
                            ),
                            abs(
                                own_king[1]
                                - file
                            )
                        )

                        enemy_distance = max(
                            abs(
                                enemy_king[0]
                                - promotion_row
                            ),
                            abs(
                                enemy_king[1]
                                - file
                            )
                        )

                        bonus_eg += (
                            enemy_distance
                            - own_distance
                        ) * (
                            advancement - 2
                        )

                    score_mg += bonus_mg
                    score_eg += bonus_eg

            mg += sign * score_mg
            eg += sign * score_eg

        return mg, eg

    def _mop_up(self, count, kings):
        non_pawn_material = {}

        for color in (WHITE, BLACK):
            pieces = count[color]

            non_pawn_material[color] = (
                pieces["knight"] * PIECE_VALUES["knight"]
                + pieces["bishop"] * PIECE_VALUES["bishop"]
                + pieces["rook"] * PIECE_VALUES["rook"]
                + pieces["queen"] * PIECE_VALUES["queen"]
            )

        material_difference = (
            non_pawn_material[WHITE]
            - non_pawn_material[BLACK]
        )

        if (
            material_difference >= 300
            and count[BLACK]["pawn"] == 0
        ):
            winner = WHITE
            loser = BLACK
            sign = 1

        elif (
            -material_difference >= 300
            and count[WHITE]["pawn"] == 0
        ):
            winner = BLACK
            loser = WHITE
            sign = -1

        else:
            return 0

        winning_king = kings[winner]
        losing_king = kings[loser]

        if (
            winning_king is None
            or losing_king is None
        ):
            return 0

        centre_distance = (
            max(
                3 - losing_king[0],
                losing_king[0] - 4
            )
            + max(
                3 - losing_king[1],
                losing_king[1] - 4
            )
        )

        king_distance = (
            abs(
                winning_king[0]
                - losing_king[0]
            )
            + abs(
                winning_king[1]
                - losing_king[1]
            )
        )

        return sign * (
            10 * centre_distance
            + 4 * (14 - king_distance)
        )
