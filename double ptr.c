#include<stdio.h>
int main()
{
	int x=5;
	int *p=&x;
	int **pp=&p;
	printf("%d\n", **pp);
	return 0;
}
