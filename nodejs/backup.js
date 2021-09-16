const fs = require('fs');
const content = fs.readFileSync('database.db');
const HEADER_LENGTH = 100;
const header = Buffer.alloc(HEADER_LENGTH);
content.copy(header, 0, 0, HEADER_LENGTH);
const pageSize = header.readInt16LE(16) * 256;
const pageCounter = header.readInt32BE(28);
function backup(content, pageSize, pageCount, currentSnapshotName = 'snapshot3.txt', pageDir = 'objects/'){
    console.log('Page Size : ', pageSize)
    console.log('Page Count', pageCount)
    let crypto = require('crypto');
    let filenames = [];
    for(let i = 0; i < pageCount; i++){
        const pageStartIndex = pageSize * i;
        const pageEndIndex = pageStartIndex + pageSize;
        const pageContent = content.subarray(pageStartIndex, pageEndIndex);
        const hash = crypto.createHash('sha256').update(pageContent).digest('hex');
        const fileDir = pageDir + hash[0] + hash[1] //First Two Charecter
        const fileName = hash.substring(2) // The Rest of the Charecters
        const fileDest = `${fileDir}/${fileName}`;
        fs.open(fileDest, 'w', function(err){
            if(err && err.code == 'ENOENT'){
                //Directory not exists
                //Make the Directory
                fs.mkdirSync(fileDir, {recursive : true});
            }
            fs.writeFileSync(fileDest, pageContent);
        })
        filenames.push(fileDest)
    };
    // Now The `filenames` Contains location of the file which contain the Current State of specified page of the Database
    fs.writeFileSync(currentSnapshotName, filenames.join('\n'));
}
function restore(snapshot='snapshot.txt', target='backup.db'){
    console.log('---> Restoration started from <--- ', snapshot)
    let sources = fs.readFileSync(snapshot, {encoding:'utf-8'}).split('\n');
    let chunks = [];
    sources.forEach(location =>{
        let chunk = fs.readFileSync(location);
        console.log('\t--->', location, chunk.length)
        chunks.push(chunk)
    });

    const buf = Buffer.concat(chunks)
    fs.writeFileSync(target, buf);
    console.log('---> Restored Successfully to ---> ', target);
}
module.exports = {restore : restore, backup : backup}
