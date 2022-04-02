import os
import sys
import json


# Shared constants
INDEX_FILENAME = "parsely_index.json"

PATH = "path"
NAME = "name"
SIZE = "size"
TYPE = "type"

BYTE = "B"
KILO = "K"
MEGA = "M"
GIGA = "G"


def build_index(directory, files=[]):
    with os.scandir(directory) as items:
        for item in items:
            if item.is_dir():
                build_index(item.path, files)
            else:
                filename, filetype = os.path.splitext(item.name)
                files.append(
                    {
                        PATH: os.path.abspath(item.path),
                        NAME: filename,
                        SIZE: item.stat().st_size,
                        TYPE: filetype,
                    }
                )

    return files


def persist_index(index):
    WRITE_FLAG = "w"
    with open(INDEX_FILENAME, WRITE_FLAG) as file:
        json.dump(index, file)


def load_index():
    READ_FLAG = "r"
    with open(INDEX_FILENAME, READ_FLAG) as file:
        index = json.load(file)

    return index


def index(args):
    persist_index(build_index(args.directory))


def search_filename(name, filtered):
    return [file for file in filtered if file[NAME].find(name) != -1]


def search_filesize(size, scale, filtered):
    scale_table = {BYTE: 1, KILO: 1000, MEGA: 1000000, GIGA: 1000000000}
    if not scale in scale_table:
        sys.exit(
            "Invalid scale provided. Please try again with one of the "
            + f"following: {BYTE} for bytes, {KILO} for kilobytes, {MEGA} for "
            + f"megabytes, and {GIGA} for gigabytes."
        )

    FILESIZE_FUZZ_FACTOR = 0.1
    size_query = size * scale_table[scale]
    floor = size_query - (size_query * FILESIZE_FUZZ_FACTOR)
    ceiling = size_query + (size_query * FILESIZE_FUZZ_FACTOR)

    return [file for file in filtered if file[SIZE] >= floor and file[SIZE] <= ceiling]


def search_filetype(type, filtered):
    return [file for file in filtered if file[TYPE] == type]


def print_results(filtered):
    if len(filtered) == 0:
        sys.exit("No results found for the given search query.")

    print("Found the following result(s) from the given search query.")
    for item in filtered:
        print(f"{item[NAME]}{item[TYPE]} located at {item[PATH]}")


def search(args):
    if args.name == None and args.size == None and args.type == None:
        sys.exit("Specify at least one search function and corresponding criteria.")
    if not os.path.isfile(INDEX_FILENAME):
        sys.exit(
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
        help="Index a directory tree.",
    )
    index_parser.add_argument(
        "directory",
        nargs="?",
        metavar="DIRECTORY",
        default=os.getcwd(),
        help="Index the given directory. If no path is supplied, will index "
        + "the current working directory.",
    )
    index_parser.set_defaults(handler=index)

    search_parser = subparsers.add_parser(
        "search",
        help="Perform a search query.",
    )
    search_parser.add_argument(
        "-n",
        "--name",
        metavar="FILENAME",
        help="Search for files by filename. Must supply part or all of a "
        + "filename as a positional argument to this flag.",
    )
    search_parser.add_argument(
        "-s",
        "--size",
        nargs=2,
        metavar=("FILESIZE", "SCALE"),
        help="Search for files by filesize. Must supply the filesize as two "
        + "positional arguments to this flag: the first argument is the "
        + "quantitative size, and the second argument is the scale. For "
        + "example, an argument of '4 M' corresponds to a size of 4 megabytes. "
        + f"Searching is only supported for byte ({BYTE}), kilobyte ({KILO}), "
        + f"megabyte ({MEGA}), and gigabyte ({GIGA}) scales.",
    )
    search_parser.add_argument(
        "-t",
        "--type",
        metavar="FILETYPE",
        help="Search for files by filetype. Must supply the filetype as a "
        + "positional argument to this flag.",
    )
    search_parser.set_defaults(handler=search)

    return parser


if __name__ == "__main__":
    parser = build_parser()
    args = parser.parse_args()
    args.handler(args)
