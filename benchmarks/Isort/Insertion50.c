// C program for insertion sort
#include <math.h>
#include <stdio.h>
#define NUMELEMS 50

int Array[NUMELEMS];

/* Function to sort an array using insertion sort*/
void insertionSort(int arr[], int n)
{
	int i, key, j;
	for (i = 1; i < n; i++) {//@49
		key = arr[i];
		j = i - 1;

		/* Move elements of arr[0..i-1], that are
		greater than key, to one position ahead
		of their current position */
		while (j >= 0 && arr[j] > key) {//@1225
			arr[j + 1] = arr[j];
			j = j - 1;
		}
		arr[j + 1] = key;
	}
}

/* Driver program to test insertion sort */
int main()
{
	for(int i = 0; i < NUMELEMS; i++){//@50
		printf("Input\n");
		scanf("%d", &Array[i]);
	}

	insertionSort(Array, NUMELEMS);

	return 0;
}
