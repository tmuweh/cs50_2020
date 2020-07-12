# give readability level of a text
import string

# get text from user
text = input("Text: ")

# get len of text
text_size = len(text)

# where to store counts
sentences = 0
words = 0
letters = 0

# check for char after word or sentence
was_blank_punct = False

for i in range(text_size):
    if text[i].isalnum():
        letters += 1

        # count first word in text
        if words == 0:
           words += 1

    # count all punctuation as new sentences
    if text[i] == "." or text[i] == "?" or text[i] == "!":
        sentences += 1

    # set new value for blank or punctuation
    if text[i].isspace():
        was_blank_punct = True

    # new word found
    if text[i].isalnum() and was_blank_punct:
        words += 1
        was_blank_punct = False

# calculate L and S
index = 0.0588 * ((letters / words) * 100) - 0.296 * ((sentences / words) * 100) - 15.8

# Round to grade
grade = round(index)

# Print grade
if grade < 1:
    print("Before Grade 1")
elif grade > 16:
    print("Grade 16+")
else:
    print(f"Grade {grade}")