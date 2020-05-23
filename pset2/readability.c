#include <stdio.h>
#include <cs50.h>
#include <ctype.h>
#include <string.h>
#include <math.h>



int main(void)

{
    //prompt for user to enter text
    string text = get_string("Text: ");

    //get string length of the entered text
    int n = strlen(text);

    //store counts of sentences, words and letters
    int sentences = 0;
    int words = 0;
    int letters = 0;

    //check for a char after spcace is a letter hence a word.
    bool was_blank_punct = false;

    for(int i = 0; i!= n; i ++)
    {

        //counts letters and nummbers e.g 2 years = six letters
        if(isalnum(text[i]))
        {
            letters++;

            // counts first word in the text
            if(words == 0)
            {
                words++;
            }
        }

        //counts all punctuations as new sentences
        if(text[i] == '.' || text[i] =='?' || text[i] =='!')
        {
            sentences++;
        }

        //sets a new value for was_blank_punct
        if(isblank(text[i]))
        {
            was_blank_punct = true;

        }

        if( isalnum(text[i]) && was_blank_punct)
        {
           words++;
           was_blank_punct = false;
        }

    }
    //calculate values of L and S

    //insert into formula
    float index = 0.0588 * ((letters / (float)words) * 100) - 0.296 * ((sentences / (float)words) * 100) - 15.8;

    //round to nearest integer
    int grade = (int) rint(index);

    //display grade level
    if( grade < 1)
    {
        printf("Before Grade 1\n");
    }
    else
    if(grade > 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %d\n", grade);
    }

    return 0;
}