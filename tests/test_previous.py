import sys
from shogilib import Ptype, Piece, Position, Move, BLACK, WHITE, PAWN, GOLD, KNIGHT, LANCE, PAWN, generate_previous_moves, generate_previous_positions

def test_generate_previous_moves():
    pos = Position.from_fen('r7g/1P4G1k/1pppppppP/8G/2N6/9/P1PPPPPPp/9/KG1R5[lllLnnNPbbssss] b')
    assert not pos.illegal()
    moves = set(generate_previous_moves(pos))
    #print(f'moves={list(sorted([m.to_uci() for m in moves]))}')
    moves_strs = ['G@b1', 'G@g8', 'G@i6', 'N@c5', 'P@a3', 'P@b8', 'P@c3', 'P@d3', 'P@e3', 'P@f3', 'P@g3', 'P@h3', 'R@d1', 'a2a1', 'a2a3', 'b2a1', 'b2b1', 'b3c5', 'c1b1', 'c1d1', 'c2c3', 'd2d1', 'd2d3', 'e1d1', 'e2e3', 'f1d1', 'f2f3', 'f8g8', 'g1d1', 'g2g3', 'g9g8', 'h1d1', 'h2h3', 'h5i6', 'h6i6', 'h8g8', 'i1d1', 'i5i6']
    moves1 = set(Move.from_uci(x) for x in moves_strs)
    for m in moves:
        assert m in moves1
    for m in moves1:
        assert m in moves

def test_generate_previous_positions():
    pos = Position.from_fen('r7g/1P4G1k/1pppppppP/7G1/2N6/9/P1PPPPPPp/9/KG1R5[lllLnnNPbbssss] b')
    assert pos.is_consistent()
    assert not pos.illegal()
    poslist = [pos1.fen() for pos1 in generate_previous_positions(pos)]
    poslist1 = ['r7g/1P4G1k/1ppppppp1/7GP/2N6/9/P1PPPPPPp/9/KG1R5[PLNlllnnssssbb] w', 
                'r7g/1P4G1k/1ppppppp+p/7GP/2N6/9/P1PPPPPPp/9/KG1R5[LNlllnnssssbb] w', 
                'r7g/1P4G1k/1pppppppl/7GP/2N6/9/P1PPPPPPp/9/KG1R5[PNlllnnssssbb] w', 
                'r7g/1P4G1k/1ppppppp+l/7GP/2N6/9/P1PPPPPPp/9/KG1R5[PNlllnnssssbb] w', 
                'r7g/1P4G1k/1pppppppn/7GP/2N6/9/P1PPPPPPp/9/KG1R5[PLlllnnssssbb] w', 
                'r7g/1P4G1k/1ppppppp+n/7GP/2N6/9/P1PPPPPPp/9/KG1R5[PLlllnnssssbb] w']
    #print(f'poslist={poslist}')
    for pos1 in poslist1:
        assert pos1 in poslist
    # 打ち歩詰めの手は溯れない
    assert 'r7g/1P4G1k/1ppppppp1/7G1/2N6/9/P1PPPPPPp/9/KG1R5[PPLNlllnnssssbb] w' not in poslist

def test_do_undo():
    posstr = 'r7g/1P4G1k/1pppppppP/7G1/2N6/9/P1PPPPPPp/9/KG1R5[PLNlllnnssssbb] b'
    pos = Position.from_fen(posstr)
    assert pos.is_consistent()
    moves = pos.plm(pos.side_to_move)
    for m in moves:
        pos1 = pos.apply_move(pos.side_to_move, m)
        if not pos1.is_consistent():
            continue
        poslist = [pos2.fen() for pos2 in generate_previous_positions(pos1)]
        print(f'm={m}, pos1={pos1.fen()}, poslist={poslist}')
        assert posstr in poslist