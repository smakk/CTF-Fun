## 题目
这个题好像直接输入特定的字符串就可以了，题目里面有system函数
看main函数
```
void __cdecl main()
{
  char *v0; // ST18_4
  char *v1; // ST1C_4

  setbuf(stdin, 0);
  setbuf(stdout, 0);
  setbuf(stderr, 0);
  v0 = read_fromuser();
  v1 = sub_8048BAD((int)v0);
  sub_8048A36(v1);
  free(v1);
  free(v0);
}
```
接着看
```
char *read_fromuser()
{
  int v0; // eax
  char buf; // [esp+13h] [ebp-215h]
  int v3; // [esp+14h] [ebp-214h]
  ssize_t v4; // [esp+18h] [ebp-210h]
  char s[512]; // [esp+1Ch] [ebp-20Ch]
  unsigned int v6; // [esp+21Ch] [ebp-Ch]

  v6 = __readgsdword(0x14u);
  v3 = 0;
  while ( 1 )
  {
    v4 = read(0, &buf, 1u);
    if ( v4 < 0 )
      break;
    if ( v4 )
    {
      v0 = v3++;
      s[v0] = buf;
      if ( v3 <= 3 || s[v3 - 1] != 10 || s[v3 - 2] != 13 || s[v3 - 3] != 10 || s[v3 - 4] != 13 )
        continue;
    }
    goto LABEL_11;
  }
  perror("read");
LABEL_11:
  s[v3] = 0;
  if ( sub_804893E(s) )
    return 0;
  if ( s[0] )
    return strdup(s);
  return 0;
}
```
不断读入字符串，保证字符串最后四个字节为\r\n\r\n就可以执行到LABEL_11位置
```
signed int __cdecl sub_804893E(const char *a1)
{
  const char *format; // [esp+18h] [ebp-230h]
  char *formata; // [esp+18h] [ebp-230h]
  char v4; // [esp+1Ch] [ebp-22Ch]
  char command; // [esp+3Ch] [ebp-20Ch]
  unsigned int v6; // [esp+23Ch] [ebp-Ch]

  v6 = __readgsdword(0x14u);
  format = strstr(a1, "User-Agent: ");
  if ( !format )
    return 0;
  __isoc99_sscanf(format, "User-Agent: %32s\r\n", &v4);
  printf(format);
  if ( !jude((int)&v4) )
    return 0;
  formata = strstr(a1, "token: ");
  if ( !formata )
    return 0;
  __isoc99_sscanf(formata, "token: %512s\r\n", &command);
  system(&command);
  return 1;
}
```
关键看judge
```
signed int __cdecl sub_80488DD(int a1)
{
  signed int i; // [esp+18h] [ebp-10h]
  signed int v3; // [esp+1Ch] [ebp-Ch]

  v3 = strlen(s);
  for ( i = 0; i < v3; ++i )
  {
    if ( (i ^ *(char *)(i + a1)) != s[i] )
      return 0;
  }
  return 1;
}
```
所以useragent满足这个条件就可以执行token后面的代码了