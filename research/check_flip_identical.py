from shogilib import Position
from rank import pos2l
from rank_to_fen import flipH_onboards
from pprint import pprint
import argparse

def process_file(filename, parfile=False):
    file_OK = f'{filename}_OK.txt' if parfile else 'flipH_OK_identical_OK.txt'
    file_NG = f'{filename}_NG.txt' if parfile else 'flipH_OK_identical_NG.txt'

    with open(filename) as f:
        with open(file_OK, 'w') as wf1:
            with open(file_NG, 'w') as wf2:
                for fen in f:
                    pos = Position.from_fen(fen)
                    onboards = pos2l(pos)[1]
                    if flipH_onboards(onboards) == onboards:
                        print(f'True: {fen}')
                        wf1.write(fen)
                    else:
                        print(f'False: {fen}')
                        wf2.write(fen)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    parser.add_argument('-p', '--parallel', action='store_true')
    args = parser.parse_args()
    process_file(args.filename, args.parallel)

if __name__ == '__main__':
    main()
