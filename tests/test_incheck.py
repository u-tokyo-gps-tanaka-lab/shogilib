from shogilib import (
    Position,
    BLACK,
    WHITE,
)


def test_in_check():
    pos = Position.from_fen(
        "+R3K+P1+Ps/1+L1G3+p+L/3k3+p+p/2N1+p2bL/4+p1P1+p/+s1n2gp2/n1+P+PRP1n1/+sp+Sp1p1G1/1b2+P+L1+P1[g] w"
    )
    assert pos.in_check(BLACK)
    assert pos.side_to_move == WHITE


def test_can_capture_op_king():
    pos = Position.from_fen(
        "+R3K+P1+Ps/1+L1G3+p+L/3k3+p+p/2N1+p2bL/4+p1P1+p/+s1n2gp2/n1+P+PRP1n1/+sp+Sp1p1G1/1b2+P+L1+P1[g] w"
    )
    assert pos.can_capture_op_king()
    assert pos.side_to_move == WHITE
