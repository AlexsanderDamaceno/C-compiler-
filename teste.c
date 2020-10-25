{
a = 2;
b = 0;
for(a = 0; a < 10; a = a + 1){
  b = b + 1;

  if(b == 5){
  c = 0;
  for(b = 0; b < 10; b = b + 1){
    c  = c + 1;
    if(c  == 4)
         return c;
   }
 }
}

return b;

}
