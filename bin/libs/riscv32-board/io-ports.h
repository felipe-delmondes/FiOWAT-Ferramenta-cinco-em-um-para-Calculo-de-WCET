#ifndef AVR_CUSTOM_IO_H
#define AVR_CUSTOM_IO_H

__attribute__((optnone)) void InitIO(void);

int virtual_putchar(char, FILE *);
int virtual_getchar(FILE *);

#endif /* AVR_CUSTOM_IO_H */