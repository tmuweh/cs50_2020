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

    //check for non-numeric key
    for(int i = 0; i < strlen(argv[1]); i++) // loops through argumetn string for the presence of a non numeric char.
    {
        if(argv[1][i] < '0' || argv[1][i] > '9') // checks every character in the argument string for numeric ascii values
        {
            printf("Usage: ./caesar key \n");

            return 1;
        }

        //if exits loop without return then... no non-numeric found
    }

   //convert string to integer using atoi()
    key = atoi(argv[1]);

    //prompt user to import plain text
    string plaintext = get_string("plaintext: ");
    char ciphertext[strlen(plaintext)];

    //cipher plain text
    for(int i = 0; i < strlen(plaintext); i++)
    {
        //cipher characters preserving the case

        //preserve non alpha characters
        if(!isalpha(plaintext[i]))
        {
            ciphertext[i] = plaintext[i];
        }else
        {
            //convert indexs to simple and manipulatable reference 0 25, making a 0 and z 25 and convert back once done
            if(isupper(plaintext[i]))
            {
                ciphertext[i] = (((plaintext[i] - 'A') + key) % 26) + 'A';
            }else
            {
                ciphertext[i] = (((plaintext[i] - 'a') + key) % 26) + 'a';
            }
        }
    }

    printf("ciphertext: %s", ciphertext);

    printf("\n");

    return 0;

}