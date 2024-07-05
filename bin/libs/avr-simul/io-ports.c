#include "io-ports.h"
#include <stdio.h>
#include <stdint.h>
#include <avr/io.h>
#include <util/delay.h>
#include <avr/interrupt.h>

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
    fdev_setup_stream(&mystdout, virtual_putchar, NULL, _FDEV_SETUP_WRITE);
    stdout = &mystdout;

    fdev_setup_stream(&mystdin, NULL, virtual_getchar, _FDEV_SETUP_READ);
    stdin = &mystdin;
}