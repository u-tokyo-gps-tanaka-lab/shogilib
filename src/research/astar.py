from collections import defaultdict
from heapq import heappush, heappop
import argparse

from shogilib import Position, generate_previous_positions, BLANK, KING, Ptype, BLACK, WHITE, W, H, showstate, show_images_hv
from research.paths import output_path

def f(x, y, pos):
    piece = pos.board[y][x]
    ptype = piece.ptype()
    pl = piece.player()
    if ptype == BLANK:
        return 0
    if pl == BLACK:
        y = 8 - y
    if ptype == KING:
        if y >= 2:
            for y1 in range(y +1, 9):
                y2 = (8 - y1) if pl == BLACK else y1
                p = pos.board[y2][x]
                if p != BLANK and p.player() == pl:
                    ptype_p = p.ptype()
                    if ptype_p in [Ptype.PPAWN, Ptype.PLANCE, Ptype.PKNIGHT]:
                        return 1
                    if ptype_p == Ptype.PSILVER:
                        if y2 >= 4:
                            return 1
        return 0
                
    if not ptype.is_promoted():
        return 1
    if ptype == Ptype.PROOK:
        return 2
    if ptype == Ptype.PBISHOP:
        if (y, x) in [(7,4), (8,3), (8,4), (8,5)]:
            return 3
        else:
            return 2
    if ptype == Ptype.PSILVER:
        if y <= 3:
            return 2
        else:
            return y -1
    assert ptype in [Ptype.PPAWN, Ptype.PLANCE, Ptype.PKNIGHT]
    if y <=2:
        return 2
    else:
        return y

def admissible_heuristic(pos):
    value = [0, 0] # b, w
    for y in range(H):
        for x in range(W):
            piece = pos.board[y][x]
            if piece != BLANK:
                pl = piece.player()
                value[pl.value] += f(x, y, pos)
                # print(value)
    ans = max(value) * 2
    i = pos.side_to_move.value
    if value[1-i] > value[i]:
        ans -= 1
    return ans

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
                            if y > 3:
                                ans += y - 3
                        else:
                            if y < 6:
                                ans += 6 - y                                
    assert len(kings) == 2
    # if abs(kings[0][0] - kings[1][0]) + abs(kings[0][1] - kings[1][1]) <= 2:
    #     ans += 10
    return ans        

def can_reach_KK(pos):
    prev = {}
    h1 = admissible_heuristic(pos)
    h2 = distance_to_KK(pos)
    q = [(h1, h2, pos)]
    prev[pos] = None
    distance = defaultdict(int)
    distance[pos] = 0
    i = 0
    while len(q) > 0:
        _, h_pos1, pos1 = heappop(q)
        i += 1
        if i % 100 == 0:
            print(f'i={i}, len(q)={len(q)}, h_pos1={h_pos1}, pos1={pos1.fen()}')
        if h_pos1 == 0:
            ans = [pos1]
            while pos1 != pos:
                pos1 = prev[pos1]
                ans.append(pos1)
            ans.append(pos)
            return (True, [pos.fen() for pos in ans], i)
        for pos2 in generate_previous_positions(pos1):
            if pos2 not in prev:
                h1_pos2 = admissible_heuristic(pos2)
                h2_pos2 = distance_to_KK(pos2)
                prev[pos2] = pos1
                distance[pos2] = distance[pos1] + 1
                heappush(q, (distance[pos2] + h1_pos2, h2_pos2, pos2))
    maxd = max((v, k) for k, v in distance.items())
    return (False, (maxd[0], maxd[1].fen()), i)

    # fen = '+p+p+p+p+p+p+p+p+p/+p+p+p+p+p+p+p+p+p/+n+n+n+nk+l+l+l+l/+s+s+s+s1gggg/+r7+b/+r7+b/9/9/4K4[] w'
    # fen = 'K2g2+N2/1n+P3+pp+L/k1s1+P2n+P/1R2+b1l1+R/5+p+S2/+P1+P3g1+P/1+L+N+p1g2G/L1+P1+P1+PP+P/+SB1+p+P4[Ps] w'
    # fen = '+p+p+p+p+p+p+p+p+p/+p+p+p+p+p+p+p+p+p/+l+l+l+l+n+n+n+n+s/+s+s+sb5/6g2/6g1K/5r1g1/8g/5+b1k+r[] w'

def process_file(filename, parfile=False):
    file_OK = f'{filename}_OK.txt' if parfile else output_path('astar_OK.txt')
    file_NG = f'{filename}_NG.txt' if parfile else output_path('astar_NG.txt')
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

def process_file(filename, parfile=False):
    file_OK = f'{filename}_OK.txt' if parfile else output_path('reach_OK.txt')
    file_NG = f'{filename}_NG.txt' if parfile else output_path('reach_NG.txt')
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
