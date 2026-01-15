from shogilib import Ptype

from research.rank_all import count2N, count_ptype
from research.rank import canpromote2comb_table, nopromote2comb_table


def test_count2N():
    c = [
        [[8, 1], [4, 1], [3, 1], [2, 1], [5, 1], [7, 1], [6, 2]],
        [[8, 3], [4, 3], [3, 3], [2, 17], [5, 3], [7, 1]],
    ]
    c = [[(Ptype(pt), v) for pt, v in c[0]], [(Ptype(pt), v) for pt, v in c[1]]]
    ans = count2N(c)
    assert ans == (
        289210612561726463707360299578838583875978852988197273600000,
        (
            [2, 2, 2, 2, 2, 2, 3],
            [632632, 4499200, 3980544, 135341850839413067360501760, 1499264, 200],
        ),
    )


def test_count2N_table():
    for n_empty in [40, 50, 60]:
        for pti, v in [[8, 3], [4, 3], [3, 3], [2, 17], [5, 3], [7, 1]]:
            pt = Ptype(pti)
            if pt.can_promote():
                ans0, combs, _ = canpromote2comb_table[n_empty][v]
            else:
                ans0, combs, _ = nopromote2comb_table[n_empty][v]
            ans1 = count_ptype(pt, n_empty, v)
            assert ans0 == ans1
