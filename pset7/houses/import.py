# import modules
from csv import DictReader
from sys import argv, exit
import cs50

# check for command line argument
if len(argv) != 2:
    print("Usage: python import.py file.csv")
    exit(1)

# create db students if not created otherwise open
open(f"students.db", "w").close()
db = cs50.SQL("sqlite:///students.db")

# creat tables in database for name(first middle and last), house and birth
db.execute("CREATE TABLE students (first TEXT, middle TEXT, last TEXT, house TEXT, birth NUMERIC)")

# open csv file for reading
with open("characters.csv", "r") as data:

    # create a DictReader
    reader = DictReader(data, delimiter=",")

    # iterate over csv file
    for row in reader:

        # split name column into a list of first middle and last name
        names = row["name"].split(" ")

        # check size of list
        first = names[0]
        if len(names) == 3:
            middle = names[1]
            last = names[2]
        else:
            middle = "NULL"
            last = names[1]

        # convert birth to int
        birth = int(row["birth"])

        # insert into student database
        db.execute("INSERT INTO students (first, middle, last, house, birth) VALUES(?, ?, ?, ?, ?)",
                                            first, middle, last, row["house"], birth)


