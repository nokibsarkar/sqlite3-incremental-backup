import pathlib
from setuptools import setup

# The directory containing this file
ROOT = pathlib.Path(__file__).parent.parent.parent

# The text of the README file
README = (ROOT/ "README.md").read_text()

# This call to setup() does all the work
setup(
    name="sqlite3-incremental-backup",
    version="1.0.0",
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
