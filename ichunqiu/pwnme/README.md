## 程序分析
### 程序功能分析
main函數
```
__int64 __fastcall main(__int64 a1, char **a2, char **a3)
{
  __int64 v3; // rdx
  __int64 v4; // rcx
  __int64 v5; // r8
  __int64 v6; // r9
  FILE *v7; // rdi
  __int64 v8; // rdx
  __int64 v9; // rcx
  __int64 v10; // r8
  __int64 v11; // r9
  __int64 buf; // [rsp+10h] [rbp-60h]
  __int64 v14; // [rsp+18h] [rbp-58h]
  __int64 v15; // [rsp+20h] [rbp-50h]
  __int64 v16; // [rsp+28h] [rbp-48h]
  __int64 v17; // [rsp+30h] [rbp-40h]
  __int64 v18; // [rsp+40h] [rbp-30h]
  __int64 v19; // [rsp+48h] [rbp-28h]
  char v20[20]; // [rsp+50h] [rbp-20h]
  int v21; // [rsp+64h] [rbp-Ch]

  v18 = 48LL;
  v19 = 0LL;
  *(_DWORD *)v20 = 0;
  *(_QWORD *)&v20[4] = 48LL;
  *(_QWORD *)&v20[12] = 0LL;
  v21 = 0;
  //这个函数只有打印功能
  print_welcome();
  while ( 1 )
  {
  //关键函数，读取用户以及密码
    register(
      (__int64)&buf,
      (__int64)a2,
      v3,
      v4,
      v5,
      v6,
      v18,
      v19,
      *(__int64 *)v20,
      *(__int64 *)&v20[8],
      *(__int64 *)&v20[16]);
    if ( (_BYTE)buf != 48 )
      break;
    puts("Register failure,try again...");
    fflush(stdout);
  }
  puts("Register Success!!");
  v7 = stdout;
  fflush(stdout);
  //菜单选项
  menu((__int64)v7, (__int64)a2, v8, v9, v10, v11, buf, v14, v15, v16, v17);
  return 0LL;
}
```
主要功能在于register和menu，看menu
```
__int64 __fastcall menu(__int64 s, __int64 a2, __int64 a3, __int64 a4, __int64 a5, __int64 a6, __int64 sa, __int64 a8, __int64 a9, __int64 a10, __int64 a11)
{
  FILE *v11; // rdi
  int v12; // eax
  __int64 v13; // rdx
  __int64 v14; // rcx
  __int64 v15; // r8
  __int64 v16; // r9

  v11 = stdin;
  setbuf(stdin, 0LL);
  while ( 1 )
  {
    //获取一个输入，表示选择
    v12 = getoptions();
    switch ( v12 )
    {
      case 2:
        edit_account((__int64)&sa, 0LL, v13, v14, v15, v16, sa, a8, a9, a10, a11);
        break;
      case 3:
        return exit(v11, 0LL);
      case 1:
        showaccount((char)v11, 0LL, v13, v14, v15, v16, sa, a8, a9);
        break;
      default:
        puts("error options");
        fflush(stdout);
        break;
    }
    v11 = stdout;
    fflush(stdout);
  }
}
```
程序的漏洞在edit_account和showaccount处
```
int __fastcall showaccount(char format, __int64 a2, __int64 a3, __int64 a4, __int64 a5, __int64 a6, char formata, __int64 a8, __int64 a9)
{
//直接输出字符串，有格式化字符串漏洞，字符串地址在main函数中为buf
  printf(&formata, a2, a3, a4, a5, a6);
  return printf((const char *)&a9 + 4);
}
```
还有一个缓冲区溢出的漏洞，在edit_account中
```
__int64 __fastcall edit_account(__int64 s, __int64 a2, __int64 dest, __int64 a4, __int64 a5, __int64 a6, __int64 sa, __int64 a8, __int64 desta, __int64 a10, __int64 a11)
{
  int v12; // [rsp+18h] [rbp-18h]
  char v13; // [rsp+1Fh] [rbp-11h]
  void *buf; // [rsp+20h] [rbp-10h]
  void *src; // [rsp+28h] [rbp-8h]

  src = malloc(0x12CuLL);
  buf = malloc(0x12CuLL);
  puts("please input new username(max lenth:20): ");
  fflush(stdout);
  v13 = read(0, buf, 0x12CuLL);
  if ( v13 <= 0 || v13 > 20 )
  {
    puts("len error(max lenth:20)!try again..");
    fflush(stdout);
    *(_QWORD *)s = sa;
    *(_QWORD *)(s + 8) = a8;
    *(_QWORD *)(s + 16) = desta;
    *(_QWORD *)(s + 24) = a10;
    *(_QWORD *)(s + 32) = a11;
  }
  else
  {
    memset(&sa, 0, 0x14uLL);
    strcpy((char *)&sa, (const char *)buf);
    puts("please input new password(max lenth:20): ");
    fflush(stdout);
    v12 = read(0, src, 0x12CuLL);
    //漏洞在这里，读取的字节数先转成了byte，再转成了unsigned
    if ( (_BYTE)v12 && (unsigned __int8)v12 <= 0x14u )
    {
      memset((char *)&desta + 4, 0, 0x14uLL);
      sub_400A90(src, v12);
     //读取内容
      memcpy((char *)&desta + 4, src, v12);
      fflush(stdout);
      *(_QWORD *)s = sa;
      *(_QWORD *)(s + 8) = a8;
      *(_QWORD *)(s + 16) = desta;
      *(_QWORD *)(s + 24) = a10;
      *(_QWORD *)(s + 32) = a11;
    }
    else
    {
      puts("len error(max lenth:20)!try again..");
      fflush(stdout);
      *(_QWORD *)s = sa;
      *(_QWORD *)(s + 8) = a8;
      *(_QWORD *)(s + 16) = desta;
      *(_QWORD *)(s + 24) = a10;
      *(_QWORD *)(s + 32) = a11;
    }
  }
  return s;
}
```
这个函数的溢出点根据反编译出的结果有些问题，直接看汇编可以看出来
```
mov     [rbp+var_18], eax
mov     eax, [rbp+var_18]
mov     [rbp+var_19], al
cmp     [rbp+var_19], 0
jnz     short loc_400C0C
```
上面这段直接截取了eax的al段，放到了[rbp+var_19]，而在后面的比较中，直接使用该值和0x14来进行比较了，所以这里会有溢出的情况，当输入的数据长度达到0x101，小于0x114的时候都能（最后一个字节符合大小判断即可）
```
loc_400C0C:
cmp     [rbp+var_19], 14h
ja      short loc_400C8E
```
查看程序安全机制
[*] '/home/likaiming/workspace/CTF-Fun/ichunqiu/pwnme/pwnme'
    Arch:     amd64-64-little
    RELRO:    Full RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
