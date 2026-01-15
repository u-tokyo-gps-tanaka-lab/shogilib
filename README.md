# shogilib

Codes and raw results of the paper "Statistical estimation of the number of legal positions in Shogi" (https://ipsj.ixsq.nii.ac.jp/records/240740
 (in Japanese)), presented at IPSJ Game Programming Workshop 2024.

"将棋の実現可能局面数の推計" https://ipsj.ixsq.nii.ac.jp/records/240740 で使用したコードと実験結果です。

## Reproduce the experiment

This project requires [uv](https://github.com/astral-sh/uv) for dependency management.

### Setup

```
$ uv sync
$ cd src/research
```

You need to have IPAGothic font in your system to visualize positions.

### 1. generate $S_{all}$ and rank its elements

```bash
$ uv run python rank_all.py
```

If the program works correctly, you should see the following outputs and get `count2i.json`. `16014219505238849250` is the number of elements in $S_{all}$.

```text
### 1. generate $S_{all}$ and rank its elements

```bash
$ uv run python rank_all.py
```

If the program works correctly, you should see the following outputs and get `count2i.json`. `16014219505238849250` is the number of elements in $S_{all}$.

```text
make_count_sub(i=7) return len(ans)=3
make_count_sub(i=6) return len(ans)=9
make_count_sub(i=5) return len(ans)=45
make_count_sub(i=4) return len(ans)=855
make_count_sub(i=3) return len(ans)=4275
make_count_sub(i=2) return len(ans)=21375
make_count_sub(i=1) return len(ans)=106875
80880932079767835177773204009328769812438521503800714936366945233084532
```

### 2. generate random integers (position ranks)

```bash
$ uv run python random_number_10K.py
$ uv run python random_number_500M.py # requires a few GB of storage
```

They will create `RN10K.txt` and `RN500M.txt` respectively. The former is for testing and the latter for the main experiment.

### 3. check the legality of the positions

```bash
$ uv run python rank_to_fen.py ../../research/RN500M.txt
```

`rank_to_fen.py` reads the random ranks, generates pseudo-legal positions corresponding to them, and checks if they are identical when flipped horizontally. It creates `flipH_[OK,NG].txt` in default.

```bash
$ uv run python check_piece.py ../../research/flipH_OK.txt
$ uv run python check_king.py ../../research/piece_OK.txt
$ uv run python check_prev.py ../../research/king_OK.txt
$ uv run python check_reach.py ../../research/prev_OK.txt
```

After running these commands, you will be able to estimate the number of reachable positions in Shogi using interval estimation of the population proportion of $S_{all}$.
