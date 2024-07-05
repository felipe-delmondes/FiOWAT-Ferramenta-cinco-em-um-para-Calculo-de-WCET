#ifndef AVR_CUSTOM_IO_H
#define AVR_CUSTOM_IO_H

#include <avr/io.h>
#include <stdio.h>

__attribute__((optnone)) void InitIO(void);

int uart_getchar(FILE *);
int uart_putchar(char, FILE *);

#endif /* AVR_CUSTOM_IO_H */