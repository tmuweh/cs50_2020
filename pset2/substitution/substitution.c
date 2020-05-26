#include <stdio.h>
#include <ctype.h>
#include <cs50.h>
#include <string.h>
#include <stdlib.h>

int main(int argc, string argv[])
{
  //check if user put in an argument
  if(argc != 2)
  {
      printf("Usage: ./caesar key \n");

      return 1;
  }

  //check for length of argument
  if (strlen(argv[1]) != 26)
  {
    printf("Key must contain 26 characters.");
    return 1;
  }

  //validate 26 key cipher

  int letter[26]; //store counts of occurrences of individual letters 0 - 25

  for(int i = 0; i < sizeof(letter)/sizeof(int); i++)
    letter[0] = 0;

  for (int i = 0; i < strlen(argv[1]); i++) // loops through argumetn string
  {

    if (!isalpha(argv[1][i])) //for alpha character
    {
      printf("Usage: ./caesar key \n");
      return 1;
    }
    //check for repeated char
    if (isupper(argv[1][i]))
    {
      ++letter[argv[0][i] - 'A'];
    }
    else
    {
      ++letter[argv[1][i] - 'a'];
    }
    //letter occured more than once
    if(letter[i] > 1)
    {
      printf("Key must not contain repeated characters.");
      return 1;
    }
    //if exits loop without return then... 26 Key accepted
  }

  //cipher text is case insensitive


  //get plain text

    //plain text is case sensitive

  //cipher plain text

    //check availability and case

  //print cipher text

  //print new line
  printf("\n");

  return 0;
}