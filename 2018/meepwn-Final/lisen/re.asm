func:
push rbp
mov rbp,rsp
mov dword ptr[rbp-0x24],edi
mov qword ptr[rbp-0x30],rsi
mov qword ptr[rbp-0x38],rdx
mov rax,qword ptr[rbp-0x30]
mov eax,dword ptr[rax]
mov dword ptr[rbp-0x10],eax
mov rax,qword ptr[rbp-0x30]
mov eax,dword ptr[rax+4]
mov dword ptr[rbp-0xc],eax
mov dword ptr[rbp-0x8],0x0
mov dword ptr[rbp-0x4],1952997742
mov dword ptr[rbp-0x14],0
jmp .heree
.backk:
mov eax,dword ptr[rbp-0xc]
shl eax,4
mov edx,eax
mov eax,dword ptr[rbp-0xc]
shr eax,5
xor edx,eax
mov eax,dword ptr[rbp-0xc]
lea ecx,[rax+rdx]
mov eax,dword ptr[rbp-8]
and eax,3
lea rdx,[rax*4]
mov rax,qword ptr[rbp-0x38]
add rax,rdx
mov edx,dword ptr[rax]
mov eax,dword ptr[rbp-8]
add eax,edx
xor eax,ecx
add dword ptr[rbp-0x10],eax
mov eax,dword ptr[rbp-0x4]
add dword ptr[rbp-0x8],eax
mov eax,dword ptr[rbp-0x10]
shl eax,4
mov edx,eax
mov eax,dword ptr[rbp-0x10]
shr eax,5
xor edx,eax
mov eax,dword ptr[rbp-0x10]
lea ecx,[rdx+rax]
mov eax,dword ptr[rbp-0x8]
shr eax,11
mov eax,eax
and eax,3
lea rdx,[rax*4]
mov rax,qword ptr[rbp-0x38]
add rax,rdx
mov edx,dword ptr[rax]
mov eax,dword ptr[rbp-0x8]
add eax,edx
xor eax,ecx
add dword ptr[rbp-0xc],eax
add dword ptr[rbp-0x14],1

.heree:
mov eax,dword ptr[rbp-0x14]
cmp eax,dword ptr[rbp-0x24]
jl .backk

mov rax,qword ptr[rbp-0x30]
mov edx,dword ptr[rbp-0x10]
mov dword ptr [rax],edx/*TODO*/
mov rax,qword ptr[rbp-0x30]
lea rdx,[rax+4]
mov eax,dword ptr[rbp-0xc]
mov dword ptr [rdx],eax
leave
ret





main:
push rbp
mov rbp,rsp
sub rsp,128
// get [fs:0x28]
xor eax,eax
mov dword ptr[rbp-0x70],99
mov dword ptr[rbp-0x6c],111
mov dword ptr[rbp-0x68],116
mov dword ptr[rbp-0x64],104
mov dword ptr[rbp-0x60],97
mov dword ptr[rbp-0x5c],110
mov dword ptr[rbp-0x74],8
mov dword ptr[rbp-0x50],2492539336
mov dword ptr[rbp-0x4c],55281258
mov dword ptr[rbp-0x48],2196754676
mov dword ptr[rbp-0x44],2821507075
mov dword ptr[rbp-0x40],1768494383
mov dword ptr[rbp-0x3c],3785976562
mov dword ptr[rbp-0x38],3783291222
mov dword ptr[rbp-0x34],2216322110
mov dword ptr[rbp-0x30],3164129935
mov dword ptr[rbp-0x2c],3771161883
mov dword ptr[rbp-0x28],1972774763
mov dword ptr[rbp-0x24],1762315061
mov dword ptr[rbp-0x20],3932463561
mov dword ptr[rbp-0x1c],1672697163
mov dword ptr[rbp-0x18],1101278339
mov dword ptr[rbp-0x14],4284021098
mov dword ptr[rbp-0x10],2995319743
mov dword ptr[rbp-0xc],3170481900
mov dword ptr[rbp-0x78],0
jmp .here
.back:
mov eax,dword ptr[rbp-0x78]
lea edx,[eax+eax]
lea rax,qword ptr[rbp-0x50]
mov edx,edx
shl rdx,2
lea rcx,[rdx+rax]
mov eax,dword ptr[rbp-0x74]
lea rdx,qword ptr[rbp-0x70]
mov rsi,rcx
mov edi,eax
call func
add dword ptr[rbp-0x78],1
.here:
cmp dword ptr[rbp-0x78],8
jle .back
mov eax,0
leave
ret













