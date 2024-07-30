from shogilib import Position, generate_previous_positions

def load_fen_list(fname):
    ans = []
    with open(fname) as f:
        for fen in f.readlines():
            fen = fen.rstrip()
            pos = Position.from_fen(fen)
            ans.append(pos)
    return ans
def save_fen_list(fname, ls):
    with open(fname, 'w') as wf:
        wf.write('\n'.join(pos.fen() for pos in ls))
        wf.write('\n')
check_OK = load_fen_list('check_OK.txt')            
#
print(f'len(piece) = {len(check_OK)}')
prev_OK = []
prev_NG = []
prev_NG_nocheck = []
for pos in check_OK:
    #print(pos.fen())
    poslist = generate_previous_positions(pos)
    if len(poslist) == 0:
        prev_NG.append(pos)
        if not pos.in_check(pos.side_to_move):
            prev_NG_nocheck.append(pos)
    else:
        prev_OK.append(pos)

save_fen_list('prev_OK.txt', prev_OK)
save_fen_list('prev_NG.txt', prev_NG)
save_fen_list('prev_NG_nocheck.txt', prev_NG_nocheck)