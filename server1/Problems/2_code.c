#include<stdio.h>
#include<ctype.h>
#define size 65536
int main()
{

char buff[size], num[12];
int n, t, i, j = 0;
scanf("%d",&t);
getchar();

while((n = fread(buff,1,size,stdin)) > 0){
for(i = 0; i < n; i++){
if(buff[i] == '\n'){
num[j-1] &= 0xfffffffe;
num[j] = 0;
puts(num);
j = 0;
}
else if(isdigit(buff[i]))
num[j++] = buff[i];
}
}
return 0;
}