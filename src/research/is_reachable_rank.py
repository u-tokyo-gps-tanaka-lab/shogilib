import argparse
from shogilib import Position, WHITE, generate_previous_positions
from research.rank import countsum, rank2l, rank2pos
from research.rank_to_fen import flipH_onboards
from research.check_reach import can_reach_KK


def flipH(rank):
    assert rank < countsum
    (hands, onboards) = rank2l(rank)
    onboards1 = onboards[:]
    onboards.sort()
    assert onboards == onboards1
    if flipH_onboards(onboards) < onboards:
        return False
    else:
        return True


def prev(rank):
    pos = rank2pos(rank)
    assert pos.side_to_move == WHITE, f"pos={pos.fen()}"
    poslist = generate_previous_positions(pos)
    if len(poslist) != 0:
        return True
    else:
        return False


def king(rank):
    pos = rank2pos(rank)
    assert pos.side_to_move == WHITE, f"pos={pos.fen()}"
    if not pos.can_capture_op_king():
        return True
    else:
        return False


def piece(rank):
    pos = rank2pos(rank)
    assert pos.side_to_move == WHITE, f"pos={pos.fen()}"
    if pos.legal_piece_positions():
        return True
    else:
        return False


def reach_KK(rank):
    pos = rank2pos(rank)
    assert pos.side_to_move == WHITE, f"pos={pos.fen()}"
    tf, ans = can_reach_KK(pos)
    if tf:
        return True
    else:
        return False


"""
if the given rank is reachable, return True.
"""


def check(rank):
    for f in [flipH, piece, king, prev, reach_KK]:
        status = f(rank)
        print(f"{f.__name__}({rank}) = {status}")
        if not status:
            return False
    return True


def search(rank):
    r = rank
    while True:
        if check(r):
            break
        else:
            if r % 1 == 0:
                print(f"{r} is unreachable.")
        r += 1
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("rank", type=int)
    parser.add_argument("-s", "--search", action="store_true")
    args = parser.parse_args()

    result = search(args.rank) if args.search else check(args.rank)
    print(f"{args.rank} is {'reachable' if result else 'unreachable'}.")


if __name__ == "__main__":
    main()
