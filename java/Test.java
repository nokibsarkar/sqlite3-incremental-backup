import nokib.SQLite3Incremental.SQLite3Incremental;
public class Test {
    public static void main(String[] args) {
        String dbFile = "test.sqlite3";
        String currentSnapshotName = "test";
        System.out.println("\t\tTesting with Java.......");
        try {
            SQLite3Incremental.backup(dbFile, currentSnapshotName);
            SQLite3Incremental.restore(currentSnapshotName, dbFile);
        } catch (Exception e) {
            e.printStackTrace();
        }
        System.out.println("\t\tTesting with Java Ends.......");
    }
}
