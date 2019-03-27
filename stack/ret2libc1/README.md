## 解答
0x08048720	/bin/sh
0x0804A0F4	system	
.plt:08048460 ; int system(const char *command)
很簡單了，所有的步驟按照ret2syscall來做就可以了，只是注意這裏的參數傳遞不是使用寄存器而是使用棧，需要僞造一個返回值