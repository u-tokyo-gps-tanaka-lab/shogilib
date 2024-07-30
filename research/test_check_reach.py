from shogilib import Position
from check_reach import distance_to_KK, can_reach_KK

def test_distance_to_KK():
    pos = Position.from_fen('k8/9/9/9/9/9/9/9/8K[pppppppppPPPPPPPPPllLLnnNNssSSggGGbBrR] b')
    assert distance_to_KK(pos) == 0
    pos = Position.from_fen('k8/9/ppppppppp/9/9/9/9/9/8K[PPPPPPPPPllLLnnNNssSSggGGbBrR] b')
    assert distance_to_KK(pos) == 90

def test_can_reach_KK():
    pos = Position.from_fen('3+S2G+P1/P1K1P1+r2/1ps+p+p1R1P/3+Bk+p3/b2+s3n+p/N2L1p1p1/1+ngg2pS1/L1+p+P+N1+pPg/L2+l2+P+P1[] b')
    assert can_reach_KK(pos)[0]
    pos = Position.from_fen('k8/9/9/9/9/9/9/9/8K[pppppppppPPPPPPPPPllLLnnNNssSSggGGbBrR] b')
    assert pos.is_consistent()
    assert can_reach_KK(pos)[0]
    pos = Position.from_fen('k8/9/ppppppppp/9/9/9/9/9/8K[PPPPPPPPPllLLnnNNssSSggGGbBrR] b')
    assert pos.is_consistent()
    assert can_reach_KK(pos)[0]

def main():
    pos = Position.from_fen('3+S2G+P1/P1K1P1+r2/1ps+p+p1R1P/3+Bk+p3/b2+s3n+p/N2L1p1p1/1+ngg2pS1/L1+p+P+N1+pPg/L2+l2+P+P1[] b')
    assert can_reach_KK(pos)[0]

if __name__ == '__main__':
    main()