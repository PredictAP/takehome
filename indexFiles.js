const fs = require('fs');
const path = require('path');

// const indexFiles = async () => {
//     let indexDirectory = [];
//     await fs.readdir('./test_data', (err, files) => {
//         if(err) {
//             console.error('there was an error reading the files', err);
//             return {message: 'there was an error reading the files', error: err, status: 'failed'};
//         }

//         for (let i = 0; i < files.length; i++) {

//             const filePath = path.join('./test_data', files[i]);
//             fs.stat(filePath, (error, stat) => {
//                 if(stat.isFile()) {
//                     console.log(filePath, ' is a file');
//                     indexDirectory.push({
//                         fileName: files[i],
//                         filePath: filePath,
//                         fileSize: stat.size,
//                         contentType: path.extname(files[i])
//                     })
//                 }

//                 if(stat.isDirectory()) {
//                     console.log(filePath, ' is a directory');
//                 }
//             })
//         };
//     });
//     console.log('indexDirectory >>> ', indexDirectory);
//     return indexDirectory
// }

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