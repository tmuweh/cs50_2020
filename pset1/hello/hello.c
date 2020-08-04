#include <stdio.h>
#include <cs50.h>

int main(void)
{
	//get input name from user
	string name = get_string("What is your name?\n");
	//print hello plus the user name entered from user
	printf("Hello, %s!\n", name);

	return 0;
}

