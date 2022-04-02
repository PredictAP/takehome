# Take Home Project

Challenge: A directory contains multiple files and directories of non-uniform file and directory names. Create a program that traverses a base directory and creates an index file that can be used to quickly lookup files by name, size, and content type.

# Instructions

Fork this repository and implement the above requirements. The result must be an application that implements both the index and search features. Use your best judgement as to the interface that is used to use the index and search features, but remember that this is meant to create a dialog during the interview process, not be something that would be used in production.

Feel free to use the language, libraries, and tools that you are most comfortable in and best reflect your ability to translate requirements into a functional implementation.

Once the project is implemented, remove the `# Instructions` section of this readme and add the section `# Usage` with instructions on how to run the produced application.

The `test_data` directory in this project contains files and directories that can be used to test your implementation.

Good luck.

# Project Plan

There is some ambiguity in the requirements for this project, so I started by trying to understand what would make the Minimum Viable Product for this implementation. I settled on the following key points, with some noted caveats:

* The project will use a Command Line Interface. This allows me to develop the project rapidly without having to worry about the presentation of graphics. And since the intended audience for this project is other software developers, it felt appropriate. :)

* There is a caveat to using a CLI; as CLI applications generally operate on a command and/or set of options and then "quit", I understood that my program would have to read the created index file every time it was invoked. This is obviously not efficient, but for the purposes of an MVP it will suffice.

* If I wanted to make this more robust, I could make the CLI behave more like a "shell" program, i.e., once invoked it would sit at a prompt and allow you to enter multiple commands. This has the benefit of needing to read the created index file only once during startup, to store the directory tree in memory which should theoretically allow much faster search times.

* One last note on performance and memory; obviously the larger the created index file, the larger the memory footprint of the program would be. In that case, my CLI solution is poorly fitted for large scale indexing and search operations. If handling hundreds to thousands of files was a requirement, I would probably want to use something like a SQLite database to store the index information, and then perform queries to reduce RAM usage.

* I ended up choosing JSON as the format for the index file. JSON has an associative structure that allows me to retain some semantics for my search criteria. The file stores a flattened view of the directory tree, as a JSON array with one JSON object for each file, and each object contains semantic information such as filename, filesize, and filetype. The flat structure allows me to quickly iterate over the entire index when performing a search using a filter function. To support searching by multiple criteria simultaneously, I can chain multiple filters together.

* The project will be written in Python. This allows more time for development and requires less time for configuration. As a plus, I need no external dependencies; I just provide a script file that you can invoke with the Python interpreter on your machine.
