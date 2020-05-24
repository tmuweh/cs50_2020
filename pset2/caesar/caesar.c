#include <stdio.h>
#include <cs50.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>



int main(int argc, string argv[])
{
    int key = 0;
    //check for arguments and print respective message
    if(argc != 2)
    {
        printf("Usage: ./caesar key \n");

        return 1;
    }

    //convert string to integer using atoi()
    key = atoi(argv[1]);

    //assumes atoi converts non digits to zero so text if converted is zero :)
    if(key == 0)
    {
        printf("Usage: ./caesar key \n");

        return 1;
    }

    //prompt user to import plain text
    string plaintext = get_string("PlainText: ");
    string ciphertext = "";

    //length of string
    int size = strlen(plaintext);
    printf("%d,", size);
    //cipher plain text

        //cipher one character to preserve the case

        //preserve non alphanum characters


    printf("\n");

    return 0;

}