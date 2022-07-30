export SOURCE_DATABASE_NAME=test.sqlite3
export BACKUP_FILE_NAME=test.sqlite3.backup
export SNAPSHOT_NAME=test.snapshot
export OBJECT_DIRECTORY=objects
python3 generate_database.py $SOURCE_DATABASE_NAME
cd python && python3 test_backup.py $SOURCE_DATABASE_NAME $BACKUP_FILE_NAME $SNAPSHOT_NAME $OBJECT_DIRECTORY
cd ../nodejs && node test.mjs $SOURCE_DATABASE_NAME $BACKUP_FILE_NAME $SNAPSHOT_NAME $OBJECT_DIRECTORY
cd ../c && gcc main.c -o main && ./main
