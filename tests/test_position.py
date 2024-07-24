from shogilib import Player, Ptype, Piece, Position, BLACK, WHITE, can_promote_y, player2c, Move
from shogilib import KING, ROOK, BISHOP, GOLD, SILVER, PAWN, LANCE, KNIGHT, BLANK, king_checkmate_pawn

def test_player():
    assert WHITE.value == 0
    assert BLACK.value == 1
    assert BLACK == WHITE.flip()
    assert WHITE == BLACK.flip()

def test_player2c():
    assert player2c(WHITE) == 'w'
    assert player2c(BLACK) == 'b'

def test_player_can_promote_y():
    for y in range(3):
        assert can_promote_y(WHITE, y)
    for y in range(3, 9):
        assert not can_promote_y(WHITE, y)
    for y in range(6):
        assert not can_promote_y(BLACK, y)
    for y in range(6, 9):
        assert can_promote_y(BLACK, y)

def test_ptype_promote():
    for pt in [PAWN, LANCE, KNIGHT, SILVER, BISHOP, ROOK]:
        assert pt.can_promote()
        assert not pt.is_promoted()
        assert pt.promote().is_promoted()
        assert pt.promote().unpromote() == pt
    for pt in [KING, GOLD]:
        assert not pt.can_promote()
        assert not pt.is_promoted()
def test_must_promote_y():
    assert PAWN.must_promote_y(WHITE, 0)
    assert PAWN.must_promote_y(BLACK, 8)
    assert not PAWN.must_promote_y(WHITE, 1)
    assert not PAWN.must_promote_y(BLACK, 7)
    assert LANCE.must_promote_y(WHITE, 0)
    assert LANCE.must_promote_y(BLACK, 8)
    assert not LANCE.must_promote_y(WHITE, 1)
    assert not LANCE.must_promote_y(BLACK, 7)
    assert KNIGHT.must_promote_y(WHITE, 0)
    assert KNIGHT.must_promote_y(BLACK, 8)
    assert KNIGHT.must_promote_y(WHITE, 1)
    assert KNIGHT.must_promote_y(BLACK, 7)
    assert not KNIGHT.must_promote_y(WHITE, 2)
    assert not KNIGHT.must_promote_y(BLACK, 6)


def test_piece():
    for pl in [BLACK, WHITE]:
        for pt in [PAWN, LANCE, KNIGHT, SILVER, BISHOP, ROOK]:
            p = pt.to_piece(pl)
            assert p.player() == pl
            assert p.ptype() == pt
            assert not p.is_promoted()
            assert p.promote().is_promoted()
            assert p.promote().unpromote() == p
        for pt in [KING, GOLD]:
            p = pt.to_piece(pl)
            assert p.player() == pl
            assert p.ptype() == pt
            assert not p.is_promoted()

def test_piece_fen():
    for pl in [BLACK, WHITE]:
        for pt, c in [(PAWN, 'p'), (LANCE, 'l'), (KNIGHT, 'n'), (SILVER, 's'), (BISHOP, 'b'), (ROOK, 'r'), (GOLD, 'g'), (KING, 'k')]:
            p = pt.to_piece(pl)
            fen = p.fen()
            if p.ptype().can_promote():
                pfen = p.promote().fen()
            if pl == BLACK:
                assert fen == c
                if p.ptype().can_promote():
                    assert pfen == '+' + c 
            else:
                assert fen == c.upper()
                if p.ptype().can_promote():
                    assert pfen == '+' + c.upper()

def test_position_equal():
    fens = ['lnsgkgsnl/1r5b1/ppppppppp/9/9/9/PPPPPPPPP/1B5R1/LNSGKGSNL[-] w', 'lnsgkgsnl/1r5b1/ppppppppp/9/9/9/PPPPPPPPP/1B5R1/LNSGKGSNL[-] b']
    for fen in fens:
        assert Position.from_fen(fen) == Position.from_fen(fen)

def test_position_in_dict():
    fens = ['lnsgkgsnl/1r5b1/ppppppppp/9/9/9/PPPPPPPPP/1B5R1/LNSGKGSNL[-] w', 'lnsgkgsnl/1r5b1/ppppppppp/9/9/9/PPPPPPPPP/1B5R1/LNSGKGSNL[-] b']
    d = {}
    for fen in fens:
        pos = Position.from_fen(fen)
        d[pos] = 1
    for fen in fens:
        assert Position.from_fen(fen) in d                    

def test_is_consistent():
    p = Position.from_fen('4k4/9/9/9/9/9/9/9/n3K4[pppppppppPPPPllLLnNNssSSggGGbBrR] w')
    assert p.board[8][0] == KNIGHT.to_piece(BLACK)
    fens = ['lnsgkgsnl/1r5b1/ppppppppp/9/9/9/PPPPPPPPP/1B5R1/LNSGKGSNL[-] w', 'lnsgkgsnl/1r5b1/ppppppppp/9/9/9/PPPPPPPPP/1B5R1/LNSGKGSNL[-] b']
    for fen in fens:
        p = Position.from_fen(fen)
        assert p.is_consistent()
    fens = ['lnsgkgsnl/1r5b1/ppppppppp/1p7/9/9/PPPPPPPPP/1B5R1/LNSGKGSNL[-] w', 'lnsgkgsnl/1r5b1/ppppppppp/9/9/8P/PPPPPPP2/1B5R1/LNSGKGSNL[-] b']
    for fen in fens:
        print(f'fen={fen}')
        p = Position.from_fen(fen)
        assert not p.is_consistent()

