#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <allegro.h>

#define DIR_X 0
#define DIR_Y 1

int getpixelintensity(BITMAP* image, int x, int y)
{
    int value = getpixel(image, x, y);
    return (getr(value) + getg(value) + getb(value)) / 3;
}

void putpixelintensity(BITMAP* image, int x, int y, int value)
{
    int color = makeacol(value, value, value, 1);
    putpixel(image, x, y, color);
}

int compute_gradient(BITMAP* image, int x, int y, int dir)
{
    const static int grad_tables[2][3][3] = {
        {
            {-1, 0, 1},
            {-2, 0, 2},
            {-1, 0, 1}
        },
        {
            {1,   2,  1},
            {0,   0,  0},
            {-1, -2, -1}
        }
    };

    if (!(0 < x && x < image->w-1 && 0 < y && y < image->h-1))
        return 255;

    int i, j;
    int sum = 0;

    for (i=-1; i<=1; i++)
        for (j=-1; j<=1; j++)
            sum += getpixelintensity(image, x+i, y+j) * grad_tables[dir][i+1][j+1];

    return sum;
}

int compute_sobel(int grad_x, int grad_y)
{
    int sobel = roundf(sqrtf(grad_x*grad_x + grad_y*grad_y));

    if (sobel < 0)
        sobel = 0;
    else if (sobel > 255)
        sobel = 255;

    return sobel;
}

int compute_direction(int grad_x, int grad_y)
{
    if (grad_x == 0)
        return 0;

    return round((atanf(grad_y/grad_x) + M_PI/2)/M_PI * 255);
}

int main(int argc, char *argv[])
{
    int x, y, failure;

    if (argc != 4) {
        printf("Usage: gradient input.bmp sobel.bmp gradient-direction.bmp\n");
        printf("Compute sobel.bmp and gradient-direction.bmp based on input.bmp\n");
        printf("The filenames above should be replaced with their "
               "desired semantic equalivalent, of course.\n");
        exit(1);
    }

    char* input_filename = argv[1];
    char* sobel_filename = argv[2];
    char* direction_filename = argv[3];

    allegro_init();
    set_color_depth(32);

    BITMAP* input_image = load_bitmap(input_filename, NULL);

    if (!input_image) {
        printf("The given input image \"%s\" cannot be loaded.\n", input_filename);
        printf("Try a .BMP file instead.\n", input_filename);
        exit(2);
    }

    BITMAP* sobel_image = create_bitmap(input_image->w, input_image->h);
    BITMAP* direction_image = create_bitmap(input_image->w, input_image->h);

    for (x=0; x<input_image->w; x++)
        for (y=0; y<input_image->h; y++) {

            int grad_x = compute_gradient(input_image, x, y, DIR_Y);
            int grad_y = compute_gradient(input_image, x, y, DIR_X);

            int sobel = compute_sobel(grad_x, grad_y);
            int direction = compute_direction(grad_x, grad_y);

            putpixelintensity(sobel_image, x, y, sobel);
            putpixelintensity(direction_image, x, y, direction);
       }

    if (failure = save_bitmap(sobel_filename, sobel_image, NULL))
        printf("The sobel image \"%s\"cannot be saved.\n");

    if (failure |= save_bitmap(direction_filename, direction_image, NULL))
        printf("The sobel image \"%s\"cannot be saved.\n");

    if (failure) {
        exit(3);
    }

    return 0;
}
