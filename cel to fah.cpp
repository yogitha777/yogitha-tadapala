#include<stdio.h>
int main()
{
	float celsius,fahrenheit;
	printf("enter temp in celsius");
	scanf("%f",&celsius);
	fahrenheit=(1.8*celsius)+32;
	printf("temp in fahrenheit:%2f",fahrenheit);
	return 0;
}
