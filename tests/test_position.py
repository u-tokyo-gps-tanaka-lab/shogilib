from shogilib import (
    Player,
    Ptype,
    Piece,
    Position,
    BLACK,
    WHITE,
    can_promote_y,
    player2c,
    Move,
)
from shogilib import (
    KING,
    ROOK,
    BISHOP,
    GOLD,
    SILVER,
    PAWN,
    LANCE,
    KNIGHT,
    BLANK,
    king_checkmate_pawn,
)


def test_fen():
    fen = "l+s+pg3p1/s+p1P1b2N/r+p+p2PRL1/3ppgp2/3+p1+p1GS/1n2n+p+s2/1+b+pK3N1/+p2P4k/2+l1pLpg1[] w"
    pos = Position.from_fen(fen)
    assert pos.fen() == fen


def test_position_equal():
    fens = [
        "lnsgkgsnl/1r5b1/ppppppppp/9/9/9/PPPPPPPPP/1B5R1/LNSGKGSNL[-] w",
        "lnsgkgsnl/1r5b1/ppppppppp/9/9/9/PPPPPPPPP/1B5R1/LNSGKGSNL[-] b",
    ]
    for fen in fens:
        assert Position.from_fen(fen) == Position.from_fen(fen)


def test_position_in_dict():
    fens = [
        "lnsgkgsnl/1r5b1/ppppppppp/9/9/9/PPPPPPPPP/1B5R1/LNSGKGSNL[-] w",
        "lnsgkgsnl/1r5b1/ppppppppp/9/9/9/PPPPPPPPP/1B5R1/LNSGKGSNL[-] b",
    ]
    d = {}
    for fen in fens:
        pos = Position.from_fen(fen)
        d[pos] = 1
    for fen in fens:
        assert Position.from_fen(fen) in d


def test_is_consistent():
    p = Position.from_fen("4k4/9/9/9/9/9/9/9/n3K4[pppppppppPPPPllLLnNNssSSggGGbBrR] w")
    assert p.board[8][0] == KNIGHT.to_piece(BLACK)
    fens = [
        "lnsgkgsnl/1r5b1/ppppppppp/9/9/9/PPPPPPPPP/1B5R1/LNSGKGSNL[-] w",
        "lnsgkgsnl/1r5b1/ppppppppp/9/9/9/PPPPPPPPP/1B5R1/LNSGKGSNL[-] b",
    ]
    for fen in fens:
        p = Position.from_fen(fen)
        assert p.is_consistent()
    fens = [
        "lnsgkgsnl/1r5b1/ppppppppp/1p7/9/9/PPPPPPPPP/1B5R1/LNSGKGSNL[-] w",
        "lnsgkgsnl/1r5b1/ppppppppp/9/9/8P/PPPPPPP2/1B5R1/LNSGKGSNL[-] b",
    ]
    for fen in fens:
        print(f"fen={fen}")
        p = Position.from_fen(fen)
        assert not p.is_consistent()


