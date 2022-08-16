"""
This file would generate a random SQLite3 database and then backup it.
"""
import random, sqlite3, sys
def generate_database(target_file):
    print("Generating the test sqlite3 database : " + target_file)
    with sqlite3.connect(target_file) as db:
        db.execute("DROP TABLE IF EXISTS test")
        db.execute("CREATE TABLE test (id INTEGER PRIMARY KEY, value TEXT)")
        db.executemany(
            "INSERT INTO test (value) VALUES (?)",
            [
                (str(random.randint(0, 100)),) for i in range(100000)
            ]
        )
if __name__ == '__main__':
    generate_database("python/test.sqlite3")
    generate_database("nodejs/test.sqlite3")
    generate_database("c/test.sqlite3")

    


