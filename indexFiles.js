const fs = require('fs');
const path = require('path');

const indexFiles = (directoryPath, arrayOfFiles) => {

        const files = fs.readdirSync(directoryPath);

        arrayOfFiles = arrayOfFiles || [];

        files.forEach((file, fileIndex) => {
            if(fs.statSync(path.join(directoryPath, file)).isDirectory()) {
                arrayOfFiles = indexFiles(path.join(directoryPath, file), arrayOfFiles);
            } else {
                const fileInfo = {
                    fileName: file,
                    filePath: path.join(directoryPath, file),
                    fileSize: fs.statSync(path.join(directoryPath, file)).size,
                    contentType: path.extname(file)
                }
                arrayOfFiles.push(fileInfo);
            }
        });

    return arrayOfFiles;
}

module.exports = indexFiles;