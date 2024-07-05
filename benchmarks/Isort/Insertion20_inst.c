// C program for insertion sort
#include <math.h>
#include <stdio.h>
#include "io-ports.h"
#include "tick-counter.h"
#define NUMELEMS 20

int Array[NUMELEMS];

/* Function to sort an array using insertion sort*/
void insertionSort(int arr[], int n)
{
	int i, key, j;
	for (i = 1; i < n; i++) {
		key = arr[i];
		j = i - 1;

		/* Move elements of arr[0..i-1], that are
		greater than key, to one position ahead
		of their current position */
		while (j >= 0 && arr[j] > key) {
			arr[j + 1] = arr[j];
			j = j - 1;
		}
		arr[j + 1] = key;
	}
}

/* Driver program to test insertion sort */
int main()
{	InitIO();
	for(int i = 0; i < NUMELEMS; i++){//@100
		printf("Input\n");
		scanf("%d", &Array[i]);
	}

	InitTickCounter_Overflow();
	ResetTickCounter();
	insertionSort(Array, NUMELEMS);
	StopTickCounter();

	printf("#cycles %"PRIu32"\n", GetTick_Overflow());
    printf("Bye Bye!\n");

	return 0;
}
