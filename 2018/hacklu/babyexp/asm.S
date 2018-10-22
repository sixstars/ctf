BITS 64

section .text 
global _start
_start:
	;write execve("/bin/sh",0,0);
	xor rax,rax
	mov al, 60
	syscall