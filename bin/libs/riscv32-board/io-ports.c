#include "io-ports.h"
#include <stdio.h>
#include <stdint.h>

// printf adapter
FILE mystdout;
FILE mystdin;

int virtual_putchar(char c, FILE *unused)
{
    special_output_port = c;
    return 0;
}

int virtual_getchar(FILE *unused)
{
    int in_char;
    in_char = special_input_port;
    return in_char;
}

void InitIO(void)
{

}