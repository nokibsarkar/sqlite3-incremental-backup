import pathlib
from setuptools import setup

# The directory containing this file
ROOT = pathlib.Path(__file__).parent.parent.parent

# The text of the README file
README = """
# Sqlite-incremental-Backup
This is an utility script that incrementally backup SQLite3 Database. This approach was proposed by a [StackOverflow User](https://stackoverflow.com/a/60559099/9748238) which I turned into code. Currently the script may be run in two language NodeJs and Python (*Coming soon*). I am willing to convert this as a module. Feel free to convert into any language and let me know.
# Background
SQLite3 is one of the most popular relational databases (and built-in Python) in this tech world. Many organizations use it at the production level because of its lightness, robustness, and portability. Using at the Production level also requires an efficient backup system in order to prevent data corruption, data loss, and whatnot. As SQLite3 is solely based on a single file, backing up requires the whole file to be copied on each backup (or, snapshot). It requires unnecessary space to save all the snapshots (for a slightly modified version). So, there is the solution, Incremental Backup System. In this system, the database is backed up only when the file content changes, therefore saving much space. I personally browsed over the internet to find any incremental backup system (even unofficial) but a Stackoverflow Thread. So, I wrote myself a lightweight utility/library/module to backup incrementally and save some space while processing a huge amount of database backup.
# Documentation
## NodeJs
Refer to [Nodejs Documentation](https://github.com/nokibsarkar/sqlite3-incremental-backup/tree/main/nodejs#readme)

"""

# This call to setup() does all the work
setup(
    name="sqlite3-incremental-backup",
    version="2.1.5",
    description="Backup SQLite3 Database incrementally",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/nokibsarkar/sqlite3-incremental-backup",
    author="Nazmul Haque Naqib",
    author_email="nokibsarkar@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
    packages=["sqlite3backup"],
    include_package_data=True,
    install_requires = []
)
