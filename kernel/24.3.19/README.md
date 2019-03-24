## 函數分析
baby_ioctl函數的內容如下：
```
signed __int64 __fastcall baby_ioctl(__int64 a1, attr *a2)
{
  attr *v2; // rdx
  signed __int64 result; // rax
  int i; // [rsp-5Ch] [rbp-5Ch]
  attr *v5; // [rsp-58h] [rbp-58h]

  _fentry__(a1, a2);
  v5 = v2;
  if ( (_DWORD)a2 == 0x6666 )
  {
    printk("Your flag is at %px! But I don't think you know it's content\n", flag);
    result = 0LL;
  }
  else if ( (_DWORD)a2 == 0x1337
         && !_chk_range_not_ok((__int64)v2, 16LL, *(_QWORD *)(__readgsqword((unsigned __int64)&current_task) + 4952))
         && !_chk_range_not_ok(
               v5->flag_str,
               SLODWORD(v5->flag_len),
               *(_QWORD *)(__readgsqword((unsigned __int64)&current_task) + 4952))
         && LODWORD(v5->flag_len) == strlen(flag) )
  {
    for ( i = 0; i < strlen(flag); ++i )
    {
      if ( *(_BYTE *)(v5->flag_str + i) != flag[i] )
        return 0x16LL;
    }
    printk("Looks like the flag is not a secret anymore. So here is it %s\n", flag);
    result = 0LL;
  }
  else
  {
    result = 0xELL;
  }
  return result;
}
```
_chk_range_not_ok的檢查檢查指針是否來自用戶空間，分析文件可以知道用戶輸入的結構爲
```
struct _input
{
	char *flag;
	size_t len;
};
```
3個判斷爲
1. 輸入數據是否爲用戶態
2. 輸入數據中的指針是否只想用戶態
3. 輸入數據中的長度是否等於內核中的flag的長度
## 解答
當ioctl傳入0x6666的時候可以會的flag的位置，當ioctl傳入ioctl傳入的時候經過了3個判斷，然後用傳入的flag判斷和內核中的flag是否相等，相等則輸出falg，這時創建競爭條件，另外啓動一個線程，不斷的更改flag的值，如果在判斷之後可以更改掉傳入的flag，則可以實現輸出flag
## 其他方法
將等待爆破的字節放在mmap申請的內存頁末尾，此時下一個字節位於不可讀寫的用戶態空間，當得到正確的一字節時，內核會比較用戶空間內下一字節的正確性，由於該地址是不可讀取的，將導致kernel panic，從而可以判斷是否爆破的一個字節正確。