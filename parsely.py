import os
import json


INDEX_FILENAME = "parsely_index.json"
FILESIZE_FUZZ_FACTOR = 0.1


def build_index(directory, files=[]):
    with os.scandir(directory) as items:
        for item in items:
            if item.is_dir():
                build_index(item.path, files)
            else:
                files.append(
                    {
                        "path": os.path.abspath(item.path),
                        "name": item.name.split(".")[0],
                        "size": item.stat().st_size,
                        "type": item.name.split(".")[1],
                    }
                )

    return files


def persist_index(index):
    with open(INDEX_FILENAME, "w") as file:
        json.dump(index, file)


def load_index():
    with open(INDEX_FILENAME, "r") as file:
        index = json.load(file)

    return index


def index(args):
    persist_index(build_index(args.directory))


def search_filename(name, filtered):
    return [file for file in filtered if file["name"].find(name) != -1]


def search_filesize(size, scale, filtered):
    if scale != "B" and scale != "K" and scale != "M" and scale != "G":
        print(
            "Invalid scale provided. Please try again with one of the "
            + "following: B for bytes, K for kilobytes, M for megabytes, and G "
            + "for gigabytes."
        )
        return

    scale_table = {"B": 1, "K": 1000, "M": 1000000, "G": 1000000000}
    size_query = size * scale_table[scale]
    floor = size_query - (size_query * FILESIZE_FUZZ_FACTOR)
    ceiling = size_query + (size_query * FILESIZE_FUZZ_FACTOR)

    return [
        file for file in filtered if file["size"] >= floor and file["size"] <= ceiling
    ]


def search_filetype(type, filtered):
    return [file for file in filtered if file["type"] == type]


def print_results(filtered):
    print(filtered)


def search(args):
    if args.name == None and args.size == None and args.type == None:
        print("Specify at least one search function and corresponding criteria.")
    if not os.path.isfile(INDEX_FILENAME):
        print(
            "There is no existing index file. Run this program with the index "
            + "command and try your search again."
        )

    filtered = load_index()

    if args.name != None:
        filtered = search_filename(args.name, filtered)

    if args.size != None:
        filtered = search_filesize(int(args.size[0]), args.size[1], filtered)

    if args.type != None:
        filtered = search_filetype(args.type, filtered)

    print_results(filtered)


def build_parser():
    import argparse

    parser = argparse.ArgumentParser(
        description="Index a directory tree and search for the files within."
    )
    subparsers = parser.add_subparsers(required=True)

    index_parser = subparsers.add_parser(
        "index",
        help="""Index a directory tree.""",
    )
    index_parser.add_argument(
        "directory",
        metavar="DIRECTORY",
        help="""Index the given directory. Must supply a directory path as a 
        positional argument.""",
    )
    index_parser.set_defaults(func=index)

    search_parser = subparsers.add_parser(
        "search",
        help="""Perform a search query.""",
    )
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
