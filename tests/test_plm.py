import sys
from shogilib import Ptype, Piece, Position, Move, BLACK, WHITE, PAWN, GOLD, KNIGHT, LANCE, PAWN

def test_plm_piece():
    pos = Position.from_fen('Pnsgkgsnl/1r5b1/ppppppppp/9/9/9/1PPPPPPPP/1B5R1/LNSGKGSNL[l] w')
    moves = []
    pos.plm_piece(moves, WHITE, GOLD, 8, 3)
    #print([m.to_uci() for m in moves])
    assert Move.from_uci('d1c2') in moves
    assert Move.from_uci('d1d2') in moves
    assert Move.from_uci('d1e2') in moves
    assert len(moves) == 3
    # don't generate moves for knight and lance that have no place to go
    pos = Position.from_fen('4k4/P8/9/1LN6/9/9/9/9/4K4[pppppppppPPPllLnnNssSSggGGbBrR] w')
    moves = []   
    assert pos.board[3][2] == KNIGHT.to_piece(WHITE)
    print(f'KNIGHT={Ptype(KNIGHT)}')
    pos.plm_piece(moves, WHITE, Ptype(KNIGHT), 3, 2)
    print([m.to_uci() for m in moves])
    assert Move.from_uci('c6b8+') in moves
    assert Move.from_uci('c6d8+') in moves
    assert Move.from_uci('c6b8') not in moves
    assert Move.from_uci('c6d8') not in moves
    assert len(moves) == 2
    moves = []
    pos.plm_piece(moves, WHITE, LANCE, 3, 1)
    print([m.to_uci() for m in moves])
    assert Move.from_uci('b6b7') in moves
    assert Move.from_uci('b6b7+') in moves
    assert Move.from_uci('b6b8') in moves
    assert Move.from_uci('b6b8+') in moves
    assert Move.from_uci('b6b9+') in moves
    assert Move.from_uci('b6b9') not in moves

def test_plm_drop():
    # don't generate drop moves for pawn, knight, lance that have no place to go
    pos = Position.from_fen('.nsgkgsnl/1r5b1/1pppppppp/9/9/9/1PPPPPPPP/1B5R1/L1SGKGSNL[pPLN] w')
    moves = []
    pos.all_drop_moves(moves, WHITE)
    assert Move.from_uci('P@a8') in moves
    assert not Move.from_uci('P@a9') in moves
    assert Move.from_uci('L@a8') in moves
    assert not Move.from_uci('L@a9') in moves
    assert Move.from_uci('P@a7') in moves
    assert not Move.from_uci('P@a9') in moves
    assert not Move.from_uci('N@a8') in moves
    assert not Move.from_uci('N@a9') in moves

def test_plm():
    pos = Position.from_fen('.nsgkgsnl/1r5b1/ppppppppp/9/9/9/1PPPPPPPP/1B5R1/LNSGKGSNL[PL] w')
    moves_strs = ['L@a2', 'L@a3', 'L@a4', 'L@a5', 'L@a6', 'L@a8', 'L@b4', 'L@b5', 'L@b6', 'L@c2', 'L@c4', 'L@c5', 'L@c6', 'L@c8', 'L@d2', 'L@d4', 'L@d5', 'L@d6', 'L@d8', 'L@e2', 'L@e4', 'L@e5', 'L@e6', 'L@e8', 'L@f2', 'L@f4', 'L@f5', 'L@f6', 'L@f8', 'L@g2', 'L@g4', 'L@g5', 'L@g6', 'L@g8', 'L@h4', 'L@h5', 'L@h6', 'L@i2', 'L@i4', 'L@i5', 'L@i6', 'L@i8', 'P@a2', 'P@a3', 'P@a4', 'P@a5', 'P@a6', 'P@a8', 'a1a2', 'a1a3', 'a1a4', 'a1a5', 'a1a6', 'a1a7', 'a1a7+', 'b1a3', 'b2a3', 'b3b4', 'c1c2', 'c1d2', 'c3c4', 'd1c2', 'd1d2', 'd1e2', 'd3d4', 'e1d2', 'e1e2', 'e1f2', 'e3e4', 'f1e2', 'f1f2', 'f1g2', 'f3f4', 'g1f2', 'g1g2', 'g3g4', 'h2c2', 'h2d2', 'h2e2', 'h2f2', 'h2g2', 'h2i2', 'h3h4', 'i1i2', 'i3i4']
    sf_moves = set(Move.from_uci(x) for x in moves_strs)
    moves = set(pos.plm(WHITE))
    print(list(sorted(m.to_uci() for m in moves)))
    for m in sf_moves:
        assert m in moves
    for m in moves:
        assert m in sf_moves


