## 题目
这道题有canary、NX。64位程序，先看main函数
```
unsigned __int64 __fastcall main(__int64 a1, char **a2, char **a3)
{
  char s; // [rsp+0h] [rbp-20h]
  char v5; // [rsp+8h] [rbp-18h]
  unsigned __int64 v6; // [rsp+18h] [rbp-8h]

  v6 = __readfsqword(0x28u);
  buf_alarm();
  printf("input your name: ", a2);
  memset(&s, 0, 9uLL);
  read(0, &s, 9uLL);
  v5 = 0;
  printf("wellcome :%s\n", &s);
  return leak();
}
```
从键盘读入了9个字节，然后打印出来了，buf_alarm在设置了缓冲区之后就调用了alarm函数，下面看leak函数
```
unsigned __int64 sub_4008C5()
{
  char s; // [rsp+0h] [rbp-20h]
  unsigned __int64 v2; // [rsp+18h] [rbp-8h]

  v2 = __readfsqword(0x28u);
  printf("leave a msg: ");
  memset(&s, 0, 0x10uLL);
  read(0, &s, 0x20uLL);
  if ( strstr(&s, "%p") || strstr(&s, "$p") )
  {
    puts("do you want to leak info?");
    exit(0);
  }
  printf(&s, "$p");
  return __readfsqword(0x28u) ^ v2;
}
```
可以知道这里是有一个格式化字符串漏洞的，但是读入的s不能有%p和$p
要利用格式化字符串漏洞需要栈的底部有一块内存可以控制，在main函数中也是从shell输入用户的名字，这段内存是可以控制的。
## 解答
先停在main函数中，得到其rbp的值为0x7fffffffdda0，然后停在leak函数中，得到其rbp的值为

