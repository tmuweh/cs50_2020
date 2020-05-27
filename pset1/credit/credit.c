#include <stdio.h>
#include <cs50.h>
#include <math.h>


int main()

{
    long long int credit_card = 0, number = 0;
    int sum_product_digits = 0;
    int sum_other_digits = 0;
    int product_by_two = 0;
    int checksum = 0;

    do
    {
        credit_card = get_long_long("Number: ");
        //back up number to be used for distinguishing credit cards
        number = credit_card;
    }while(credit_card < 0);

    while(credit_card != 0)
    {

        sum_other_digits += (credit_card % 10);
        //move to other credit card digit after operation
        credit_card /= 10;
        // sum of digits of the products
        product_by_two = 2 * (credit_card % 10) ;
        //handles cases like sum being tenth e.g 37 so as to sum individual digits
        while(product_by_two != 0)
        {
            sum_product_digits += (product_by_two % 10);

            //update  product by two to get second digit
            product_by_two /= 10;
        }

        //move to other credit card digit after operation
        credit_card /= 10;
    }

    checksum =  sum_product_digits + sum_other_digits;

    if(checksum % 10 == 0)
    {
        //printf("Checksum ends in 0 valid\n");

       //printf("%ld\n",5555555555554444/ 100000000000000 );

        if((number / 10000000000000) == 34 || (number / 10000000000000) == 37)
            printf("AMEX\n");
        else if((number / 100000000000000) == 51 || (number / 100000000000000) == 52 || (number / 100000000000000) == 53 || (number / 100000000000000) == 54 || (number / 100000000000000) == 55 )
            printf("MASTERCARD\n");
        else if((number / 1000000000000000) == 4 || (number / 1000000000000) == 4)
            printf("VISA\n");
        else
            printf("INVALID\n");
    }
    else
    {
        printf("INVALID\n");
    }
    //printf("%lld %d %d", credit_card, sum_other_digits, sum_product_digits);
}