from shogilib import Player, Ptype, Piece, Position, BLACK, WHITE, can_promote_y, player2c
from shogilib import KING, ROOK, BISHOP, GOLD, SILVER, PAWN, LANCE, KNIGHT

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