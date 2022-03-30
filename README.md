# Take Home Project

Challenge: A directory contains multiple files and directories of non-uniform file and directory names. Create a program that traverses a base directory and creates an index file that can be used to quickly lookup files by name, size, and content type.

# Usage

1. Optionally, create a new virtual environment:
```
python3 -m venv .venv
source .venv/bin/activate
```
2. Install pandas:
```
pip install pandas
```
3. Create index file:
```
python index.py <source folder> <destination file>
Example:
python index.py test_data file_list.json
```

### How to Search
```
python search.py [optional arguments] <index file>
```

Optional arguments:
- `-n <name>` Searches for file records with a name containing *name*
- `-e <extension>` Searches for file records by extension
- `-l <size>` Searches for files smaller than *size*
- `-g <size>` Searches for files larger than *size*

Examples:
```
python search.py -n sample file_list.json
python search.py -e jpg -g 10000 file_list.json
python search.py -n user file_list.json
```