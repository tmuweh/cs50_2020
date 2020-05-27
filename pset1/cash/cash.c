#include <stdio.h>
#include <cs50.h>
#include <math.h>

int main(void)
{
    float change = 0;
    int cent = 0;
    int coins = 0;
    do
    {
        change = get_float("Change owed: ");

    }while(change < 0.00);

    //convert dollar to cents
    cent = round(change * 100);
    while ( cent != 0)
    {
        if(cent >= 25)
        {
            coins ++;
            cent -= 25;
        }
        else if(cent >= 10)
        {
            coins ++;
            cent -= 10;
        }
        else if(cent >= 5)
        {
            coins ++;
            cent -= 5;
        }
        else if(cent >= 1)
        {
            coins ++;
            cent -= 1;
        }
        else
        {
            cent = 0;
        }
    }

    printf("%i\n", coins);


}