不能重写GOT，那格式化字符串漏洞只能用来泄露数据，有缓冲区溢出，可以直接ROP
### 格式化漏洞利用
格式化字符串要实现任意位置读写，需要在栈底有一块能自由控制的空间，这里需要分析一下写入用户名和密码的位置，下面的变量以mian函数中参数为例子
回到register函数，可以知道，用户名写在v18位置，密码写在v20+4的位置
看edit_account和showaccount函数，可以看出，用户名写在buf位置，v15+4的位置
好像还是不一样的位置
使用gdb让程序停在printf处，发现printf的参数，也就是rdi的值在0x7fffffffdcb0处，而rsp、rbp的值在0x7fffffffdca0处，也就是说buf=0x7fffffffdcb0，然后让gdb停在下一个printf处（打印密码的位置），发现RDI的值在0x7fffffffdcc4处，也就是说v15+4=0x7fffffffdcc4。查看静态代码，也可以得知v15和buf的位置差了0x10。
要利用格式化字符漏洞，需要讲带格式化参数的字符串写到栈底，也就是在buf处。而在密码处需要写入我们想读或者是写的地址。
0x7fffffffdca0和0x7fffffffdcc4差了4.5个参数，再加上用寄存器传递的6个参数。也就是buf处的格式化参数位置必须大于等于11，然后密码还需要填满前0.5个字节，凑成整数。
### 缓冲区溢出漏洞利用
使用pattern.py脚本
```
python ../../pattern.py create 272
```
得出产生异常时ret的值为0x3562413462413362
```
python ../../pattern.py offset 0x3562413462413362
```
得出偏移为40
使用ROPgadget寻找gadget，可以知道文件中是有sh这个字符串的，所以只需要一条gadget就可以了
0x0000000000400ed3 : pop rdi ; ret
0x000000000040048f : sh
最后使用ljust将payload调整为合适大小
## 解答
可以看具体代码了




