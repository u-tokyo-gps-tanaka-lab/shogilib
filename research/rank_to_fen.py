import sys
import json
from bisect import bisect_left, bisect_right
from functools import reduce
from operator import mul
from shogilib import Ptype, WHITE, BLACK, KING, H, W

COUNT2I_JSON = 'count2i.json'
def read_count2i(filename):
    with open(filename) as f:
        return json.load(f)

counts = read_count2i(COUNT2I_JSON)
countsum, rank2count = counts['sum'], counts['rank2count']
# print(f'countsum={countsum}, len(count2offset)={len(count2offset)}')

KPOS_COUNT = H * (W // 2) * (H * W - 1) + H * (H * (W + 1) // 2 - 1)
def kpos_rank2pos(onboards, j, empties):
    if j < H * (W // 2) * (H * W - 1):
        j0 = j % (H * (W // 2))
        k0 = empties.pop(j0)        
        j1 = j // (H * (W // 2))
        k1 = empties.pop(j1)
    else:
        j -= H * (W // 2) * (H * W - 1)
        j0 = j % H 
        k0 = empties.pop(H * (W // 2) + j0)
        j1 = j // H 
        k1 = empties.pop(j1)
    onboards.append((KING.to_piece(WHITE), (k0 % H, k0 // H)))
    onboards.append((KING.to_piece(BLACK), (k1 % H, k1 // H)))

def comb(n, m):
    if n < m:
        return 0
    m = min(m, n - m)
    ans = 1
    for i in range(m):
        ans = ans * (n - i) // (i + 1)
    return ans

# rest個の空マスから n_pieces を選ぶ時，最小のインデックスを i個にする組み合わせの数は?
comb_table = [[[0] * rest for n_pieces in range(19)] for rest in range(H * W + 1)]
for n_pieces in range(1, 19):
    for rest in range(n_pieces, H * W + 1):
        s = 0
        for i in range(rest - 1, -1, -1):
            comb_table[rest][n_pieces][i] = comb(rest - 1 - i, n_pieces - 1)
# rest個の空マスから n_pieces を選ぶ時，最小のインデックスを i個未満の組み合わせの数は?
comb_table_pre = [[[0] * (rest + 1) for n_pieces in range(19)] for rest in range(H * W + 1)]        
for n_pieces in range(1, 19):
    for rest in range(n_pieces, H * W + 1):
        for i in range(rest):
            #print(f'len(comb_table_pre[rest][n_pieces]) = {len(comb_table_pre[rest][n_pieces])}')
            #print(f'len(comb_table[rest][n_pieces]) = {len(comb_table[rest][n_pieces])}')
            comb_table_pre[rest][n_pieces][i + 1] = comb_table_pre[rest][n_pieces][i] + comb_table[rest][n_pieces][i] 



def ptype_rank2pos(onboards, piece, j, n_pieces, empties):
    rest = len(empties)
    #print(f'ptype_rank2pos(j={j}, n_pieces={n_pieces}, len(empties)= {len(empties)}')
    empty_base = 0
    while n_pieces > 0:
        i = bisect_right(comb_table_pre[rest][n_pieces], j) - 1
        j -= comb_table_pre[rest][n_pieces][i]
        rest = rest - 1 - i
        #print(f'len(empties) = {len(empties)}, i={i}, empty_base={empty_base}, rest={rest}')
        pi = empties.pop(empty_base + i)
        empty_base += i
        onboards.append((piece, pi % H, pi // H))
        n_pieces -= 1


def basic_ptype_rank2pos(onboards, pt, j, combs, empties):
    for i, x in enumerate(combs):
        if x != 0:
            rest = len(empties)
            v = comb(rest, x)
            cur = j % v
            j //= v
            piece = pt.piece(WHITE if i % 2 == 0 else BLACK)
            if i & 2 == 0:
                piece = piece.promote()
            ptype_rank2pos(onboards, piece, cur, x, empties)
def pt2comblist(pt, n_empty, allcount):
    rank2comb = []
    x = 0
    for pb0 in range(allcount + 1 if pt.can_promote() else 1):
        v0 = allcount - pb0
        n_empty_1 = n_empty - pb0
        for pb1 in range(v0 + 1 if pt.can_promote() else 1):
            v1 = v0 - pb1
            n_empty_2 = n_empty_1 - pb1
            for b0 in range(v1 + 1):
                n_empty_3 = n_empty_2 - b0
                b1 = v1 - b0
                xadd = comb(n_empty, pb0) * comb(n_empty_1, pb1) * comb(n_empty_2, b0) * comb(n_empty_3, b1)
                rank2comb.append((x, (pb0, pb1, b0, b1)))
                x += xadd
    return x, rank2comb                

def rank2l(x):
    j = bisect_left(rank2count, (x, [], []))
    if not (j < len(rank2count) and rank2count[j][0] == x):
        j -= 1
    o, cs, ms = rank2count[j]
    rest = x - o
    mult = KPOS_COUNT * reduce(mul, ms[0], 1) * reduce(mul, ms[1], 1)
    assert rest < mult
    hands = [[], []]
    for i, (pti, v) in enumerate(cs[0]):
        pt = Ptype(pti)
        assert mult % ms[0][i] == 0
        mult //= ms[0][i]
        j = rest % ms[0][i]
        rest //= ms[0][i]
        for _ in range(j):
            hands[0].append(pt)
        for _ in range(v - j):
            hands[1].append(pt)
    onboards = []
    assert mult % KPOS_COUNT
    mult //= KPOS_COUNT
    j = rest % KPOS_COUNT
    rest //= KPOS_COUNT
    empties = list(range(H * W))
    kpos_rank2pos(onboards, j, empties)
    for i, (pti, v) in enumerate(cs[1]):
        pt = Ptype(pti)
        assert mult % ms[1][i] == 0
        mult //= ms[1][i]
        j = rest % ms[1][i]
        rest //= ms[1][i]
        x, rank2comb = pt2comblist(pt, rest, v)
    
        assert j < x
        k = bisect_left(rank2comb, (j, (0, 0, 0, 0)))
        if not(k < len(rank2comb) and rank2comb[k][0] == j):
            k -= 1
        j -= rank2comb[k][0]
        basic_ptype_rank2pos(onboards, pt, j, rank2comb[k], empties)
    return (hands, onboards)

flipH_OK = []
flipH_NG = []

def flipHpos(v):
    y, x = v % H, v // H 
    x = W - 1 - x
    return x * H + y

def flipH_onboards(xs):
    assert xs[0][0] == KING.to_piece(WHITE)
    assert xs[1][0] == KING.to_piece(BLACK)
    ans = []
    for pt, v in xs:
        ans.append((pt, flipHpos(v)))
    return ans        

def process_file(filename):
    with open(filename) as f:
        for l in f.readlines():
            x = int(l)
            assert x < countsum
            (hands, onboards) = rank2l(x)
            pos = l2pos(hands, onboards)
            if flipH_onboards(onboards) < onboards:
                flipH_NG.append(pos)
            else:
                flipH_OK.append(pos)

def main():
    for fname in sys.argv[1:]:
        process_file(fname)

if __name__ == "__main__":
    main()