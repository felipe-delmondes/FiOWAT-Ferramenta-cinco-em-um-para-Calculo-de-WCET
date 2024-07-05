#ifndef FIRST_H
#define FIRST_H

#include <stdio.h>

int calculadora(void){
	char texto[10];
	printf("Digite um frase curta: ");
	scanf("%s", texto);
	return texto[0]/20;	
}


int fatorial(int n){
	if(n <= 1){
		return 1;
	}
	else{
		return n*fatorial(n-1);
	}
}

#endif