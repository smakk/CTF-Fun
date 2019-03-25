## 解答
主函數同樣是gets的溢出，不過同事還將字符串複製給了buf2
```
int __cdecl main(int argc, const char **argv, const char **envp)
{
  char s; // [esp+1Ch] [ebp-64h]

  setvbuf(stdout, 0, 2, 0);
  setvbuf(stdin, 0, 1, 0);
  puts("No system for you this time !!!");
  gets(&s);
  strncpy(buf2, &s, 0x64u);
  printf("bye bye ~");
  return 0;
}
```
這跳轉到buf2去，然後執行buf2處的代碼，asm(shellcraft.sh())生成shellcode的彙編代碼，ljust補充剩餘字節