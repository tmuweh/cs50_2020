# import modules
from sys import argv, exit
import cs50

#commandline argument
if len(argv) != 2:
    print("Usage: python roster.py <house>")
    exit(1)

# Get city
house = argv[1]

# connect db to student
db = cs50.SQL("sqlite:///students.db")

# get records
records = db.execute("SELECT * FROM students WHERE house = ?", house)

# print records
for row in records:
    if row["middle"] == "NULL":
        name = row["first"] + " " + row["last"]
    else:
        name = row["first"] + " " + row["middle"] + " " + row["last"]

    print(f"{name}, born {row['birth']}")
