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

# initialize the array
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

        # find number of consecutive repeats from current str
        while dna[k:(k+j)] == str:

            # keep track of consecutive repeats
            counter += 1

            # shifting an str length(j) along sequence
            k += j

        # update most consecutive occurence
        if dict[str] < counter:
            dict[str] = counter

        # reset counter
        counter = 0

# read into list
bank = reader(database, dialect='excel')

#convert dictionary to list
occurence_list = list(dict.values())

# to hold int value of database str count
dicts =  []

# compare repeats with STRs in the data base and print name of owner or not found

match = False
for line in bank:
    name = line.pop(0)

    # convert string lis to int
    for number in line:
        dicts.append(int(number))

    # compare two int list of str counts for each person on the database
    if dicts == occurence_list:
        print(name)
        match = True

    # empty list after each comparison
    dicts = []



# close opened files
database.close()
sequence.close()

# Not found
if match != True:
    print("No Match")
exit(0)