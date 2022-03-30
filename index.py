import os
import json
import argparse


files = []

def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("folder", type=str)
    arg_parser.add_argument("outfile", type=str)
    args = arg_parser.parse_args()

    scan_dir(args.folder)
    with open(args.outfile, "w") as outfile:
        outfile.write(json.dumps(files))


def scan_dir(path):
    for dir_entry in os.scandir(path):
        if dir_entry.is_dir():
            scan_dir(dir_entry.path)
        else:
            filename = os.path.splitext(dir_entry.name)
            files.append({"name": filename[0], "ext": filename[1][1:], "filesize": dir_entry.stat().st_size})


if __name__ == "__main__":
    main()