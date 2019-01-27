key="lOv3"
cnt = 0
for i in range(0x40341D,0x40350d):
# for i in range(0x40341D,0x6070A8):
	PatchByte(i,Byte(i)^ord(key[cnt]))
	cnt+=1
	if(cnt == 4):
		cnt=0


cnt = 0
for i in range(0x40330F,0x4033FF):
# for i in range(0x40341D,0x6070A8):
	PatchByte(i,Byte(i)^ord(key[cnt]))
	cnt+=1
	if(cnt == 4):
		cnt=0


cnt = 0
for i in range(0x4033FF,0x4033FF+0x1E):
# for i in range(0x40341D,0x6070A8):
	PatchByte(i,Byte(i)^ord(key[cnt]))
	cnt+=1
	if(cnt == 4):
		cnt=0


def patch_elf(address,length_addr,key):
	# key="lOv3"
	cnt = 0
	for i in range(address,address+Dword(length_addr)):
	# for i in range(0x40341D,0x6070A8):
		PatchByte(i,Byte(i)^ord(key[cnt]))
		cnt+=1
		if(cnt == len(key)):
			cnt=0


patch_elf(0x402D55,0x6070C4,"D0l1")

