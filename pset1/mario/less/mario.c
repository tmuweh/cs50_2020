#include <stdio.h>
#include <cs50.h>

int main(void)
{
    int height = 0;
    do{
        height = get_int("Enter a height: ");

    }while(height < 1 || height > 8);

     for (int  row  =  0; row < height; row++)
    {
        for(int column = 0; column <= height; column++)
        {
            //print space or hash tag using formular nth row + space <= height - 1 print space else, print hash
            if( (row + column) < height)

                printf(" ");
            else

                printf("#");

        }
        printf("\n");
    }

    return 0;
}
