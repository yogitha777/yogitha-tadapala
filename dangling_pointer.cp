#include<stdio.h>
#include<stdlib.h>
int main()
{
	int *ptr=(int *)malloc(sizeof(int));
	*ptr=42;
	free(ptr);
	//printf("%d", *ptr);//
	ptr=NULL;
	return 0;
}
