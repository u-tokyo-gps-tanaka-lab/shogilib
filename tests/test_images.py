from shogilib import Position, showstate

def test_images():
    pos = Position.from_fen('Lnsgkgsnl/1r5b1/1pppppppp/9/9/9/1PPPPPPPP/1B5R1/2SGKGSN1[LNllp] w')
    print(pos.fen())
    showstate(pos, filename='state.png')