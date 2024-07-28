import sys
import json
from math import comb
from bisect import bisect_left, bisect_right
from functools import reduce
from operator import mul
from shogilib import Ptype, WHITE, BLACK, KING, H, W
from rank import countsum, rank2l, l2pos


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
    for piece, v in xs:
        ans.append((piece, flipHpos(v)))
    ans.sort()
    return ans        

def process_file(filename):
    with open(filename) as f:
        with open('flipH_OK.txt', 'w') as wf1:
            with open('flipH_NG.txt', 'w') as wf2:
                for l in f.readlines():
                    x = int(l)
                    assert x < countsum
                    (hands, onboards) = rank2l(x)
                    onboards1 = onboards[:]
                    onboards.sort()
                    assert onboards == onboards1
                    pos = l2pos((hands, onboards))
                    if flipH_onboards(onboards) < onboards:
                        wf2.write(pos.fen() + '\n')
                    else:
                        wf1.write(pos.fen() + '\n')
def main():
    for fname in sys.argv[1:]:
        process_file(fname)

if __name__ == "__main__":
    main()