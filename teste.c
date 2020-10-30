
int f2(){

  int  a = 0;
  int count = 0;
  for(count = 0; count < 10; count = count + 1){
    a =  a + 1;
  }

  return a;

}

int f(){

  return ((20*20)/(100+100)) + f2();
}

int main(){

  return (10 + f())/22;


}
