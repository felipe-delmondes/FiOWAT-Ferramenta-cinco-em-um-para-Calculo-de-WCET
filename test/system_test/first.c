#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include "first.h"


void soma_prefixa(int *src, int *dst, int N){
	if(N > 0){
		int i = 0;
		do{		//@10
			int tmp = 0;
			int j = 0;
			if(j < i){
				do{    //@50
					tmp += src[j];
					j++;
				}while(j < i);
				dst[i] = tmp;
			}
			i++;
		}while(i < N);
	}
}



//In�cio da fun��o main
int main(int argc, char** argv){
	int i;
	int src[5], dst[5];
	printf("Programa: %s\n\n\n", argv[0]);
	srand(time(NULL));
	for(i = 0; i<5; i++){//@20
		src[i]=rand()%10;
		dst[i]=rand()%7;
	}
	
	
	int k = 2;
	soma_prefixa(src, dst, k);
	k = calculadora();
	if(k > 0){
		k = fatorial(k);
	}
	
	printf("Fatorial: %d",k);
	return 0;
}