from shogilib import Position
def load_fen_list(fname):
    ans = []
    with open(fname) as f:
        for fen in f.readlines():
            pos = Position.from_fen(fen)
            ans.append(pos)
    return ans
def save_fen_list(fname, ls):
    with open(fname, 'w') as wf:
        wf.write('\n'.join(pos.fen() for pos in ls))
        wf.write('\n')
piece_OK = load_fen_list('piece_OK.txt')            
#
print(f'len(piece) = {len(piece_OK)}')
check_OK = []
check_NG = []
for pos in piece_OK:
    if pos.can_capture_op_king():
        check_NG.append(pos)
    else:
        check_OK.append(pos)

save_fen_list('check_OK.txt', check_OK)
save_fen_list('check_NG.txt', check_NG)