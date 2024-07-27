from shogilib import Player, Ptype, Piece, Position, BLACK, WHITE, can_promote_y, player2c, Move
from shogilib import KING, ROOK, BISHOP, GOLD, SILVER, PAWN, LANCE, KNIGHT, BLANK, king_checkmate_pawn




def test_piece():
    for pl in [WHITE, BLACK]:
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
    for pl in [WHITE, BLACK]:
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

def test_piece_cmp():
    assert KING.to_piece(WHITE) < KING.to_piece(BLACK)
    assert PAWN.to_piece(WHITE) < PAWN.to_piece(BLACK)
    assert not PAWN.promote().to_piece(WHITE) < PAWN.promote().to_piece(WHITE)
    assert PAWN.promote().to_piece(BLACK) < PAWN.to_piece(WHITE)
