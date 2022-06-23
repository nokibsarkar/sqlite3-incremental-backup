import { backup, restore } from "./sqlite3-incremental-backup.mjs";
import fs from "fs";
console.log("Testing with Nodejs")
const SOURCE_DATABASE_NAME = process.argv[2]
const BACKUP_FILE_NAME = process.argv[3]
const SNAPSHOT_NAME = process.argv[4]
const OBJECT_DIRECTORY = process.argv[5]
console.log("\tBacking up the database")
backup(SOURCE_DATABASE_NAME, SNAPSHOT_NAME, OBJECT_DIRECTORY, (...args) => {
    console.log("\tBacked up Successfully")
    console.log("\tRestoring the database")
    restore(SNAPSHOT_NAME, BACKUP_FILE_NAME, OBJECT_DIRECTORY, (...args) => {
        console.log("\tRestored Successfully")
        console.log("\tComparing the two files")
        const source = fs.readFileSync(SOURCE_DATABASE_NAME, "utf8")
        const backup = fs.readFileSync(BACKUP_FILE_NAME, "utf8")
        if (source === backup) {
            console.log("\tFiles are same")

        } else {
            console.log("\tFiles are different")
            throw new Error("Files are different")
        }
        console.log("Removing the test files")
        fs.unlinkSync(SOURCE_DATABASE_NAME)
        fs.unlinkSync(BACKUP_FILE_NAME)
        fs.unlinkSync(SNAPSHOT_NAME)
        fs.rmSync(OBJECT_DIRECTORY, { recursive: true })
        console.log("Test Successful")
    })
})
