# Take Home Project

Challenge: A directory contains multiple files and directories of non-uniform file and directory names. Create a program that traverses a base directory and creates an index file that can be used to quickly lookup files by name, size, and content type.

# usage

We can save the  provided Bash script in a file with a ".sh" extension, such as "indexer.sh". We will use a text editor to create the file and paste the script into it.

We open a terminal or command prompt.

We navigate to the directory where we have  saved the "indexer.sh" file using the cd command. For example, if the file is saved in the "Documents" directory, we can navigate there using the command:
cd Documents

We make the script executable by running the following command:
chmod +x indexer.sh

We run the script using the following command:
./indexer.sh

The script will traverse the "test-data" directory (assuming it's in the same directory as the script) and create the index file named "index.json". It will display the file name, size, and content type for the file specified in the file_name variable. We can modify the file_name variable in the script to perform lookups for different files. For example, to lookup "user2.json", we can change the line file_name="user1.json" to file_name="user2.json".

The script will output the results of the lookup, or an error message if the file is not found in the index.
