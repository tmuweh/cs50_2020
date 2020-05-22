#include <stdio.h>
#include <cs50.h>

int main(void)
{

	string name = get_string("What is your name?\n"); //get input name from user

	printf("Hello, %s!\n", name); //print hello plus the user name entered from user

	return 0;
}

