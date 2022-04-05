# Take Home Project

Challenge: A directory contains multiple files and directories of non-uniform file and directory names. Create a program that traverses a base directory and creates an index file that can be used to quickly lookup files by name, size, and content type.

# Usage
## Set Up
This challenge was developed utilizing Node.js and set up as an API.  Please follow these directions to set up your environment.
1. Clone the git project from the fork: https://github.com/ckendig/takehome onto your local machine.
2. Open your terminal (if on Mac/Linux) or Command Prompt (if on Windows).
3. This project requires node to be installed on your machine.  If you do not have node installed, please visit https://nodejs.org/en/ and install the LTS version of Node.
4. Navigate to the folder you have cloned the project to and run ``` npm install ``` in your terminal window.
5. Add the .env file to your root directory of the projct and add the following variables:
```
    DEFAULT_BASE_DIR=./test_data
    PORT=8080
```
6. In your terminal window on the root directory of the project run ``` npm run dev ```.  This will run the project with Nodemon to port 8080.  If Port 8080 is currently in use, update your .env file with a different port that is not in use.

## Using This Feature
Once you have the environment running locally, navigate to http://localhost:8080 in any web browser.  You can search for a file in 1 of 4 ways (I added one since I wanted to see it in the object): File Name, File Directory, File Size, and Content Type.  This is currently designed to just take 1 query parameter at a time right now for simplicity of the project, but this is how you will use it.

```
http://localhost:8080/search/?fileName=user
http://localhost:8080/search/?fileDirectory=data
http://localhost:8080/search/?fileSize=16
http://localhost:8080/search/?contentType=png

```

## Relevancy Score
There is a fairly arcaic relevancy score that I added to each result.  Here is how that breaks down:
```
3 - Highest Score. If search value is found at the START of the result value.
2 - If search value is found at the END of the result value.
1 - If search value is found ANYWHERE in the result value.

```
I then sort the relevance from highest to lowest before sending it back to the client.

