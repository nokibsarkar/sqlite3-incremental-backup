#ifndef SQLITE3_INCREMENTAL_BACKUP
#define SQLITE3_INCREMENTAL_BACKUP
#define SQLITE_PAGE_SIZE_INDEX 16
#define SQLITE_HEAD_LENGTH  16
#define SQLITE_PAGE_COUNT_INDEX  28
#define SQLITE_HEADER_LENGTH  100
#define BE_TO_LE_4(num) ((num >> 24) & 0xff) | ((num << 8) & 0xff0000) | (( num >> 8) & 0xff00) | ((num << 24) & 0xff000000); 
#define BE_TO_LE_2(num) num << 8
#include <stdio.h>
#include <string.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <errno.h>
#include <stdlib.h>
enum SQLITE3_I_ERROR {
    SQLITE_I_OK = 0,
    SQLITE_I_DB_NOT_OPEN,
    SQLITE_I_DB_NOT_SQLIE,
    SQLITE_I_OB_NOT_OPEN,
    SQLITE_I_SN_NOT_OPEN
};
/**
 * @brief The function to be called to obtain the incremental backup
 * 
 */
// int sqlite3_incremental_backup(
//     char * dbFile, // the database file to backup
//     char * currentSnapshotName, // the name of the current snapshot
//     char * objectDir // the directory to store the objects
// );

// Check if the path exists
int _check_exist(char * path){
    struct stat st;
    return stat(path, &st) == 0;
}
void _create_if_not_exists(char * path, int mode){
    if (_check_exist(path) == 0) {
        mkdir(path, mode);
    }
};
/**
 * @brief The function for perform the incremental backup of the SQLite3 database
 * 
 * @param dbFile The SQLite3 filename to backup
 * @param currentSnapshotName A file where the metadata of this snapshot would be preserved
 * @param objectDir The folder where all the objects would reside
 * @param subdir_mode The permission of the subdirectories if needed to be created
 * @return An error code if any, otherwise SQLITE_I_OK
 */
