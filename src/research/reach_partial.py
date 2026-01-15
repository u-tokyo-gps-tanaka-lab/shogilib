from shogilib import (
    Position,
    generate_previous_positions,
    BLANK,
    KING,
    W,
    H,
    BLACK,
    WHITE,
)
from heapq import heappush, heappop
from collections import defaultdict
import sys
from research.check_reach import can_reach_KK
from research.paths import output_path


assert len(sys.argv) == 2
infname = sys.argv[1]
prevOK = []
with open(infname, "r") as rf:
    for l in rf:
        prevOK.append(Position.from_fen(l))

reachOK = []
reachNG = []
okcount = defaultdict(int)
ngcount = defaultdict(int)
i = 0
for pos in prevOK:
    ans = can_reach_KK(pos)
    if ans[0] == True:
        # if i % 100 == 0:
        #    print(ans[1])
        reachOK.append(pos)
        okcount[len(ans[1])] += 1
    else:
        # if i % 100 == 0:
        #    print(ans[1])
        reachNG.append(pos)
        ngcount[ans[1]] += 1
print(f"reachNG={len(reachNG)}, reachOK={len(reachOK)}")
print(f"reachNG[:10] = {[pos.fen() for pos in reachNG[:10]]}")
print(f"reachOK[:10] = {[pos.fen() for pos in reachOK[:10]]}")

with open(output_path(f"reachOK.{infname}.txt"), "w") as wf:
    for pos in reachOK:
        wf.write(pos.fen() + "\n")
with open(output_path(f"reachNG.{infname}.txt"), "w") as wf:
    for pos in reachNG:
        wf.write(pos.fen() + "\n")
