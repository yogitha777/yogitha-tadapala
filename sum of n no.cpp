#include<stdio.h>
int main()
{
	int sum=0, i=1;
	while(i<=10)
	{
		sum=sum+i;
        i++;
	}
	printf("%d\t", sum);
	return 0;
}
