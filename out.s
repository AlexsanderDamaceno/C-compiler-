

.globl main


main:
  push %rbp
  mov %rsp , %rbp
sub $48 , %rsp
  lea -40(%rbp) , %rax
  push %  rax
  mov $1 , %rax
  pop %  rdi
  mov %rax , (%rdi)
  lea -40(%rbp) , %rax
  push %  rax
  mov $32 , %rax
  pop %  rdi
  mov %rax , (%rdi)
  lea -40(%rbp) , %rax
  mov (%rax), %rax
  jmp .L.return.main
.L.return.main:
  mov %rbp , %rsp
  pop %rbp
  ret
