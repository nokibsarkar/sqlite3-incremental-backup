"""
# Sqlite-incremental-Backup
This is an utility script that incrementally backup SQLite3 Database. This approach was proposed by a [StackOverflow User](https://stackoverflow.com/a/60559099/9748238) which I turned into code. Currently the script may be run in two language NodeJs and Python (*Coming soon*). I am willing to convert this as a module. Feel free to convert into any language and let me know.
# Background
SQLite3 is one of the most popular relational databases (and built-in Python) in this tech world. Many organizations use it at the production level because of its lightness, robustness, and portability. Using at the Production level also requires an efficient backup system in order to prevent data corruption, data loss, and whatnot. As SQLite3 is solely based on a single file, backing up requires the whole file to be copied on each backup (or, snapshot). It requires unnecessary space to save all the snapshots (for a slightly modified version). So, there is the solution, Incremental Backup System. In this system, the database is backed up only when the file content changes, therefore saving much space. I personally browsed over the internet to find any incremental backup system (even unofficial) but a Stackoverflow Thread. So, I wrote myself a lightweight utility/library/module to backup incrementally and save some space while processing a huge amount of database backup.
# Documentation
## NodeJs
Refer to [Nodejs Documentation](https://github.com/nokibsarkar/sqlite3-incremental-backup/tree/main/nodejs#readme)

"""

__version__ = "2.0.0" # major.minor.patch
_author__ = "Nazmul Haque Naqib <nokibsarkar@gmail.com>"
SQLITE_PAGE_SIZE_INDEX = 16
SQLITE_HEADER_LENGTH = 16
SQLITE_PAGE_COUNT_INDEX = 28
import os, datetime
from hashlib import sha256
def backup(db_file, current_snapshot_name : str = None, object_dir : str = 'objects/',):
    """
    This function is used to backup a SQLite database incrementally.
    :param db_file: The path to the source SQLite database.
    :param object_dir: The path to the directory where the all the pages should reside.
    :param block_size: The block size to use for the backup.
    :return: None
    """
    if current_snapshot_name == None:
        print("No Snapshot name provided, generating a new snapshot name.")
        current_snapshot_name = f"snapshopt-{datetime.datetime.utcnow()}.txt"
    page_size = 0
    # Open the database.
    with open(db_file, "rb") as db_file_object:
        assert db_file_object.read(SQLITE_HEADER_LENGTH) == b"SQLite format 3\x00"
        db_file_object.seek(SQLITE_PAGE_SIZE_INDEX, os.SEEK_SET)
        page_size = int.from_bytes(db_file_object.read(2), 'little') * 256
        db_file_object.seek(SQLITE_PAGE_COUNT_INDEX, os.SEEK_SET)
        page_count = int.from_bytes(db_file_object.read(4), 'big')
    pages = []
    with open(db_file, "rb") as db_file_object:
        for page_number in range(page_count):
            db_file_object.seek(page_number * page_size, os.SEEK_SET)
            page = db_file_object.read(page_size)
            hash = sha256(page).hexdigest()
            directory, filename = hash[:2], hash[2:]
            file_path = os.path.join(object_dir, directory, filename)
            if not os.path.exists(file_path): # 
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                with open(file_path, "wb") as file_object:
                    file_object.write(page)
            pages.append(hash)
    # Write the pages to the object directory.
    with open(current_snapshot_name, 'w') as fp:
        fp.write('\n'.join(pages))
"""
The restoration function is used to restore a SQLite database from a backup file.
"""
def restore(snapshot : str, target : str,  object_dir : str = 'objects'):
    """
    This function is used to restore a SQLite database from a backup file.
    :param db_file: The path to the target SQLite database.
    :param backup_file_name: The path to the backup file.
    :param object_dir: The path to the directory where the all the pages should reside.
    :return: None
    """
    # Read the pages from the backup file.
    with open(snapshot, 'r') as fp:
        pages = fp.read().split('\n')
    # Open the database.
    with open(target, "wb") as db_file_object:
        # Iterate thourgh the pages and write them to the database.
        for page in pages:
            path = os.path.join(object_dir, page[:2], page[2:])
            with open(path, "rb") as file_object:
                db_file_object.write(file_object.read())
    # Restoration is complete.
