# Take Home Project

Challenge: A directory contains multiple files and directories of non-uniform file and directory names. Create a program that traverses a base directory and creates an index file that can be used to quickly lookup files by name, size, and content type.

# Usage

This program requires Python version 3.7. Run the program by invoking it with the `python` interpreter:

```bash
python parsely.py
```

Some machines may still have `python` symlinked to Python 2, so in that case, you should use `python3`.

There are two commands:

`index`: given a path, builds an index of files and their information by recursively traversing down the directory tree from the given path. If no path is given, the current working directory is used by default.

`search`: allows searching based on any combination of filename, filesize, and filetype. The search function is denoted by options, noted below. Options can be supplied as shorthand or the longform version.

`-n`, `--name`: search by filename. Provide a positional argument after this flag for the search query. Supports searching with partial filenames.

`-s`, `--size`: search by filesize. Provide two positional arguments after this flag for the search query; the first indicates the quantitative size of the file being searched, and second indicates the scale of the size. For example, using the flag like so `-s 4 M` can be used to search for files that are approximately 4 megabytes large. I say approximately because the filesize search will look for files that are within the 90-110% size of the requested file size.

The following scales are supported by filesize search:

| Scale    | Identifier |
| -------- | ---------- |
| Byte     | B          |
| Kilobyte | K          |
| Megabyte | M          |
| Gigabyte | G          |

`-t`, `--type`: search by filetype. Provide a positional argument after this flag for the search query. You _MUST_ provide a valid file extension. For example, `-t .jpg` will work, but `-t jpg` will not.

It is possible to combine these flags to specify your search. For example:

```bash
python parsely.py search -n fahim -s 2 K -t .txt
```

Will look for files that have the string `fahim` somewhere in their filename, are approximately 2 kilobytes large, and end with the `.txt` file extension.

For convenience, the help output for the program and the sub commands are provided below.

```bash
usage: parsely.py [-h] {index,search} ...

Index a directory tree and search for the files within.

positional arguments:
  {index,search}
    index         Index a directory tree.
    search        Perform a search query.

options:
  -h, --help      show this help message and exit
```

```bash
usage: parsely.py index [-h] [DIRECTORY]

positional arguments:
  DIRECTORY   Index the given directory. If no path is supplied, will index
              the current working directory.

options:
  -h, --help  show this help message and exit
```

```bash
usage: parsely.py search [-h] [-n FILENAME] [-s FILESIZE SCALE] [-t FILETYPE]

options:
  -h, --help            show this help message and exit
  -n FILENAME, --name FILENAME
                        Search for files by filename. Must supply part or all
                        of a filename as a positional argument to this flag.
  -s FILESIZE SCALE, --size FILESIZE SCALE
                        Search for files by filesize. Must supply the filesize
                        as two positional arguments to this flag: the first
                        argument is the quantitative size, and the second
                        argument is the scale. For example, an argument of '4
                        M' corresponds to a size of 4 megabytes. Searching is
                        only supported for byte (B), kilobyte (K), megabyte
                        (M), and gigabyte (G) scales.
  -t FILETYPE, --type FILETYPE
                        Search for files by filetype. Must supply the filetype
                        as a positional argument to this flag.
```

# Project Plan

There is some ambiguity in the requirements for this project, so I started by trying to understand what would make the Minimum Viable Product for this implementation. I settled on the following key points, with some noted caveats:

- The project will use a Command Line Interface. This allows me to develop the project rapidly without having to worry about the presentation of graphics. And since the intended audience for this project is other software developers, it felt appropriate. :)

- There is a caveat to using a CLI; as CLI applications generally operate on a command and/or set of options and then "quit", I understood that my program would have to read the created index file every time it was invoked. This is obviously not efficient, but for the purposes of an MVP it will suffice.

- If I wanted to make this more robust, I could make the CLI behave more like a "shell" program, i.e., once invoked it would sit at a prompt and allow you to enter multiple commands. This has the benefit of needing to read the created index file only once during startup, to store the directory tree in memory which should theoretically allow much faster search times.

- One last note on performance and memory; obviously the larger the created index file, the larger the memory footprint of the program would be. In that case, my CLI solution is poorly fitted for large scale indexing and search operations. If handling hundreds to thousands of files was a requirement, I would probably want to use something like a SQLite database to store the index information, and then perform queries to reduce RAM usage.

- I ended up choosing JSON as the format for the index file. JSON has an associative structure that allows me to retain some semantics for my search criteria. The file stores a flattened view of the directory tree, as a JSON array with one JSON object for each file, and each object contains semantic information such as filename, filesize, and filetype. The flat structure allows me to quickly iterate over the entire index when performing a search using a filter function. To support searching by multiple criteria simultaneously, I can chain multiple filters together.

- The project will be written in Python. This allows more time for development and requires less time for configuration. As a plus, I need no external dependencies; I just provide a script file that you can invoke with the Python interpreter on your machine.
