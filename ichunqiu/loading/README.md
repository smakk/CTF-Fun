## 题目
main函数，好像只有这一个函数
```
int __cdecl main(int argc, const char **argv, const char **envp)
{
  signed int v4; // [esp+24h] [ebp-Ch]
  int i; // [esp+28h] [ebp-8h]
  int (*v6)(void); // [esp+2Ch] [ebp-4h]

  v6 = (int (*)(void))mmap(0, 0x8000u, 7, 34, -1, 0);
  for ( i = 0; i <= 0x1FFF && __isoc99_scanf((const char *)&unk_80485F0, &v4); ++i )
    *((float *)v6 + i) = (long double)v4 / 2333.0;
  write(1, "try to pwn\n", 0xBu);
  return v6();
}
```
调用mmap分配内存，属性为读写执行
然后看scanf函数，字符串为%d，读取一个数
```
.rodata:080485F0 unk_80485F0     db  25h ; %             ; DATA XREF: main+53↑o
.rodata:080485F1                 db  64h ; d
.rodata:080485F2                 db    0
```
然后向分配的地址中写入数据，最后返回v6处的函数，很明显，这题就是要构造shellcode
## 解答
然后这题直接搜索float shellcode就可以找到原题了。
问题在于使用整形去控制浮点类型的数是有范围的，所以需要很精确的选择shellcode，和填充指令，比较复杂，以后有机会再去研究吧``
