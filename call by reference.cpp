#include<stdio.h>
void swap(int *x,int *y);
int main()
{
	int a=20,b=30;
	swap(&a, &b);
	printf("a=%d\tb=%d",a,b);
}
void swap(int *x, int *y)
{
	int temp;
	temp=*x;
	*x=*y;
	*y=temp;
	
}
