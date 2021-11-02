# sqlite3-incremental-backup
This Module can be used to incrementally backup your database which will reduce the needed Backup size.
# Installation
For Installation Please Use `npm` command as follows:
```npm install sqlite3-incremental-backup```
# Example
For Simple use case, use as follows :
```
import {backup, restore} from './sqlite3-incremental-backup';
const srcFile = 'source.db';
const targetFile = 'target.db';
const snapshotName = 'snapshot1.txt'; //Can be any arbitrary name. MUST BE UNIQUE FOR EACH SNAPSHOT OTHERWISE THE PREVIOUS WILL BE LOST
backup(srcFile, snapshotName); // For Backup
restore(snapshotName, targetFile); // For Restoration
```
*Note : Both `backup` and `restore` functions are asynchronous. For using Synchronously, Please use `await` keyword.*
