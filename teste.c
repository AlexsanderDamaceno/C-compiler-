
int main(){
   

   struct { int a;  int  b;  int c[10][10]; } b;

   	int i   = 0; 
    int j   = 0; 
    int sum = 0; 
  
	for(; i < 10; i = i + 1){
	  for(j = 0; j < 10; j = j + 1){	
            b.c[i][j] = 1; 
        }
	}


	for(i = 0; i < 10; i = i + 1){
	  for(j = 0; j < 10; j = j + 1)	
         sum  = sum + b.c[i][j];
	}

	return sum; 


}
 