from shogilib import Position
from research.rank import pos2l
from research.rank_to_fen import flipH_onboards
from research.paths import OUTPUT_DIR
from pprint import pprint
import argparse, os

def process_file(filename, parfile=False, output_dir='.'):
    base_filename = os.path.basename(filename)
    
    if parfile:
        file_OK = os.path.join(output_dir, f'{base_filename}_OK.txt')
        file_NG = os.path.join(output_dir, f'{base_filename}_NG.txt')
    else:
        file_OK = os.path.join(output_dir, 'flipH_OK_identical_OK.txt')
        file_NG = os.path.join(output_dir, 'flipH_OK_identical_NG.txt')

    with open(filename) as f:
        with open(file_OK, 'w') as wf1:
            with open(file_NG, 'w') as wf2:
                for fen in f:
                    pos = Position.from_fen(fen)
                    onboards = pos2l(pos)[1]
                    if flipH_onboards(onboards) == onboards:
                        print(f'True: {fen.strip()}')
                        wf1.write(fen)
                    else:
                        print(f'False: {fen.strip()}')
                        wf2.write(fen)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    parser.add_argument('-p', '--parallel', action='store_true')
    parser.add_argument('-o', '--output_dir', default=OUTPUT_DIR, help='Directory to store output files.')
    args = parser.parse_args()
    process_file(args.filename, args.parallel, args.output_dir)

if __name__ == '__main__':
    main()