def test_legal_piece_positions():
    # 行き場のない歩
    for p in ['Pnsgkgsnl/1r5b1/ppppppppp/9/9/9/1PPPPPPPP/1B5R1/LNSGKGSNL[l] w', 'Pnsgkgsnl/1r5b1/ppppppppp/9/9/9/1PPPPPPPP/1B5R1/LNSGKGSNL[l] b', 
              '1nsgkgsnl/1r5b1/ppppppppp/9/9/9/1PPPPPPPP/1B5R1/pNSGKGSNL[lL] w', '1nsgkgsnl/1r5b1/ppppppppp/9/9/9/1PPPPPPPP/1B5R1/pNSGKGSNL[lL] b']:
        assert not Position.from_fen(p).legal_piece_positions()
    # 行き場のない香車
    for p in ['Lnsgkgsnl/1r5b1/1pppppppp/9/9/9/1PPPPPPPP/1B5R1/LNSGKGSNL[lp] w', 'Lnsgkgsnl/1r5b1/1pppppppp/9/9/9/1PPPPPPPP/1B5R1/LNSGKGSNL[lp] b', 
              '1nsgkgsnl/1r5b1/ppppppppp/9/9/9/1PPPPPPPP/1B5R1/lNSGKGSNL[lLp] w', '1nsgkgsnl/1r5b1/ppppppppp/9/9/9/1PPPPPPPP/1B5R1/lNSGKGSNL[plL] b']:
        assert not Position.from_fen(p).legal_piece_positions()     
    for p in ['N3k4/9/9/9/9/9/9/9/4K4[pppppppppPPPPllLLnNNssSSggGGbBrR] w',
                'N3k4/9/9/9/9/9/9/9/4K4[pppppppppPPPPllLLnNNssSSggGGbBrR] b',
                '4k4/1N7/9/9/9/9/9/9/4K4[pppppppppPPPPllLLnNNssSSggGGbBrR] w',
                '4k4/1N7/9/9/9/9/9/9/4K4[pppppppppPPPPllLLnNNssSSggGGbBrR] b',
                '4k4/9/9/9/9/9/9/9/n3K4[pppppppppPPPPllLLnNNssSSggGGbBrR] w',
                '4k4/9/9/9/9/9/9/9/n3K4[pppppppppPPPPllLLnNNssSSggGGbBrR] b',]:
        assert not Position.from_fen(p).legal_piece_positions()              
    # 二歩
    for p in ['1nsgkgsnl/Pr5b1/ppppppppp/9/9/9/P1PPPPPPP/1B5R1/LNSGKGSNL[l] w', 
              '1nsgkgsnl/Pr5b1/ppppppppp/9/9/9/P1PPPPPPP/1B5R1/LNSGKGSNL[l] b',
              'pnsgkgsnl/1r5b1/ppppppppp/9/9/9/P1PPPPPPP/1B5R1/LNSGKGSNL[l] w', 
              'pnsgkgsnl/1r5b1/ppppppppp/9/9/9/P1PPPPPPP/1B5R1/LNSGKGSNL[l] b', 
              ]:
        assert not Position.from_fen(p).legal_piece_positions()

def test_king_pos():
    pos = Position.from_fen('Pnsgkgsnl/1r5b1/ppppppppp/9/9/9/1PPPPPPPP/1B5R1/LNSGKGSNL[l] w')
    assert pos.king_pos(WHITE) == (8, 4)
    assert pos.king_pos(BLACK) == (0, 4)

def test_in_check():
    pos = Position.from_fen('r7g1/P6Gk/1pppppppp/9/9/2N7/1PPPPPPPP/9/K2R1[lllLnnNPbGGGGggssss] w')
    assert pos.in_check(BLACK)
    assert not pos.in_check(WHITE)


def test_apply_move():
    pos = Position.from_fen('r7g/P7k/1pppppppp/9/9/2N6/1PPPPPPPP/9/KG1R5[lllLnnNPbGGGGggssss] w')
    pos1 = pos.apply_move(WHITE, Move.from_uci('a1a2'))
    fen1 = pos1.fen()
    assert fen1 == 'r7g/P7k/1pppppppp/9/9/2N6/1PPPPPPPP/K8/1G1R5[PLNGGGGlllnnssssbgg] b'

def test_apply_unmove():
    pos = Position.from_fen('r7g/P7k/1pppppppp/9/2N6/9/P1PPPPPPP/9/KG1R5[lllLnnNPbbggssss] b')
    assert pos.is_consistent()
    pos1 = pos.apply_unmove(WHITE, Move.from_uci('b3c5'), KNIGHT.to_piece(BLACK))
    fen1 = pos1.fen()
    assert fen1 == 'r7g/P7k/1pppppppp/9/2n6/9/PNPPPPPPP/9/KG1R5[PLlllnnssssbbgg] w'

def test_checkmate():
    pos = Position.from_fen('r7g/R8/1kppppppp/9/1PNG5/9/L1P1PPPPP/9/KG16[llLnnNPPPbGGGggssss] b')
    assert pos.in_check(BLACK)
    assert pos.in_checkmate()

def test_king_checkmate_pawn():
    pos = Position.from_fen('r7g/P5G1k/1pppppppP/8G/2N6/9/P1PPPPPPp/9/KG1R5[lllLnnNPbbssss] b')
    assert king_checkmate_pawn(pos, 2, 8)
