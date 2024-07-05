#ifndef AVR_CUSTOM_IO_H
#define AVR_CUSTOM_IO_H

#include <avr/io.h>
#include <stdio.h>

/* Simulator conections */
#define special_output_port (*((volatile char *)0x20))

#define special_input_port (*((volatile char *)0x22))


__attribute__((optnone)) void InitIO(void);


int virtual_putchar(char, FILE *);
int virtual_getchar(FILE *);

#endif /* AVR_CUSTOM_IO_H */