/**
 * A utility module to Backup SQLite3 Database incrementally which is not officially supported, but the approach was proposed by a stackoverflow user. (https://stackoverflow.com/a/60559099/9748238)
 * @name sqlite3-incremental-backup
 * @author Nokib Sarkar
 * @version 1.0.1S
 * @description
 * @example For Backing up a database named `mydb.sqlite` use the backup function as `backup('mydb.sqlite')`
 * For Restoration use the function `restore('<Snap shot name>', '<Target file>')`S
 */

import { readFileSync, open, mkdirSync, writeFileSync } from 'fs';
import { createHash } from 'crypto';

/**
 * The Function to backup the Sqlite3 Database incrementally. For simple use case, just call this function as `backup('<Your Database File>')`. Refer to Documentation for more.
 * @param {String} file The Input File name of the database which should be backed up. ***PLEASE USE AN UNIQUE FILENAME FOR EACH BACKUP***. Defaults to `snapshot.txt`.
 * @param {String} currentSnapshotName The name of the Current SnapShot name. This file contains the references to the actual pages
 * @param {String} objDir The Directory Where All the objects will be generated. The script must have right permission to that folder. For consistency, please use the same Directory where the previous call of the API generated. Otherwise it would not be useful at all. It defaults to `objects/`
 */
function backup(
    file,
    currentSnapshotName = 'snapshot.txt',
    objDir = 'objects/') {
    const content = readFileSync(file);
    const HEADER_LENGTH = 100;
    const header = Buffer.alloc(HEADER_LENGTH);
    content.copy(header, 0, 0, HEADER_LENGTH);
    const pageSize = header.readInt16LE(16) * 256;
    const pageCount = header.readInt32BE(28);

    let filenames = [];
    for (let i = 0; i < pageCount; i++) {
        const pageStartIndex = pageSize * i;
        const pageEndIndex = pageStartIndex + pageSize;
        const pageContent = content.subarray(pageStartIndex, pageEndIndex);
        const hash = createHash('sha256').update(pageContent).digest('hex');
        const fileDir = objDir + hash[0] + hash[1] //First Two Charecter
        const fileName = hash.substring(2) // The Rest of the Charecters
        const fileDest = `${fileDir}/${fileName}`;
        open(fileDest, 'w', function (err) {
            if (err && err.code == 'ENOENT') {
                //Directory not exists
                //Make the Directory
                mkdirSync(fileDir, { recursive: true });
            }
            writeFileSync(fileDest, pageContent);
        })
        filenames.push(fileDest)
    };
    // Now The `filenames` Contains location of the file which contain the Current State of specified page of the Database
    writeFileSync(currentSnapshotName, filenames.join('\n'));
};
/**
 * Th Function to restore the database from `snapshot`. Please ***DO NOT*** alter the foder structure which was used to backup specifically, do not modify the folder where all the object file resides. The database will be restored and saved into the filename given by the parameter `target`.
 * @param {String} snapshot The filename of the snapshot from which you want to restore the database. If resides in different database, please use the full path.
 * @param {String} target The name of the file where the database will be restored. If there is an existing database having the same name, the previous database will be destroyed and the database from current snapshot will overwrite the content. 
 */
function restore(snapshot = 'snapshot.txt', target = 'backup.db') {
    console.log('---> Restoration started from <--- ', snapshot)
    let sources = readFileSync(snapshot, { encoding: 'utf-8' }).split('\n');
    let chunks = [];
    sources.forEach(location => {
        let chunk = readFileSync(location);
        console.log('\t--->', location, chunk.length)
        chunks.push(chunk)
    });

    const buf = Buffer.concat(chunks)
    writeFileSync(target, buf);
    console.log('---> Restored Successfully to ---> ', target);
}
export const restore = restore;
export const backup = backup;
