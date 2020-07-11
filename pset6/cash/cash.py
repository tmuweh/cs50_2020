from cs50 import get_float

# coins required
coins = 0

# get change owed
change = get_float("Change Owed: ")

# convert change to cent
cent = round(100 * change)

# calculate the number of coins required
while cent != 0:
    if cent >= 25:
        coins += 1
        cent -= 25
    elif cent >= 10:
        coins += 1
        cent -= 10
    elif cent >= 5:
        coins += 1
        cent -= 5
    else:
        coins += 1
        cent -= 1

# print coins required
print(coins)