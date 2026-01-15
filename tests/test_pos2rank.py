from itertools import combinations
from collections import defaultdict, Counter
import random

from research.rank import kpos_rank2pos, comb, comb_table_pre, piece_rank2pos, pt2comblist, basic_ptype_rank2pos, pos_x, pos_y, canpromote2comb_table, nopromote2comb_table, rank2l, l2pos, pos2rank, l2key, pos2l, rank2pos
from research.paths import data_path
from shogilib import Position, H, W, KING, WHITE, BLACK, PAWN, SILVER, GOLD, BISHOP, ROOK


def test_l2key():
    fen = 'S+l1+P+p1+N1+R/+L2+pPS+pP1/+p1P2+pg2/Kb4b1s/1n2+p+ppks/1+P5nr/2+P3lg1/3+PpP1P1/1+N4Glg[] w'
    pos = Position.from_fen(fen) 
    l = pos2l(pos)
    key = l2key(l)
    assert key == ((), ((8, 4), (4, 4), (3, 4), (2, 18), (5, 4), (7, 2), (6, 2)))
    fen = 'n1nP2p+P1/6+pRN/K2+P1+L3/+p+P3+pgN+L/+P+L1G+b+p2s/B3lg2p/pp1+Pks1+Sr/2p6/+p5p+s+p[g] w'
    pos = Position.from_fen(fen) 
    l =  pos2l(pos)
    #print(f'l={l}')
    key = l2key(l)
    assert key == (((8, 1),), ((8, 3), (4, 4), (3, 4), (2, 18), (5, 4), (7, 2), (6, 2)))

def test_pos2rank():
    # ggKK positions
    for fen in ['4k4/4G4/9/9/9/9/9/9/1GK6[ggnnnnssssppppppppppppppppppllllrrbb] w']:
        pos = Position.from_fen(fen)
        rank = pos2rank(pos)
        pos1 = rank2pos(rank)
        if pos != pos1:
            print(f'rank={rank}, pos={pos.fen()}, pos1={pos1.fen()}')
        assert pos == pos1
    # KK positions
    for fen in ['4k4/9/9/9/9/9/9/9/2K6[ggggnnnnssssppppppppppppppppppllllrrbb] w']:
        pos = Position.from_fen(fen)
        rank = pos2rank(pos)
        pos1 = rank2pos(rank)
        if pos != pos1:
            print(f'rank={rank}, pos={pos.fen()}, pos1={pos1.fen()}')
        assert pos == pos1
RANK_MAX = 80880932079767835177773204009328769812438521503800714936366945233084532
def test_pos2rank_from_file():
    with open(data_path('check_OK.txt')) as f:
        for lno in range(1000):
            l = f.readline()
            fen = ' '.join(l.split()[:2])
            #print(f'fen={fen}')
            pos = Position.from_fen(fen)
            rank = pos2rank(pos)
            assert rank < RANK_MAX
            #print('pos={pos}, rank={rank}')
            pos1 = rank2pos(rank)
            assert pos == pos1

def test_rank2pos_from_file():
    with open(data_path('RN100M_10000.txt')) as f:
        for lno in range(1000):
            l = f.readline()
            rank = int(l)
            pos = rank2pos(rank)
            rank1 = pos2rank(pos)
            assert rank == rank1
