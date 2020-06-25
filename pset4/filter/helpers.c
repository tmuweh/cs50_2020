#include "helpers.h"
#include <math.h>
#include <stdio.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    //store average of 3 colours
    BYTE avg_rgb = 0;
    //go through the first row of pixel
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            //take average of rgb values
            avg_rgb = round((image[i][j].rgbtBlue + image[i][j].rgbtGreen + image[i][j].rgbtRed) / 3.0);

            //assign the new value to variable
            image[i][j].rgbtBlue = avg_rgb;
            image[i][j].rgbtGreen = avg_rgb;
            image[i][j].rgbtRed = avg_rgb;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    //sepia values
    int sepiaRed, sepiaGreen, sepiaBlue;

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            //calculate sepia values for the 3 colours taking care of the floats and numbers larger than 255
            sepiaRed = round(0.393 * image[i][j].rgbtRed + 0.769 * image[i][j].rgbtGreen + 0.189 * image[i][j].rgbtBlue);
            sepiaGreen = round(0.349 * image[i][j].rgbtRed + 0.686 * image[i][j].rgbtGreen + 0.168 * image[i][j].rgbtBlue);
            sepiaBlue = round(0.272 * image[i][j].rgbtRed + 0.534 * image[i][j].rgbtGreen + 0.131 * image[i][j].rgbtBlue);

            //value note greater than 255 else value becomes 255
            if (sepiaRed > 255)
            {
                sepiaRed = 255;
            }
            if (sepiaGreen > 255)
            {
                sepiaGreen = 255;
            }
            if (sepiaBlue > 255)
            {
                sepiaBlue = 255;
            }
            //modify image rgb values with the calculated values
            image[i][j].rgbtRed = sepiaRed;
            image[i][j].rgbtGreen = sepiaGreen;
            image[i][j].rgbtBlue = sepiaBlue;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE copy_image[height][width];

    //make a copy of image
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width ;j++)
        {
            copy_image[i][j].rgbtRed = image[i][j].rgbtRed;
            copy_image[i][j].rgbtGreen = image[i][j].rgbtGreen;
            copy_image[i][j].rgbtBlue = image[i][j].rgbtBlue;
        }
    }

    //reflect image here
    for (int i = 0; i < height; i++)
    {
        for (int j = 0, k = width - 1; j < width ; j++, k--)
        {
            image[i][j].rgbtRed = copy_image[i][k].rgbtRed;
            image[i][j].rgbtGreen = copy_image[i][k].rgbtGreen;
            image[i][j].rgbtBlue = copy_image[i][k].rgbtBlue;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    int blurRed = 0;
    int blurGreen = 0;
    int blurBlue = 0;
    int pixels;
    for (int i = 0; i < height; i++)
    {

        for (int j = 0; j < width; j++)
        {
            //reset pixels
            pixels = 0;
            //for the ith row of pixel
            blurRed = image[i][j].rgbtRed;
            blurGreen = image[i][j].rgbtGreen;
            blurBlue = image[i][j].rgbtBlue;
            pixels = pixels + 1;

            //for the ith row of pixels
            if (i  > 0 && j - 1 > 0)
            {
                blurRed += image[i][j-1].rgbtRed;
                blurGreen += image[i][j-1].rgbtGreen;
                blurBlue += image[i][j-1].rgbtBlue;
                ++pixels;
            }
            if (i > 0 && j + 1 < width)
            {
                blurRed += image[i][j+1].rgbtRed;
                blurGreen += image[i][j+1].rgbtGreen;
                blurBlue += image[i][j+1].rgbtBlue;
                ++pixels;
            }

            //for the ith - 1 row of pixel
            if (i - 1 > 0 && j - 1 > 0)
            {
                blurRed += image[i-1][j-1].rgbtRed;
                blurGreen += image[i-1][j-1].rgbtGreen;
                blurBlue += image[i-1][j-1].rgbtBlue;
                ++pixels;
            }
            if (i - 1 > 0 && j > 0)
            {
                blurRed += image[i-1][j].rgbtRed;
                blurGreen += image[i-1][j].rgbtGreen;
                blurBlue += image[i-1][j].rgbtBlue;
                ++pixels;
            }
            if (i - 1 > 0 && j + 1 < width)
            {
                blurRed += image[i-1][j+1].rgbtRed;
                blurGreen += image[i-1][j+1].rgbtGreen;
                blurBlue += image[i-1][j+1].rgbtBlue;
                ++pixels;
            }

            //for the ith + 1 row of pixel
            if (i + 1 < height && j - 1 > 0)
            {
                blurRed += image[i+1][j-1].rgbtRed;
                blurGreen += image[i+1][j-1].rgbtGreen;
                blurBlue += image[i+1][j-1].rgbtBlue;
                ++pixels;
            }
            if (i + 1 < height && j > 0)
            {
                blurRed += image[i+1][j].rgbtRed;
                blurGreen += image[i+1][j].rgbtGreen;
                blurBlue += image[i+1][j].rgbtBlue;
                ++pixels;
            }
            if (i + 1 < height && j + 1 < width)
            {
                blurRed += image[i+1][j+1].rgbtRed;
                blurGreen += image[i+1][j+1].rgbtGreen;
                blurBlue += image[i+1][j+1].rgbtBlue;
                ++pixels;
            }

            //printf("pixels are : %d\n", pixels);
            image[i][j].rgbtRed = round((float)blurRed / pixels);
            image[i][j].rgbtGreen = round((float)blurGreen / pixels);
            image[i][j].rgbtBlue = round((float)blurBlue / pixels);
        }
    }
    return;
}