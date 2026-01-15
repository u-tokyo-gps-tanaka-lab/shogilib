from shogilib import Position, showstate, show_images_hv
import argparse


def single_fen(fen, filename="state.png"):
    pos = Position.from_fen(fen)
    # assert pos.fen() == fen
    print(pos.fen())
    print(f"Exporting to {filename}")
    showstate(pos, filename=f"{filename}")


def multiple_fen(fenlist, filename="state_series.png"):
    images = [showstate(Position.from_fen(fen)) for fen in fenlist]
    print(f"Exporting to {filename}")
    show_images_hv(images, 4, filename=f"{filename}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--single", nargs="+", type=str)
    parser.add_argument("-m", "--multiple", nargs="*")
    args = parser.parse_args()
    if args.single:
        single_fen(args.single[0])
    elif args.multiple:
        multiple_fen(args.multiple)
    else:
        print("No arguments")


if __name__ == "__main__":
    main()
