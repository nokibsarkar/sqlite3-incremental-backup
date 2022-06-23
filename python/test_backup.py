"""
This file would generate a random SQLite3 database and then backup it.
"""
import sqlite3backup, os, sys

if __name__ == '__main__':
    if len(sys.argv) < 5:
        print("Usage: python3 test_backup.py <source_database_name> <backup_file_name> <snapshot_name> <object_directory>")
        sys.exit(1)
    SOURCE_DATABASE_NAME = sys.argv[1]
    BACKUP_FILE_NAME = sys.argv[2]
    SNAPSHOT_NAME = sys.argv[3]
    OBJECT_DIRECTORY = sys.argv[4]
    print("Testing with python3")
    print(f"\tBacking up from `{SOURCE_DATABASE_NAME} -> {BACKUP_FILE_NAME}`")
    sqlite3backup.backup(SOURCE_DATABASE_NAME, SNAPSHOT_NAME, OBJECT_DIRECTORY)
    print(f"\tRestoring from the snapshot `{SNAPSHOT_NAME} -> {BACKUP_FILE_NAME}`")
    sqlite3backup.restore(SNAPSHOT_NAME, BACKUP_FILE_NAME, OBJECT_DIRECTORY)
    # Now compare the two files.
    with open(SOURCE_DATABASE_NAME, "rb") as source_file, open(BACKUP_FILE_NAME, "rb") as backup_file:
        assert source_file.read() == backup_file.read(), "\tThe source and the backup version are not same."
    print("\tSuccessfully restored the database.")
    print("Removing all the test files.")
    os.remove(SOURCE_DATABASE_NAME)
    os.remove(BACKUP_FILE_NAME)
    os.remove(SNAPSHOT_NAME)
    # Remove the object directory even if it's not empty
    os.system("rm -rf " + OBJECT_DIRECTORY)
    print("\tSuccessfully removed all the test files.")


