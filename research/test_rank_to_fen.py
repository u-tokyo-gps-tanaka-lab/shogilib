from itertools import combinations
from collections import defaultdict, Counter

from rank_to_fen import kpos_rank2pos, comb, comb_table_pre, ptype_rank2pos, pt2comblist, basic_ptype_rank2pos
from shogilib import H, W, KING, WHITE, BLACK, PAWN, LANCE, KNIGHT, SILVER, GOLD, BISHOP, ROOK

def test_kpos_rank2pos():
    combs = set()
    for j in range(H * (W // 2) * (H * W - 1) + H * (H * (W + 1) // 2 - 1)):
        onboards, empties = [], list(range(81))
        kpos_rank2pos(onboards, j, empties)
        assert len(empties) == 79
        assert len(onboards) == 2
        assert onboards[0][0] == KING.to_piece(WHITE)
        assert onboards[1][0] == KING.to_piece(BLACK)
        pos1, pos2 = onboards[0][1], onboards[1][1]
        combs.add((pos1, pos2))
    assert len(combs) == H * (W // 2) * (H * W - 1) + H * (H * (W + 1) // 2 - 1)
    #print(f'combs={combs}')
    for pos1, pos2 in combs:
        print(f'pos1={pos1}, pos2={pos2}')
        assert pos1 != pos2
        assert pos1[1] < 5
        if pos1[1] == 4:
            assert pos2[1] < 5

def test_comb_table():
    for n_pieces in range(1, 19):
        for rest in range(n_pieces, H * W + 1):
            assert len(comb_table_pre[rest][n_pieces]) == rest + 1
            assert comb_table_pre[rest][n_pieces][-1] == comb(rest, n_pieces)

def test_ptype_rank2pos():
    for rest, n_pieces in [(79, 1), (78, 2), (20, 4), (81, 3)]:
        combs = set()
        for j in range(comb(rest, n_pieces)):
            empties = list(range(rest))
            onboards = []
            ptype_rank2pos(onboards, KING.to_piece(WHITE), j, n_pieces, empties)
            assert len(empties) == rest - n_pieces
            assert len(onboards) == n_pieces
            print(f'onboards={onboards}')
            poslist = [(x[1], x[2]) for x in onboards]
            poslist1 = list(sorted([x for x in poslist], key=lambda p: (p[1], p[0])))
            assert poslist == poslist1
            combs.add(tuple(poslist))
        assert len(combs) == comb(rest, n_pieces)
        for cmb in combinations(range(rest), n_pieces):
            poslist = tuple((p % H, p // H) for p in cmb)
            assert poslist in combs

def test_basic_pt2comblist():
    for (pt, n_empty, allcount), count0 in [((PAWN, 79, 1), 79 * 4)]:
        x, rank2comb = pt2comblist(pt, n_empty, allcount)
        assert x == count0
        assert len(rank2comb) == 4
        for i, comb in rank2comb:
            assert sum(comb) == allcount


def test_basic_ptype_rank2pos():
    for pt, rest, n_pieces in [(PAWN, 79, 1), (GOLD, 78, 2), (SILVER, 20, 4), (ROOK, 81, 3)]:
        combs = set()
        pcmb2posl = defaultdict(list)
        for j in range(comb(rest, n_pieces)):
            empties = list(range(rest))
            onboards = []
            basic_ptype_rank2pos(onboards, pt, j, n_pieces, empties)
            assert len(empties) == rest - n_pieces
            assert len(onboards) == n_pieces
            print(f'onboards={onboards}')
            for cmb in onboards:
                piece2posl = defaultdict(list)
                for piece, y, x in cmb:
                    piece2posl[piece].append((y, x))
                kvs = list(sorted(piece2posl.items()))
                pcounts = tuple(sorted(Counter(x[0] for x in kvs).items()))
                posl = [x[1] for x in kvs]
                pcmb2posl[pcounts].append(posl)

        assert False