from collections import defaultdict
from heapq import heappush, heappop
import argparse

from check_reach import distance_to_KK
from shogilib import Position, generate_previous_positions, BLANK, KING, BLACK, WHITE, W, H
from shogilib import showstate, show_images_hv        

def can_reach_KK(pos):
    prev = {}
    q = [(distance_to_KK(pos), pos)]
    prev[pos] = None
    distance = defaultdict(int)
    distance[pos] = 0
    i = 0
    while len(q) > 0:
        d, pos1 = heappop(q)
        #if i % 1 == 0:
        #    print(f'len(q)={len(q)}, d={d}, pos1={pos1.fen()}')
        i += 1
        #print(f'd={d}, pos1={pos1.fen()}')
        if d == 0:
            ans = [pos1]
            while pos1 != pos:
                pos1 = prev[pos1]
                ans.append(pos1)
            # ans.append(pos)
            #print(f'len(prev)={len(prev)}')
            return (True, [pos.fen() for pos in ans], i)
        for pos2 in generate_previous_positions(pos1):
            if pos2 not in prev:
                prev[pos2] = pos1
                distance[pos2] = distance[pos1] + 1
                heappush(q, (distance_to_KK(pos2), pos2))
    maxd = max((v, k) for k, v in distance.items())
    return (False, (maxd[0], maxd[1].fen()), i)

def process_file(filename, parfile=False):
    file_OK = f'{filename}_OK.txt' if parfile else 'reach_OK.txt'
    file_NG = f'{filename}_NG.txt' if parfile else 'reach_NG.txt'
    with open(filename) as f:
        with open(file_OK, 'w') as wf1:
            with open(file_NG, 'w') as wf2:
                for fen in f:
                    pos = Position.from_fen(fen)
                    assert pos.side_to_move == WHITE, f'pos={pos.fen()}'
                    tf, ans, heap_count = can_reach_KK(pos)
                    if tf:
                        print(f'tf=True, len(ans)={len(ans)}, heap_count={heap_count}')
                    else:
                        print(f'tf=False, ans={ans}, heap_count={heap_count}')
                    if tf:
                        assert pos.side_to_move == WHITE, f'pos={pos.fen()}'
                        wf1.write(pos.fen() + '\n')
                    else:
                        assert pos.side_to_move == WHITE, f'pos={pos.fen()}'
                        wf2.write(pos.fen() + '\n')

def process_fen(fen):
    pos = Position.from_fen(fen)
    assert pos.side_to_move == WHITE, f'pos={pos.fen()}'
    tf, ans, heap_count = can_reach_KK(pos)
    showstate(pos, filename='check_reach_start.png')
    if tf:
        print(f'tf=True, len(ans)={len(ans)}, heap_count={heap_count}')
        show_images_hv([showstate(Position.from_fen(f)) for f in ans], 5, 'ans.png')
    else:
        print(f'tf=False, ans={ans}, heap_count={heap_count}')

def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--fen', nargs=1, metavar='FEN')
    group.add_argument('--file', nargs=1, metavar='FILENAME')
    parser.add_argument('-p', '--parallel', action='store_true', help='for parallel processing; requires --file option')
    args = parser.parse_args()

    if args.parallel and not args.file:
        parser.error('-p option requires --file option')
    if args.fen:
        process_fen(args.fen[0])
    else:
        process_file(args.file[0], args.parallel)

if __name__ == '__main__':
    main()
