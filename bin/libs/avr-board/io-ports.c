#include "io-ports.h"
#include <stdio.h>
#include <stdint.h>
#include <avr/io.h>
#include <util/delay.h>
#include <avr/interrupt.h>


#define FOSC 16000000
#define BAUD 9600
#define MYUBRR (((((FOSC * 10) / (16L * BAUD)) + 5) / 10))
#define RX_BUFSIZE 64

// printf adapter
FILE mystdout;
FILE mystdin;


int uart_getchar(FILE *stream) {
    uint8_t c;
    char *cp, *cp2;
    static char b[RX_BUFSIZE];
    static char *rxp;

    if (rxp == 0) {
        for (cp = b;;) {
            loop_until_bit_is_set(UCSR0A, RXC0);
            if (UCSR0A & (1 << FE0))
                return _FDEV_EOF;
            if (UCSR0A & (1 << DOR0))
                return _FDEV_ERR;
            c = UDR0;
            if (c == '\r')
                c = '\n';
            if (c == '\n') {
                *cp = c;
                rxp = b;
                break;
            }
            else if (c == '\t')
                c = ' ';

            if ((c >= ' ' && c <= '\x7e') || c >= '\xa0') {
                if (cp == b + RX_BUFSIZE - 1)
                    uart_putchar('\a', stream);
                else {
                    *cp++ = c;
                }
                continue;
            }
        }
    }

    c = *rxp++;
    if (c == '\n')
        rxp = 0;
    return c;
}


int uart_putchar(char c, FILE *stream)
{
    if (c == '\n')
        uart_putchar('\r', stream);
    // loop_until_bit_is_set(UCSR0A, UDRE0);
    while (( UCSR0A & (1<<UDRE0)) == 0) {};
    UDR0 = c;
    return 0;
}

void InitIO(void)
{
    // Setup Baud Rate (p.159)
    UBRR0H = MYUBRR >> 8;
    UBRR0L = MYUBRR;

    // Enable TX and RX  (p.160)
    UCSR0B = (1 << RXEN0) | (1 << TXEN0);

    // Setup a user-supplied buffer as an stdio stream.
    fdev_setup_stream(&mystdout, uart_putchar, NULL, _FDEV_SETUP_WRITE);
    stdout = &mystdout;

    fdev_setup_stream(&mystdin, NULL, uart_getchar, _FDEV_SETUP_READ);
    stdin = &mystdin;
}