int sqlite3_incremental_backup(char * dbFile, char * currentSnapshotName, char * objectDir, int subdir_mode){
    _create_if_not_exists(objectDir, subdir_mode);
    #ifdef DEBUG
    printf("Opening Database File: %s\n", dbFile);
    #endif
    FILE * dbFileObject = fopen(dbFile, "rb");
    if(dbFileObject == NULL){
        #ifdef DEBUG
        printf("Error opening database file\n");
        #endif
        return SQLITE_I_DB_NOT_OPEN;
    }
    char * header = (char *) malloc(SQLITE_HEAD_LENGTH * sizeof(char));
    fread(header, sizeof(char), SQLITE_HEAD_LENGTH, dbFileObject);
    if(strcmp(header, "SQLite format 3")){
        #ifdef DEBUG
        printf("Error: database file is not SQLite\n");
        #endif
        free(header);
        return SQLITE_I_DB_NOT_SQLIE;
    }
    free(header);
    #ifdef DEBUG
    printf("Database file is SQLite\n");
    printf("Header : %s\n", header);
    #endif
    int page_size = 0;
    int page_count = 0;
    // get the page size as two byte lower endian integer
    fseek(dbFileObject, SQLITE_PAGE_SIZE_INDEX, SEEK_SET);
    fread(&page_size, 2, 1, dbFileObject);
    page_size = BE_TO_LE_2(page_size);
    // get the page count as 4 byte lower endian integer
    fseek(dbFileObject, SQLITE_PAGE_COUNT_INDEX, SEEK_SET);
    fread(&page_count, 4, 1, dbFileObject);
    page_count = BE_TO_LE_4(page_count); // Convert big endian to little endian with 4 byte
    #ifdef DEBUG
    printf("Page Size: %d\n", page_size);
    printf("Page Count: %d\n", page_count);
    #endif
    // reset the file pointer to the beginning of the file
    fseek(dbFileObject, 0, SEEK_SET );
    int obj_dir_len = strlen(objectDir); // length of the object directory
    int hash_size = 64; // hash output length of 
    char objects[page_count][hash_size + 2]; // for additional two slashes
    char * content = (char *) malloc(page_size);
    char subdirectory[obj_dir_len + 3];
    for(int i = 0; i < page_count; i++){
        // each page
        fread(content, 1, page_size, dbFileObject);
        // get the hash of the page
        char hash[] = "b0406a68fc99c7db9553d7be36ce9e528684b82f76a0d8109b86b0e24c6c6240"; //(char *) malloc(hash_size * sizeof(char));
        hash[3] = 'a' + i;
        sprintf(objects[i], "%c%c/%s", hash[0], hash[1], &hash[2]);
        // the subdirectory where the content would reside
        sprintf(subdirectory, "%s%c%c/", objectDir, hash[0], hash[1]);
        // create the subdirectory if it does not exist
        _create_if_not_exists(subdirectory, subdir_mode);
        char file_name[obj_dir_len + hash_size + 3];
        sprintf(file_name, "%s%s", subdirectory, &hash[2]);
        #ifdef DEBUG
        printf("Hash : %s\n", hash);
        printf("Subdirectory : %s\n", subdirectory);
        printf("File Name : %s\n", file_name);
        printf("------> %s\n", objects[i]);
        #endif
        if(_check_exist(file_name)){
            #ifdef DEBUG
            printf("Object already exists\n");
            #endif
            continue;
        }
        FILE * objectFile = fopen(file_name, "wb");
        if(objectFile == NULL){
            #ifdef DEBUG
            printf("Error opening object file\n");
            #endif
            return SQLITE_I_OB_NOT_OPEN;
        }
        fwrite(content, 1, page_size, objectFile);
        fclose(objectFile);
    }
    free(content);
    fclose(dbFileObject);
    // Now save to snapshot
    FILE * snapshotFile = fopen(currentSnapshotName, "w");
    if(snapshotFile == NULL){
        #ifdef DEBUG
        printf("Error opening snapshot file\n");
        #endif
        return SQLITE_I_OB_NOT_OPEN;
    }
    for(int i = 0; i < page_count; i++){
        fprintf(snapshotFile, "%s%s", i ? "\n" : "", objects[i]);
    }
    fclose(snapshotFile);
    return SQLITE_I_OK;
}
/**
 * @brief The function to restore the SQLite3 database from the incremental backup using the metadata of the snapshot
 * 
 * @param snapshot The snapshot file to restore from
 * @param target The target file name where the database would be restored to
 * @param objectDir The object directory where the objects would reside
 * @return An error code if any, otherwise SQLITE_I_OK
 */
int sqlite3_incremental_restore(char * snapshot, char * target, char * objectDir){
    #ifdef DEBUG
    printf("Restoring the database from\n\tThe snapshot : %s\n", snapshot);
    printf("\tThe target : %s\n", target);
    printf("\tThe object directory : %s\n", objectDir);
    #endif
    FILE * snapshotFile = fopen(snapshot, "r");
    if(snapshotFile == NULL){
        #ifdef DEBUG
        printf("Error opening snapshot file : %s\n", strerror(errno));
        #endif
        return SQLITE_I_SN_NOT_OPEN;
    }
    FILE * targetFile = fopen(target, "wb");
    int obj_dir_len = strlen(objectDir); // length of the object directory
    int hash_size = 64;
    char object_name[hash_size + 2], object_path[obj_dir_len + hash_size];
    while(1){
        fgets(object_name, hash_size + 2, snapshotFile);
        if(!feof(snapshotFile))
            fseek(snapshotFile, 1, SEEK_CUR);
        else
            break;
        
        printf("Fetching Object : %s\n", object_name);
        sprintf(object_path, "%s%s", objectDir, object_name);
        //printf("Object Path : %s\n", object_path);
        FILE * objectFile = fopen(object_path, "rb");
        if(objectFile == NULL){
            #ifdef DEBUG
            printf("Error opening object file : %s\n", strerror(errno));
            #endif
            return SQLITE_I_SN_NOT_OPEN;
        }
        char c[4096];
        while(!feof(objectFile)){
            fgets(c, 4096, objectFile);
            fprintf(targetFile, "%s", c);
        }
        fclose(objectFile);
    }
    fclose(targetFile);
    fclose(snapshotFile);
}
#endif