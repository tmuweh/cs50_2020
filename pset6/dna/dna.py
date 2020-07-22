# import command line module
from sys import argv, exit

# import csv file module
from csv import reader, DictReader

# import other helper module
from cs50 import get_string

# check for commandline arguments
if len(argv) != 3:
    print("Usage: python dna.py databases.csv sequences.txt")
    exit(1)

# open database and save content to memory
database = open(argv[1], "r")

# open sequence file and save to memory
sequence = open(argv[2], "r")

# get number of STRs from database
strs = next(reader(database, dialect="excel"))

# remove the name member on list
strs.pop(0)

# get dna sequence from object.
dna = next(sequence)

# dictionary to hold strs occurences
dict = {}
keys = strs
values = 0

#initialize the array
for i in keys:
        dict[i] = 0
# for each STRs in database search sequence for the longest occurence
for str in strs:

    j = len(str)

    # count occurences
    counter = 0
    for i in range(len(dna)):

        # value to keep i unchanged
        k = i

        while dna[k:(k+j)] == str:
            counter += 1

            # shifting an str length(j) along sequence
            k += j

        if dict[str] < counter:
            dict[str] = counter
        counter = 0
print(dict)



    # keep track of the repeats

# compare repeats with STRs in the data base and print name of owner or not found

# close opened files
database.close()
sequence.close()