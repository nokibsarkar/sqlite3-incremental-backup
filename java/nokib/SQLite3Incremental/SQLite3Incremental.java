package nokib.SQLite3Incremental;
import java.io.File;
import java.util.Scanner;
public class SQLite3Incremental {
    /*
     * This method takes the database file name, the backup file name and the number of rows to be backed up
     */
    public static void backup(String dbFile, String currentSnapshotName){
        backup(dbFile, currentSnapshotName, "objects/");
    }
    public static void backup(String dbFile, String currentSnapshotName, String object_dir){
        System.out.println("Backing up...");
    }
    public static void restore(String snapshot, String target){
        restore(snapshot, target, "objects/");
    }
    public static void restore(String snapshot, String target, String object_dir){
        System.out.println("Restoring...");
    }
}