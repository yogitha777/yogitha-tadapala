#include<stdio.h>
int main()
{
	int arr[30],i,j,temp,num;
	printf("enter no. of elements");
	scanf("%d",&num);
	for(i=0;i<5;i++)
	{
		scanf("%d",&arr[i]);
	}
	j=i-1;
	i=0;
	while(i<j)
	{
	temp=arr[i];
	arr[i]=arr[j];
	arr[j]=temp;
	i++;
}
printf("result after reversal");
for(i=0;i<5;i++)
{
	printf("%d",arr[i]);
	return 0;
}
	
	
}
