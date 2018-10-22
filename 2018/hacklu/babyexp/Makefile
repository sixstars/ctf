.PHONY: all
all:
	rm -f shellcode asm.elf asm.o
	nasm -f elf64 asm.template
	ld -o asm.elf asm.o -m elf_x86_64 
	for i in $$(objdump -d ./asm.elf |grep "^ " |cut -f2); do echo -n '\x'$$i >> shellcode; done;
	cat shellcode 
clean: 
	rm -f shellcode asm.elf asm.o

