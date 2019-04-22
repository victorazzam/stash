; Compile with --> nasm -f macho code.nasm
; Link with -----> ld -arch i386 -e _start code.o

SECTION .text

GLOBAL _start
GLOBAL L1
GLOBAL L2
GLOBAL L3

_start:
  MOV ebx,19
  MOV ecx,31218
  SUB ebx,ecx
  MOV eax,19211
  ADD ebx,eax
  CMP ebx,eax
  JL L2
  JMP L1

L1:
  IMUL ebx,eax
  ADD ebx,eax
  MOV eax,ebx
  SUB eax,ecx
  JMP L3

L2:
  IMUL ebx,eax
  SUB ebx,eax
  MOV eax,ebx
  ADD eax,ecx

L3:
  INT3
  NOP