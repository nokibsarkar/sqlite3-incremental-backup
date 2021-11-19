"""
This module is written to implement the `backup` and `restore` of a SQLite database incrementally.
This library is written to be used with Python 3 or above. It may not be compatible with Python 2.
The library exposes two functions: `backup` and `restore` which are used to backup and restore a SQLite database.
"""
SQLITE_PAGE_SIZE_INDEX = 16
SQLITE_HEADER_LENGTH = 16
SQLITE_PAGE_COUNT_INDEX = 28
import os
from hashlib import sha256
def backup(db_file, object_dir = 'objects', backup_file_name='backup.txt'):
    """
    This function is used to backup a SQLite database incrementally.
    :param db_file: The path to the source SQLite database.
    :param object_dir: The path to the directory where the all the pages should reside.
    :param block_size: The block size to use for the backup.
    :return: None
    """

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
    with open(backup_file_name, 'w') as fp:
        fp.write('\n'.join(pages))
"""
The restoration function is used to restore a SQLite database from a backup file.
"""
def restore(db_file : str, backup_file_name : str, object_dir : str = 'objects'):
    """
    This function is used to restore a SQLite database from a backup file.
    :param db_file: The path to the target SQLite database.
    :param backup_file_name: The path to the backup file.
    :param object_dir: The path to the directory where the all the pages should reside.
    :return: None
    """
    # Read the pages from the backup file.
    with open(backup_file_name, 'r') as fp:
        pages = fp.read().split('\n')
    # Open the database.
    with open(db_file, "wb") as db_file_object:
        # Iterate thourgh the pages and write them to the database.
        for page in pages:
            path = os.path.join(object_dir, page[:2], page[2:])
            with open(path, "rb") as file_object:
                db_file_object.write(file_object.read())
    # Restoration is complete.
