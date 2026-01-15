from random import randrange
from research.paths import output_path

RANK_LIMIT = 80880932079767835177773204009328769812438521503800714936366945233084532
with open(output_path('RN500M.txt'), 'w') as wf:
    for i in range(500_000_000):
        wf.write(str(randrange(0, RANK_LIMIT)) + '\n')
