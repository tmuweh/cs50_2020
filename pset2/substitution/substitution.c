#include <stdio.h>
#include <cytpe.h>
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
  if (strlen(argv[i]) != 26)
  {
    printf("Key must contain 26 characters.");
    return 1;
  }

  //validate 26 key cipher 
  for (int i = 0; i < strlen(argv[1]); i++) // loops through argumetn string
  {
    if (!isalpha(argv[1][i])) //for alpha character
    {
      printf("Usage: ./caesar key \n");
      return 1;
    }
    if (!) //check for repeated char
    {
      
    }
    
    
    //if exits loop without return then... no non-numeric found
  }

  //cipher text is case insensitive


  //get plain text

    //plain text is case sensitive

  //cipher plain text

    //check availability and case

  //print cipher text

  return 0;
}