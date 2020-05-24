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

    printf("CipherText: %s", ciphertext);

    printf("\n");

    return 0;

}