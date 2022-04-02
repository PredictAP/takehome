def index(args):
    pass


def search(args):
    if args.name == None and args.size == None and args.type == None:
        print("Specify at least one search function and corresponding criteria.")


def build_parser():
    import os
    import argparse

    parser = argparse.ArgumentParser(
        description="Index a directory tree and search for the files within."
    )
    subparsers = parser.add_subparsers(required=True)

    index_parser = subparsers.add_parser("index", help="Index a directory tree.")
    index_parser.add_argument(
        "directory",
        nargs="?",
        metavar="DIRECTORY",
        default=os.getcwd(),
        help="""Index the given directory. If no argument is supplied, will 
        index the current working directory.""",
    )
    index_parser.set_defaults(func=index)

    search_parser = subparsers.add_parser("search", help="Perform a search query.")
    search_parser.add_argument(
        "-n",
        "--name",
        metavar="FILENAME",
        help="""Search for files by filename. Must supply part or all of a 
        filename as a positional argument to this flag.""",
    )
    search_parser.add_argument(
        "-s",
        "--size",
        nargs=2,
        metavar=("FILESIZE", "SCALE"),
        help="""Search for files by filesize. Must supply the filesize as two 
        positional arguments to this flag: the first argument is the 
        quantitative size, and the second argument is the scale. For example, 
        an argument of '4 M' corresponds to a size of 4 megabytes. Searching is 
        only supported for byte (B), kilobyte (K), megabyte (M), and gigabyte 
        (G) scales.""",
    )
    search_parser.add_argument(
        "-t",
        "--type",
        metavar="FILETYPE",
        help="""Search for files by filetype. Must supply the filetype as a 
        positional argument to this flag.""",
    )
    search_parser.set_defaults(func=search)

    return parser


if __name__ == "__main__":
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)
