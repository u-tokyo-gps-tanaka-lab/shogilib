from shogilib import Position, showstate, show_images_hv
from shogilib import Position, WHITE
from research.paths import output_path

# read from ~ktanaka/work/shogilib/research/reach_NG.txt
reach_NG = [
    "+P1S2+n1lS/P3p+b+R1+P/9/2Np+pG2p/1b2Gp1+n1/p+p1+pN3+p/1ks+PLgPS+p/1g3+P2+P/+P+RKL5[L] w",
    "k1+n2n1+p+l/1+r1P+P+P+p2/1K1g+P+P1+s1/7P+p/1G4+b+n+s/+p1+b+pS1lNP/3p2+p1+l/1PP2gR+S1/1+P+P+l5[g] w",
    "6g+p1/LG4+P1s/2+p1b+n1+p1/1+sp5P/P1gRP1p2/4K1P+pn/SgP+p2s+Pb/1p1L1+PNL1/3k+r+P2+l[NP] w",
    "+p2+s3+p1/+lk3+S1p1/L+pN3+P+P1/K+R1lg1g1+p/pLp2+PNPp/+p1PPp1+n1n/4r2B1/S+p4g2/1G3+p+b1+s[] w",
    "+p1+P1g4/2+P1n+B+p2/R+P2P+P3/+PKPP1p1l+s/3G1+sLS1/p2+p2bN1/+P2p5/l1N2+p1p1/k+r+S+lg1+nG+P[] w",
    "+p2+P+n1+s1+l/1+P1+P+pn2p/1g+S+b4+B/+lg+nn5/k1l+p4+P/+p1+R1+P1G+l1/+RK1g+P2S1/PP2pP+P1+s/5+p3[p] w",
    "2+S3g+P+l/1+S2nP+pn1/p1+pkl+R1pp/l1+n2+Pg1b/N1p1KG3/4S1+p2/P2+P2p1+r/2+s+bp2+P1/+pL2+p2G1[p] w",
    "+pkp+P+P+s3/1n+b2B+r+P+s/1L1+N+pP2G/K1G+L+L4/PR3+S+p2/2+n+p5/1+p2+p2s+L/2Pg4p/+pG2N+P1+p1[p] w",
    "+PS+p1p4/+PP3+PS1R/pp1P1+n1+l1/+psg+PrP1+n1/2kp3+p1/G+pl1g4/+BKS+N3G1/+l+N3+p3/+P+p2+bL3[] w",
    "G3+p4/2sp+p+s1p1/3+LPp+p1N/k+l+R+RnGp+L1/N1K4+p1/+PSP3+P+s1/3nG+l+p2/1Gp+P+p2Bp/4+p+b3[] w",
    "+p1K5+R/s5+p+S+P/1k1G4p/+bN+r+L2+p2/1pg+P+p2N1/gPp+L1+p1gP/l+P1n+N2+P+B/1+p4p1S/+P+P2+S+l3[] w",
    "+p4pp1g/1pSP1P1+P+n/1N2P2+pL/g1gb+pg1+P1/Pk1+S3p1/1bN1+p1P2/+PRK+S2N+S1/+rL5L1/+p4+P2+l[] w",
    "1Sr1p+P1p1/G+B+bk2+P2/1K1n1+Pp2/1+Lp5l/Pg+n1+P3P/p+PP+PPR1P+n/1G1p2S2/1GL3L1+S/1+S7[Np] w",
    "1+Pbk2+p+L1/1+s1+l1G2+r/1+Pp+NK1+P1+n/p2+pP+p1+sP/3Np4/+B2+n5/2g2p1+p+p/s1+LP2L1g/rg2S1+P+p1[p] w",
    "2+P1+p1G2/1n+lG1+p1p+P/+P3+P2+P+p/pg5L+n/N4+S3/Pb1L1gP2/k1p+P+r+p+p1+S/+s3+L1+Pb1/+RK1+P2+n1S[] w",
    "+B1+Lg1+S3/3G5/+L2nPN1P1/2sP+l2g1/+p1+PgB4/P+P+pN+P+p1s1/1+RPk2P1+p/p2s4N/+P1K+R+P3P[Lp] w",
    "1p+r3+PG1/+P4+p+Ls+p/+p1N2Pr+n1/k1K2+s3/p+b2+p1P1+l/1+Nsb5/l+p+s2g2+P/1P4+nG1/1+p+p+p+L2gP[p] w",
    "1g+P+P+p+L2g/GG2+PPkn1/2K3+r1r/+lBS1+P+P1p+L/1+p2+Pp+P1p/4N1p+b+n/2SpP2n1/1+S5+l1/3+s1+p3[P] w",
    "g+p2+P+l1+pp/+n+p2Gp1S+R/p+Pp4+s1/3+lG1pP1/R2L3+nG/+p+n1+p1+b1+P1/2k3+P+P1/K+p1+n5/+B+Ls3P1S[] w",
    "2+P+l+P4/3G2pr1/1s1l4N/G2p3+n+p/3P1+p+p2/nk3pB+P1/1+p2P+sL+n+p/KLp+Sp1+BG1/1+R1+P1Psg1[P] w",
    "s4+S2p/2p4PP/+P3KS3/+pPk2G1+Lb/1p+b1P+P+l+n1/2+R3+P+p1/pg1+p1pP1N/1s1p2G1N/1+PLL1GRN1[] w",
    "2+n+P1+P+N2/p1+PG+p1Sgg/2P+p2g+P+P/k3s2B+s/s3+P1L2/+RKp1pp2L/+N+N1+P3+B1/+P1+l5+p/2+PR3L+p[] w",
    "G1gp+p+l+n1+p/1PG5P/l4+s+p+S1/4+p3n/+P1kP1p2+p/K+p+rs2+p1+R/B1+P+P5/1L1+SN4/G+p1L+n2B1[Pp] w",
    "k1+P6/1+rK2ls2/B+PP3+pg1/5pBN1/P2L3+p1/2+p1g1+RpG/+P+p+LPNSp1P/2NpG1N+s+P/2+P3+L1+p[s] w",
    "1B+p2b1gG/3+p1+nnS+p/2+N3+P2/1+P+P1+P+S+l1+P/4+l1+p+P+p/1R+P1L+l2g/k2+S2+pp1/g5+N1+s/+RK+P6[ppp] w",
    "1s2+S1l2/+ppPp1+Np+p1/P3+p+P1p1/p1+P1k2n1/1LK+p2r2/Ng+R1+L3+S/1L+Pn2g2/3P+pb1g1/1+B2G1+P1+S[p] w",
    "4+P4/+p1+s1P+L+P1P/p4n3/4+P1G2/1S2+P+ppP+B/+P1g1+N2l1/+n1kp+lS1+Ps/+NP+p2g3/1r+RKL2Gb[PP] w",
    "K+R+P6/1+bg+sP+s1+p+L/1k1+pl1+PN1/2np+r1l1+P/n2n3+bP/p2+P1G1Sp/4L2+p1/+p1+PG+pP3/S4+P1+pG[] w",
    "g1+n+l3+p+p/+R+sk1P1P+pG/K4n+pp1/b1l+sGp2P/3+P4L/+P2L3SG/+PP+r3+N1+B/Pp2+p2Np/5+p2+s[] w",
    "p+ls+ng3G/1p2l+p2n/1+P3+N+p+P1/2+p+p1+L2r/k+p+RP+b+N3/2KB4G/5+p+P1+P/1P2+s1sp+P/S2+p2+l+p1[g] w",
    "+Bg2S+p+N+P+n/+p3S+p1+p1/+L2+L2+pB1/+L2S+p4/pp1G4n/1+P1+n2+r+P1/G+sP+l1+P3/1k2Pg+p2/1r+pK+P4[p] w",
    "+P1+P1b1+p+p1/2+Pgp2+L1/p3k+pG2/LP1+ln2+P1/N2+P+RgPL1/1+P1K1+s+S+s1/1N+p1+p3+B/1R2+n+p2s/1+p3g1P1[] w",
    "1+s5r1/1+p1+p+N3+p/3+lgnNL+P/P+R1+B1nP2/2P+p+P+p3/+S1spP1+P1G/g1k4L1/+p+p1l1p+p1s/+BPK5G[] w",
    "+L+p5+n1/+P2+Lbp1+pg/+RskpS+Pn2/K4+p3/1+Ng+p1+P+P2/1S3g1+P1/P3l4/+N1P+L+p3+p/+BPS1GP+RP1[] w",
    "3B1n+P1p/2+p2+l+lG+s/+pbLs+n1N+PS/1+pk+pg2+p1/2n1PR3/1pR1+P1+P1g/3K1p+p2/2L1+P2G+P/6+PS+P[] w",
    "+Rbkn5/K1sL1+p+P1g/2g1+P2+S1/1pp1+P4/2+n1p1+P+L+l/S+P3+p2+b/l2P+sp1P1/P+pG3+ppN/2N1r2G+P[] w",
    "+Pl3pp1p/1+PL6/2L1+p+p1+Pg/1+p+BpG+p+P2/1+bp1sn3/4PR1+n1/p3k4/1+P2s1GS1/+N+s+PK+R+L1Ng[p] w",
    "n+rB+P2+S+P1/P1kS1Gg2/+P1p1+pL2n/l4+p1b+p/N1P+sPP1P+r/S4+p+P+P1/1K1G1L3/4+P1+L1p/3+N2g+p1[] w",
    "2p1p3p/+P2k2+p1G/+p2g5/SpKL2P2/1g+N5+n/1+PBLr1+ns+P/1B1N1+p3/l+pR1PSp2/1gL1+SP2+p[pp] w",
    "4+Pr3/l1+p1+p2PP/1k1G1+P1p1/l2+n2PL1/K+N2p2Bs/p3G1+BN+p/+P5s1p/+s1l+P+r+S+p2/P2G1P2g[Np] w",
    "4+S3G/1+rssG+Ppsb/2Gp1+L1+pg/+p1+nP3+P1/PPp3P1P/1+R+lk2+p2/nK1N1P2+n/2+p1P+p1P1/2+LbL4[] w",
    "+ppk+p+n1G2/2+p3P1+p/1+P+RKp+L+p1p/gN2+P3+s/1L2L3+p/+S1L1+n3+p/1+pP1g1+P2/2r2B2+S/1PG1+b+s+N2[p] w",
    "1+nl+s+l2+B1/+P1S+pb4/+p+P2+p2g1/1p+p3np1/N+N1S2pG1/+P+p+L+PPl3/+p3Gp+P+R1/+Rgk1p4/K2+s3P1[] w",
    "+B+p1+Pg1+p2/p1P4k+p/+SK6+r/4L+P1+PG/3P3+P1/N1+N1NrpP1/+P+sg+P1g+p2/S+L1l1+n2+p/+P1s1L4[Bp] w",
    "+p+S5+p1/4+P2b1/rp1+p1+N1g1/2+P1kb1+P+N/4+s1L+N+p/1+ppK+P1+l2/N+S1+P2SPG/2G1pP2l/+p+pL4R+P[g] w",
    "1+N3+B1S1/9/P+pG1Rs2p/2+np5/kg+P2+P2P/s1l+N1P3/+RKGP+p+pG1s/Lp+l2pp+b1/1+PP1L+P1+N1[p] w",
    "g4+p+N1+p/2b3P1+p/n+P4G2/1pb1k2+PN/3L+l2S1/1+L1KRPnPR/+p1+P1L1+P2/+SGPS+P+pp+p1/1G+P6[s] w",
    "2k1+p+n3/+Lg5l1/+BK1P3+PR/gs+pp3+p1/+pP2b+P2N/4p+p2+p/1+p1nR1L+p+n/1+S2g1G2/+P+P+p+P+S+s2L[] w",
    "l5+p1g/+S1n2b1G1/+p+R4s1s/+p+n+l+Pn+p3/1N+S3lB1/1pp+P1gG+p+p/k2p1+P+P+p1/+p2+l5/+RK1P+p2+p1[] w",
    "G+S2+s+Bp2/5pP2/2+p+lK1+nL+P/+pgkp3+Rr/4+P2+L1/+p1+P4+PB/+SP2N2+PN/P+Lg1+S2+p1/3+nG1+P+P1[P] w",
    "pk2+P3+P/1+p+pS1G2g/K+RP+P+P3s/3pL+n+S1+N/2s3+P1p/4G+P1P+p/nL2+PG+bpP/+rl1B5/2+p5+N[l] w",
]

images = [showstate(Position.from_fen(fen)) for fen in reach_NG]
show_images_hv(images, 7, filename="reach_NG.png")

reach_NG_nocheck = []

for fen in reach_NG:
    pos = Position.from_fen(fen)
    assert pos.is_consistent()
    assert pos.legal_piece_positions()
    if not pos.in_check(WHITE):
        reach_NG_nocheck.append(fen)


def save_fen_list(fname, ls):
    with open(fname, "w") as wf:
        wf.write("\n".join(pos.fen() for pos in ls))
        wf.write("\n")


save_fen_list(output_path("reach_NG_nocheck.txt"), reach_NG_nocheck)

print(f"Total={len(reach_NG_nocheck)}")