def test_legal_piece_positions():
    # pawn that has no place to go
    for p in [
        "Pnsgkgsnl/1r5b1/ppppppppp/9/9/9/1PPPPPPPP/1B5R1/LNSGKGSNL[l] w",
        "Pnsgkgsnl/1r5b1/ppppppppp/9/9/9/1PPPPPPPP/1B5R1/LNSGKGSNL[l] b",
        "1nsgkgsnl/1r5b1/ppppppppp/9/9/9/1PPPPPPPP/1B5R1/pNSGKGSNL[Ll] w",
        "1nsgkgsnl/1r5b1/ppppppppp/9/9/9/1PPPPPPPP/1B5R1/pNSGKGSNL[Ll] b",
    ]:
        pos = Position.from_fen(p)
        assert not pos.legal_piece_positions()
        assert pos.fen() == p

    # lance that has no place to go
    for p in [
        "Lnsgkgsnl/1r5b1/1pppppppp/9/9/9/1PPPPPPPP/1B5R1/LNSGKGSNL[lp] w",
        "Lnsgkgsnl/1r5b1/1pppppppp/9/9/9/1PPPPPPPP/1B5R1/LNSGKGSNL[lp] b",
        "1nsgkgsnl/1r5b1/ppppppppp/9/9/9/1PPPPPPPP/1B5R1/lNSGKGSNL[lLp] w",
        "1nsgkgsnl/1r5b1/ppppppppp/9/9/9/1PPPPPPPP/1B5R1/lNSGKGSNL[plL] b",
    ]:
        assert not Position.from_fen(p).legal_piece_positions()
    for p in [
        "N3k4/9/9/9/9/9/9/9/4K4[pppppppppPPPPllLLnNNssSSggGGbBrR] w",
        "N3k4/9/9/9/9/9/9/9/4K4[pppppppppPPPPllLLnNNssSSggGGbBrR] b",
        "4k4/1N7/9/9/9/9/9/9/4K4[pppppppppPPPPllLLnNNssSSggGGbBrR] w",
        "4k4/1N7/9/9/9/9/9/9/4K4[pppppppppPPPPllLLnNNssSSggGGbBrR] b",
        "4k4/9/9/9/9/9/9/9/n3K4[pppppppppPPPPllLLnNNssSSggGGbBrR] w",
        "4k4/9/9/9/9/9/9/9/n3K4[pppppppppPPPPllLLnNNssSSggGGbBrR] b",
    ]:
        assert not Position.from_fen(p).legal_piece_positions()

    # Two pawns
    for p in [
        "1nsgkgsnl/Pr5b1/ppppppppp/9/9/9/P1PPPPPPP/1B5R1/LNSGKGSNL[l] w",
        "1nsgkgsnl/Pr5b1/ppppppppp/9/9/9/P1PPPPPPP/1B5R1/LNSGKGSNL[l] b",
        "pnsgkgsnl/1r5b1/ppppppppp/9/9/9/P1PPPPPPP/1B5R1/LNSGKGSNL[l] w",
        "pnsgkgsnl/1r5b1/ppppppppp/9/9/9/P1PPPPPPP/1B5R1/LNSGKGSNL[l] b",
    ]:
        assert not Position.from_fen(p).legal_piece_positions()


def test_king_pos():
    pos = Position.from_fen(
        "Pnsgkgsnl/1r5b1/ppppppppp/9/9/9/1PPPPPPPP/1B5R1/LNSGKGSNL[l] w"
    )
    assert pos.king_pos(WHITE) == (8, 4)
    assert pos.king_pos(BLACK) == (0, 4)


def test_in_check():
    pos = Position.from_fen(
        "r7g1/P6Gk/1pppppppp/9/9/2N7/1PPPPPPPP/9/K2R1[lllLnnNPbGGGGggssss] w"
    )
    assert pos.in_check(BLACK)
    assert not pos.in_check(WHITE)


def test_apply_move():
    pos = Position.from_fen(
        "r7g/P7k/1pppppppp/9/9/2N6/1PPPPPPPP/9/KG1R5[lllLnnNPbGGGGggssss] w"
    )
    pos1 = pos.apply_move(WHITE, Move.from_uci("a1a2"))
    fen1 = pos1.fen()
    assert fen1 == "r7g/P7k/1pppppppp/9/9/2N6/1PPPPPPPP/K8/1G1R5[GGGGNLPggnnlllssssb] b"


def test_apply_unmove():
    pos = Position.from_fen(
        "r7g/P7k/1pppppppp/9/2N6/9/P1PPPPPPP/9/KG1R5[lllLnnNPbbggssss] b"
    )
    assert pos.is_consistent()
    pos1 = pos.apply_unmove(WHITE, Move.from_uci("b3c5"), KNIGHT.to_piece(BLACK))
    fen1 = pos1.fen()
    assert fen1 == "r7g/P7k/1pppppppp/9/2n6/9/PNPPPPPPP/9/KG1R5[LPggnnlllssssbb] w"


def test_checkmate():
    pos = Position.from_fen(
        "r7g/R8/1kppppppp/9/1PNG5/9/L1P1PPPPP/9/KG16[llLnnNPPPbGGGggssss] b"
    )
    assert pos.in_check(BLACK)
    assert pos.in_checkmate()


def test_king_checkmate_pawn():
    pos = Position.from_fen(
        "r7g/P5G1k/1pppppppP/8G/2N6/9/P1PPPPPPp/9/KG1R5[lllLnnNPbbssss] b"
    )
    assert king_checkmate_pawn(pos, 2, 8)
