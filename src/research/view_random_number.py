import sys


def view_random(filename):
    bcount = [0] * 300
    lcount = 0
    with open(filename) as f:
        for l in f:
            lcount += 1
            v = int(l)
            for i in range(len(bcount)):
                if v & (1 << i) != 0:
                    bcount[i] += 1
    print(f"lcount={lcount}, bcount={bcount}")


for fname in sys.argv[1:]:
    view_random(fname)
