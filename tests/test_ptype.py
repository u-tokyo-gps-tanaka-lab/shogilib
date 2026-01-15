import random
from shogilib import (
    BLACK,
    WHITE,
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
)


def test_ptype_promote():
    for pt in [PAWN, LANCE, KNIGHT, SILVER, BISHOP, ROOK]:
        assert pt.can_promote()
        assert not pt.is_promoted()
        assert pt.promote().is_promoted()
        assert pt.promote().unpromote() == pt
    for pt in [KING, GOLD]:
        assert not pt.can_promote()
        assert not pt.is_promoted()


def test_must_promote_y():
    assert PAWN.must_promote_y(WHITE, 0)
    assert PAWN.must_promote_y(BLACK, 8)
    assert not PAWN.must_promote_y(WHITE, 1)
    assert not PAWN.must_promote_y(BLACK, 7)
    assert LANCE.must_promote_y(WHITE, 0)
    assert LANCE.must_promote_y(BLACK, 8)
    assert not LANCE.must_promote_y(WHITE, 1)
    assert not LANCE.must_promote_y(BLACK, 7)
    assert KNIGHT.must_promote_y(WHITE, 0)
    assert KNIGHT.must_promote_y(BLACK, 8)
    assert KNIGHT.must_promote_y(WHITE, 1)
    assert KNIGHT.must_promote_y(BLACK, 7)
    assert not KNIGHT.must_promote_y(WHITE, 2)
    assert not KNIGHT.must_promote_y(BLACK, 6)


def test_order():
    assert PAWN.promote() < PAWN
    ptypes = [KING, GOLD, KNIGHT, LANCE, PAWN, SILVER, ROOK, BISHOP]
    for i0, pt0 in enumerate(ptypes):
        for i1, pt1 in enumerate(ptypes):
            if i0 < i1:
                assert pt0 < pt1
                assert pt0 < pt1.promote()
                assert pt0.promote() < pt1
                assert pt0.promote() < pt1.promote()
            elif i0 == i1:
                assert not pt0 < pt1
                if pt0.can_promote():
                    assert not pt0 < pt1.promote()
                    assert pt0.promote() < pt1
            else:
                assert not pt0 < pt1
    ptypes1 = random.sample(ptypes, len(ptypes))
    ptypes1.sort()
    assert ptypes == ptypes1
