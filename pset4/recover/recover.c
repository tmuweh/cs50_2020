#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>

typedef uint8_t BYTE;

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

    //get 512bytes of memory
    BYTE *byte = malloc(512 * sizeof(BYTE));

    //jpeg found parameters
    bool current_jpg = false;
    bool new_jpg = false;

    //JPeGs found
    int jpegs_found = 0;

    //file name
    char image_name[10];

    //create an img pounter
    FILE *img = NULL;

    //read 512 bytes
    do{
        fread(byte, sizeof(BYTE), 512, file);

        if (byte[0] == 0xff && byte[1] == 0xd8  && byte[2] == 0xff && (byte[3] & 0xf0) == 0xe0 )
        {
            //found jpeg count upp
            ++jpegs_found;

            //set found jpg to true
            new_jpg = true;

            sprintf(image_name, "%03i.jpg", jpegs_found-1);

            //close previous image file
            if (img != NULL)
                fclose(img);

            //open new file for writing
            img = fopen(image_name, "w");

            //write to file
            fwrite(byte, sizeof(BYTE), 512,  img);

        }

        //continue writing jpg across 512 byte if new jpg is not found
        if (current_jpg && !new_jpg )
        {
            fwrite(byte, 512, sizeof(BYTE), img);
        }

        //once found a new jpeg change current jpeg to true
        if (new_jpg)
        {
            current_jpg = true;
            new_jpg = false;
        }
    }while(!feof(file));

    fclose(img);
    free(byte);
    fclose(file);
    //check for jpg signature

        //if found open file write and close once


        //else


}
