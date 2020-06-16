#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{

    //commandline argument must be 2
    if (argc != 2)
    {
        printf("Usage: ./recover forensic_image\n");
        return 1;
    }

    //open file
    FILE *file = fopen(argv[1], "r");

    //check if file was open successfully
    if (file == NULL)
    {
        printf("Image Unsupported!\n");
        return 1;
    }


}
