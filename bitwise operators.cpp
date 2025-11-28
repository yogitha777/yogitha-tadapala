#include<stdio.h>
int main()
{
	int a,b;
	printf("enter two numbers");
	scanf("%d%d",&a,&b);
	printf("bitwise operations:\n");
	printf("bitwise AND(&)\n%d&%d=%d\n",a,b,a&b);
	printf("bitwise OR(|)\n%d&%d=%d\n",a,b,a|b);
	printf("bitwise XOR(^)\n%d&%d=%d\n",a,b,a^b);
	printf("left shift(<<)\n%d&%d=%d\n",a,b,a<<b);
	printf("right shift(>>)\n%d&%d=%d\n",a,b,a>>b);
	return 0;
}
