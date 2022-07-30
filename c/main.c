#ifndef DEBUG
#define DEBUG
#endif
#include "sqlite3incremental.h"

int main(){
    printf("\tTesting with C\n");
    char dbfile[] = "test.sqlite3";
    char snapshot[] = "test.snapshot";
    char objectDir[] = "obj/";
    int subdir_mode = 0777;
    sqlite3_incremental_backup(
        dbfile,
        snapshot,
        objectDir,
        subdir_mode
    );
    sqlite3_incremental_restore(
        snapshot,
        "test-restored.sqlite3.d",
        objectDir
    );
    printf("\tTest Successfully ended with C\n");
}