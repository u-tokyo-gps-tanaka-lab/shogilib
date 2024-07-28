from shogilib import Position
def load_fen_list(fname):
    ans = []
    with open('flipH_OK.txt') as f:
        for fen in f.readlines():
            pos = Position.from_fen(fen)
            ans.append(pos)
    return ans
def save_fen_list(fname, ls):
    with open(fname, 'w') as wf:
        wf.write('\n'.join(pos.fen() for pos in ls))
        wf.write('\n')
flipH_OK = load_fen_list('flipH_OK.txt')            
#
print(f'len(flipH_OK) = {len(flipH_OK)}')
piece_OK = []
piece_NG = []
for pos in flipH_OK:
    if pos.legal_piece_positions():
        piece_OK.append(pos)
    else:
        piece_NG.append(pos)

save_fen_list('piece_OK.txt', piece_OK)
save_fen_list('piece_NG.txt', piece_NG)

