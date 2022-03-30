import argparse
import pandas as pd


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("infile", type=str)
    arg_parser.add_argument("-n", type=str)
    arg_parser.add_argument("-e", type=str)
    arg_parser.add_argument("-l", type=int)
    arg_parser.add_argument("-g", type=int)
    args = arg_parser.parse_args()

    df = pd.read_json(args.infile)

    if args.n:
        df = df[df.name.str.contains(args.n)]
    if args.e:
        df = df[df.ext == args.e]
    if args.l:
        df = df[df.filesize < args.l]
    if args.g:
        df = df[df.filesize > args.g]

    print(df)

if __name__ == "__main__":
    main()