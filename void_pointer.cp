#include<stdio.h>
int main()
{
	int x=10;
	void *ptr=&x;
	printf("value: %d\n", *(int*)ptr);
	return 0;
}

