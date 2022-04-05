const express = require('express');
require('dotenv').config();
const app = express();
const indexFiles = require('./indexFiles');


app.get('/test', (req, res) => {
    res.send('Server is working properly');
});

app.get('/search', async (req, res) => {
    const results = await indexFiles(process.env.DEFAULT_BASE_DIR);

    const searchChecks = {
        fileName: decodeURI(req.query.fileName) || false,
        fileSize: decodeURI(req.query.fileSize) || false,
        filePath: decodeURI(req.query.filePath) || false,
        contentType: decodeURI(req.query.contentType) || false
    };

    const finalResults = [];
    results.forEach(result => {
        Object.keys(searchChecks).forEach(key => {
            if (searchChecks[key] !== 'undefined' && searchChecks[key] !== undefined) {
                // Check begins with...
                if(new RegExp(`^${searchChecks[key]}`, 'i').test(result[key])) {
                    if(finalResults.filter(x => x[key] === result[key]).length === 0) {
                        finalResults.push({
                            ...result,
                            relevance: 3
                        })
                    }
                } 
                // Check ends with...
                else if (new RegExp(`${searchChecks[key]}$`, 'i').test(result[key])) {
                    if(finalResults.filter(x => x[key] === result[key]).length === 0) {
                        finalResults.push({
                            ...result,
                            relevance: 2
                        })
                    }
                } 
                // Check includes...
                else if (new RegExp(`${searchChecks[key]}`, 'ig').test(result[key])) {
                    if(finalResults.filter(x => x[key] === result[key]).length === 0) {
                        finalResults.push({
                            ...result,
                            relevance: 1
                        })
                    }
                }
            }
        })
    })
    res.send(finalResults.sort((a,b) => b.relevance - a.relevance));
})





// Start the API with Express

const port = process.env.PORT || 8080;
app.listen(port, () => console.log(`API available on http://localhost:${port}`));