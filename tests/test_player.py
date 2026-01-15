from shogilib import (
    Player,
    Ptype,
    Piece,
    Position,
    BLACK,
    WHITE,
    can_promote_y,
    player2c,
    Move,
)
from shogilib import (
    KING,
    ROOK,
    BISHOP,
    GOLD,
    SILVER,
    PAWN,
    LANCE,
    KNIGHT,
    BLANK,
    king_checkmate_pawn,
)


def test_player():
    assert WHITE.value == 0
    assert BLACK.value == 1
    assert BLACK == WHITE.flip()
    assert WHITE == BLACK.flip()


def test_player2c():
    assert player2c(WHITE) == "w"
    assert player2c(BLACK) == "b"


def test_player_can_promote_y():
    for y in range(3):
        assert can_promote_y(WHITE, y)
    for y in range(3, 9):
        assert not can_promote_y(WHITE, y)
    for y in range(6):
        assert not can_promote_y(BLACK, y)
    for y in range(6, 9):
        assert can_promote_y(BLACK, y)


def test_player_cmp():
    assert WHITE < BLACK
    assert not BLACK < WHITE
