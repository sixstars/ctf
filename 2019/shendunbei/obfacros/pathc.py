from idautils import *
from idc import *
from idaapi import *
ea = 0x404F04
def reverse_N(x):
	return (x^0x78ABDA5F)-1463918478

for xref in XrefsTo(ea, 0):
	addr = xref.frm
	edi = Dword(addr-4)
	eax = reverse_N(edi)
	PatchByte(addr,0xb8)
	PatchDword(addr+1,eax)

begin=0x401116
end=0x404A06

#0xfffffeb0bd8348 cmp     [rbp+var_150], 0

it = begin
while it < end:
	cmds = Qword(it)
	size = ItemSize(it)
	if cmds == 0xfffffeb0bd8348:
		print hex(it)
		ne = it+size
		if Byte(ne) == 0x74:
			PatchByte(ne,0xEB)
		elif Byte(ne) == 0x75:
			ne_size = ItemSize(ne)
			for i in range(ne_size):
				PatchByte(i+ne,0x90)
		elif Byte(ne) == 
		print hex(it)
	it +=size

jmp_rax=0x40124F

for xref in XrefsTo(jmp_rax, 0):
	addr = xref.frm
	print hex(addr)

PatchByte(0x404033,0xEB)
PatchByte(0x40412F,0xEB)
PatchByte(0x4047F4,0xEB)


