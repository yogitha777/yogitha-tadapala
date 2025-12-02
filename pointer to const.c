#include<stdio.h>
int main()
{
	int x=10,y=20;const int *ptr=&x;

	ptr=&y;
	return 0;
}
