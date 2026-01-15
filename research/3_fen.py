import shogilib
from check_reach import distance_to_KK, can_reach_KK

paper_fens = [
    "1+P1+l2+p+P+N/2+r+LgP+b1P/n+pRp1+p3/1P+L1+pL3/3+p3+S1/1g1n3+s1/GS1k3Sg/pK1+p5/+p+B+nPP1+PP1[] b",
    "1+P1+l2+p+P+N/2+r+LgP+b1P/n+pRp1+p3/1P+L1+pL3/3+p3+S1/1g5+s1/GS1k3Sg/pKn+p5/+p+B+nPP1+PP1[] w",
    "1+P1+l2+p+P+N/2+r+LgP+b1P/n+pRp1+p3/1P+L1+pL3/3+p3+S1/1g5+s1/G2k3Sg/pKS+p5/+p+B+nPP1+PP1[N] b",
    "1+P1+l2+p+P+N/2+r+LgP+b1P/n+pRp1+p3/1P+L1+pL3/3+p3+S1/1g5+s1/G2k3Sg/pK+p6/+p+B+nPP1+PP1[Ns] w"
]

results5B = [
    "1+P1+l2+p+P+N/2+r+LgP+b1P/n+pRp1+p3/1P+L1+pL3/3+p3+S1/1g5+s1/GSpk3Sg/pK1+n5/+p+B+nPP1+PP1[] b",
    "1+P1+l2+p+P+N/2+r+LgP+b1P/n+pRp1+p3/1P+L1+pL3/3+p3+S1/1g5+s1/GSpk3Sg/pK+n6/+p+B+nPP1+PP1[] w",
    "1+P1+l2+p+P+N/2+r+LgP+b1P/n+pRp1+p3/1P+L1+pL3/3+p3+S1/1g5+s1/G1pk3Sg/pKS6/+p+B+nPP1+PP1[N] b",
    "1+P1+l2+p+P+N/2+r+LgP+b1P/n+pRp1+p3/1P+L1+pL3/3+p3+S1/1g5+s1/G2k3Sg/pK+p6/+p+B+nPP1+PP1[Ns] w"
]

print([distance_to_KK(shogilib.Position.from_fen(pos)) for pos in paper_fens])
print([distance_to_KK(shogilib.Position.from_fen(pos)) for pos in results5B])

print(can_reach_KK(shogilib.Position.from_fen(paper_fens[3])))
print(can_reach_KK(shogilib.Position.from_fen(results5B[3])))