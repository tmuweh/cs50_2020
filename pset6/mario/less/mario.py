# program to print half pyramid of specified height  by tmuweh
from cs50 import get_int

# Max height
MAX_HEIGHT = 8

# So we get a range from 1 to MAX_HEIGHT
MAX_HEIGHT += 1

# reprompt user to enter height is height is valid
while True:
    height = get_int("Height: ")
    if height in range(1, MAX_HEIGHT):
        break

# draw pyramid of specified height
for i in range(height):
    for j in range(height):
        if i + j < height - 1:
            print(" ", end="")
        else:
            print("#", end="")
    print()
# print newline




