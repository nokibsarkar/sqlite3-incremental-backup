/**
 * A utility module to Backup SQLite3 Database incrementally which is not officially supported, but the approach was proposed by a stackoverflow user. (https://stackoverflow.com/a/60559099/9748238)
 * @name sqlite3-incremental-backup
 * @author Nokib Sarkar
 * @version 1.0.1S
 * @description
 * @example For Backing up a database named `mydb.sqlite` use the backup function as `backup('mydb.sqlite')`
 * For Restoration use the function `restore('<Snap shot name>', '<Target file>')`S
 */

import { readFileSync, mkdirSync, writeFileSync, createReadStream, createWriteStream, existsSync } from 'fs';
import { createHash } from 'crypto';

/**
 * The Function to backup the Sqlite3 Database incrementally. For simple use case, just call this function as `backup('<Your Database File>')`. Refer to Documentation for more.
 * @param {String} file The Input File name of the database which should be backed up. ***PLEASE USE AN UNIQUE FILENAME FOR EACH BACKUP***. Defaults to `snapshot.txt`.
 * @param {String} currentSnapshotName The name of the Current SnapShot name. This file contains the references to the actual pages
 * @param {String} objDir The Directory Where All the objects will be generated. The script must have right permission to that folder. For consistency, please use the same Directory where the previous call of the API generated. Otherwise it would not be useful at all. It defaults to `objects/`
 * @param {CallableFunction} callback A callback function which will be called after the successful backup. All the arguments after this parameter will be passed to `callback` function
*/
async function backup(
    file,
    currentSnapshotName = null,
    objDir = 'objects/',
    callback = null,
    ...args
) {
    const HEADER_LENGTH = 100;
    if(!currentSnapshotName)
        currentSnapshotName = `snapshot-${Date.now()}.txt`;
    // Read only the first 100 bytes of the file using readStream
    const readStream = createReadStream(file, { start: 0, end: HEADER_LENGTH });
    readStream.on('data', (header) => {
        // The whole body here
        const pageSize = header.readInt16LE(16) * 256;
        const pageCount = header.readInt32BE(28);
        const dbFile = createReadStream(file, { highWaterMark: pageSize });
        let filenames = [];
        dbFile.on(
            'data',
            (pageContent) => {
                const hash = createHash('sha256').update(pageContent).digest('hex');
                const fileDir = objDir + hash[0] + hash[1] //First Two Charecter
                const fileName = hash.substring(2) // The Rest of the Charecters
                const fileDest = `${fileDir}/${fileName}`;
                if (!existsSync(fileDir)) {
                    mkdirSync(fileDir, { recursive: true });
                }
                writeFileSync(fileDest, pageContent);
                filenames.push(fileDest)
            }
        )
        dbFile.on('end', () => {
            console.log('--->', file, 'Backed up Successfully to ---> ', currentSnapshotName)
            // Now The `filenames` Contains location of the file which contain the Current State of specified page of the Database
            writeFileSync(currentSnapshotName, filenames.join('\n'));
            callback && callback(...args)
        })
    });
};
/**
 * This Function to restore the database from `snapshot`. Please ***DO NOT*** alter the foder structure which was used to backup specifically, do not modify the folder where all the object file resides. The database will be restored and saved into the filename given by the parameter `target`.
 * @param {String} snapshot The filename of the snapshot from which you want to restore the database. If resides in different database, please use the full path.
 * @param {String} target The name of the file where the database will be restored. If there is an existing database having the same name, the previous database will be destroyed and the database from current snapshot will overwrite the content. 
 * @param {CallableFunction} callback A callback function which will be called after the successful restoration. All the arguments after this parameter will be passed to `callback` function
 */
async function restore(snapshot = 'snapshot.txt', target = 'backup.db', callback = null, ...args) {
    console.log('---> Restoration started from <--- ', snapshot)
    let sources = readFileSync(snapshot, { encoding: 'utf-8' }).split('\n');
    const writer = createWriteStream(target, {autoClose: true});
    writer.on(
        'ready',
        () => {
            // The Writable is ready to write
            sources.forEach(
                (source) => {
                    if (!source) return;
                    let chunk = readFileSync(source);
                    console.log('\t--->', source, chunk.length)
                    writer.write(chunk);
                });
            writer.end();
        }
    )
    writer.on(
        'close',
        () => {
            console.log('---> Restored Successfully to ---> ', target);
            callback && callback(...args)
    })
}

export { backup, restore }