from collections import defaultdict
from heapq import heappush, heappop
import argparse

from shogilib import Position, generate_previous_positions, BLANK, KING, BLACK, WHITE, W, H
from shogilib import showstate, show_images_hv

def distance_to_KK(pos):
    ans = 0
    kings = []
    for y in range(H):
        for x in range(W):
            piece = pos.board[y][x]
            if piece != BLANK:
                ptype = piece.ptype()
                if ptype == KING:
                    kings.append((y, x))
                else:
                    ans += 10
                    if ptype.is_promoted():
                        ans += 10
                        pl = piece.player()
                        if pl == WHITE:
                            if y > 2:
                                ans += y - 2
                        else:
                            if y < 6:
                                ans += 6 - y                                
    assert len(kings) == 2
    # if abs(kings[0][0] - kings[1][0]) + abs(kings[0][1] - kings[1][1]) <= 2:
    #     ans += 10
    return ans        

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
            return (True, [pos.fen() for pos in ans])
        for pos2 in generate_previous_positions(pos1):
            if pos2 not in prev:
                prev[pos2] = pos1
                distance[pos2] = distance[pos1] + 1
                heappush(q, (distance_to_KK(pos2), pos2))
    maxd = max((v, k) for k, v in distance.items())
    return (False, (maxd[0], maxd[1].fen()))

def load_fen_list(fname):
    ans = []
    with open(fname) as f:
        for fen in f:
            pos = Position.from_fen(fen)
            ans.append(pos)
    return ans
def save_fen_list(fname, ls):
    with open(fname, 'w') as wf:
        wf.write('\n'.join(pos.fen() for pos in ls))
        wf.write('\n')

def process_file(filename, parfile=False):
    file_OK = f'{filename}_OK.txt' if parfile else 'reach_OK.txt'
    file_NG = f'{filename}_NG.txt' if parfile else 'reach_NG.txt'
    with open(filename) as f:
        with open(file_OK, 'w') as wf1:
            with open(file_NG, 'w') as wf2:
                for fen in f:
                    pos = Position.from_fen(fen)
                    assert pos.side_to_move == WHITE, f'pos={pos.fen()}'
                    tf, ans = can_reach_KK(pos)
                    if tf:
                        print(f'tf=True, len(ans)={len(ans)}')
                    else:
                        print(f'tf=False, ans={ans}')
                    if tf:
                        assert pos.side_to_move == WHITE, f'pos={pos.fen()}'
                        wf1.write(pos.fen() + '\n')
                    else:
                        assert pos.side_to_move == WHITE, f'pos={pos.fen()}'
                        wf2.write(pos.fen() + '\n')

def process_fen(fen):
    pos = Position.from_fen(fen)
    assert pos.side_to_move == WHITE, f'pos={pos.fen()}'
    tf, ans, = can_reach_KK(pos)
    showstate(pos, filename='check_reach_start.png')
    if tf:
        print(f'tf=True, len(ans)={len(ans)}')
        # show_images_hv([showstate(Position.from_fen(f)) for f in ans], 5, 'ans.png')
        # ans.reverse()
        # for i in range(len(ans)):
        #     showstate(Position.from_fen(ans[i]), filename=f'movie/check_reach_{i+1}.png')
    else:
        print(f'tf=False, ans={ans}')

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
