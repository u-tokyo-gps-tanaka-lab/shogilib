from collections import deque
from shogilib import Position, showstate
import re

players = ["Sente", "Gote"]


# チェビシェフ距離（隣接判定）
def adjacent(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return max(abs(x1 - x2), abs(y1 - y2)) == 1


def pos2fen(sente, gote, side):
    fen = ""
    sente_x, sente_y = sente
    gote_x, gote_y = gote

    for x in range(1, 10):
        for y in range(1, 10):
            if (x, y) == (sente_x, sente_y):
                fen += "K" if side == "Sente" else "k"
            elif (x, y) == (gote_x, gote_y):
                fen += "k" if side == "Sente" else "K"
            else:
                fen += "1"
        fen += "/"

    result = ""
    for s in fen.split("/")[:-1]:
        line = re.sub(r"\d+", lambda x: str(sum(int(digit) for digit in x.group())), s)
        result += line + "/"
    result = result[:-1]
    result += "[] b" if side == "Sente" else "[] w"

    return result


# KK局面の全列挙
KK = []
pos2index = {}
index2pos = {}
index = 0

for sente_x in range(1, 10):
    for sente_y in range(1, 10):
        for gote_x in range(1, 10):
            for gote_y in range(1, 10):
                if (sente_x, sente_y) != (gote_x, gote_y):
                    for side in players:
                        pos = ((sente_x, sente_y), (gote_x, gote_y), side)
                        # 非合法局面の除去
                        if adjacent((sente_x, sente_y), (gote_x, gote_y)):
                            continue

                        KK.append(pos)
                        pos2index[pos] = index
                        index2pos[index] = pos
                        index += 1

print(f"KK Total={index}")
# pprint.pprint(pos2index)
# pprint.pprint(index2pos)


def generate_next_pos(pos, pos_to_index: dict):
    king_moves = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    (sente_x, sente_y), (gote_x, gote_y), side = pos
    states = []

    if side == "Sente":
        # 先手
        for dx, dy in king_moves:
            new_sente_x = sente_x + dx
            new_sente_y = sente_y + dy
            if 1 <= new_sente_x <= 9 and 1 <= new_sente_y <= 9:
                if (new_sente_x, new_sente_y) != (gote_x, gote_y) and not adjacent(
                    (new_sente_x, new_sente_y), (gote_x, gote_y)
                ):
                    new_pos = ((new_sente_x, new_sente_y), (gote_x, gote_y), "Gote")
                    if new_pos in KK:
                        states.append(new_pos)
                    else:
                        raise Exception(f"Invalid state: {new_pos}")
    else:
        # 後手
        for dx, dy in king_moves:
            new_gote_x = gote_x + dx
            new_gote_y = gote_y + dy
            if 1 <= new_gote_x <= 9 and 1 <= new_gote_y <= 9:
                if (new_gote_x, new_gote_y) != (sente_x, sente_y) and not adjacent(
                    (new_gote_x, new_gote_y), (sente_x, sente_y)
                ):
                    new_pos = ((sente_x, sente_y), (new_gote_x, new_gote_y), "Sente")
                    if new_pos in KK:
                        states.append(new_pos)
                    else:
                        raise Exception(f"Invalid state: {new_pos}")
    return states


# 状態遷移グラフの構築
adj = [[] for _ in range(len(KK))]

for idx, pos in enumerate(KK):
    states = generate_next_pos(pos, pos2index)
    ranks = [pos2index[state] for state in states]

    for s, r in zip(states, ranks):
        assert pos2index[s] == r
        assert index2pos[r] == s

    adj[idx] = ranks

start_pos = ((9, 5), (1, 5), "Sente")
start_rank = pos2index[start_pos]
showstate(Position.from_fen(pos2fen(*start_pos)), filename="kk-start.png")


def dfs(start):
    visited = [False] * len(KK)

    stack = deque()
    stack.append(start)
    visited[start] = True

    while stack:
        frm = stack.pop()
        for to in adj[frm]:
            if visited[to]:
                continue
            visited[to] = True
            stack.append(to)

    return visited


visited = dfs(start_rank)
if all(visited):
    print("DFS Sucess")
else:
    print("DFS Failure")
