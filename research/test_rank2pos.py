from itertools import combinations
from collections import defaultdict, Counter

from rank import kpos_rank2pos, comb, comb_table_pre, piece_rank2pos, pt2comblist, basic_ptype_rank2pos, pos_x, pos_y, canpromote2comb_table, nopromote2comb_table, rank2l, l2pos, rank2pos, pos2l
from shogilib import H, W, KING, WHITE, BLACK, PAWN, LANCE, KNIGHT, SILVER, GOLD, BISHOP, ROOK, Position
from rank_to_fen import flipH_onboards, flipHpos

def test_rank2l():
    (hands, onboards) = rank2l(0)
    #print(f'hands={hands}, onboards={onboards}')
    (hands, onboards) = rank2l(79711464585613890499229372106470162629966919404028159691811738577084532)
    print(f'hands={hands}, onboards={onboards}')
    #assert False

def test_rank2pos():
    pos = rank2pos(0)
    assert pos.fen() == 'Knppr4/klppr4/glppb4/glppb4/glpp5/gpps5/npps5/npps5/npps5[] w'
    pos = rank2pos(79711464585613890499229372106470162629966919404028159691811738577084532)
    assert pos.fen() == 'Knppr4/klppr4/glppb4/glpp5/glpp5/gpps5/npps5/npps5/npps5[b] w'

def test_pos2l():
    pos = Position.from_fen('+pg2n1+pnp/+p1g1+p2+p+p/p1P1b1b2/+p1slk3L/2+p1PGR2/3nKs1+p1/s1gPS+P3/P3n4/1lpr3LP[] w')
    l = pos2l(pos)
    flipl = flipH_onboards(l[1])
    assert flipl < l[1]


