#include<stdio.h>
int main()
{
	int x=10,y=20;
	int *const ptr=&x;
	*ptr=15;
	return 0;
}


