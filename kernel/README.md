# 內核PWN基礎知識
這裏是個人在學習linux kernel pwn中遇到的一些基礎知識，做一個簡單的總結
## 內核PWN文件
### bzImage
內核壓縮文件，內核中其他格式文件可以看[這裏](https://unix.stackexchange.com/questions/5518/what-is-the-difference-between-the-following-kernel-makefile-terms-vmlinux-vml) 
### rootfs.cpio
文件系統映像，提取.cpio文件方式
```
mkdir ./tmp
cd ./tmp
cp ../.cpio *.cpio.gz 
gunzip *.cpio.gz  #會得到一個*.cpio文件
cpio -idm *.cpio.gz #最終在/tmp目錄下會解壓出所有的內容，-d表示會自行建立目錄，-m表示不更改時間戳
```
當完成exp編寫之後，需要將新的exp打包到cpio文件中，這樣新啓動的系統中才會包含利用代碼
```
find . | cpio -o --format=newc > rootfs.cpio
```
### boot.sh
啓動腳本
```
./boot.sh
```
### vmlinux
静态编译，未经过压缩的 kernel 文件，可以用來提取gadget，如果題目沒有給出，可以使用extract-vmlinux來解壓，extract-vmlinux是linux/script中的一個腳本
```
./extract-vmlinux ./bzImage > vmlinux
```
## 內核符號
### /proc/kallsyms和System.map
kallsyms抽取了内核用到的所有函数地址(全局的、静态的)和非栈数据变量地址，生成一个数据块，類似與System.map，System.map是磁盘中真实存在的文件，存储内核中静态编译的函数和变量地址，每个新编译内核对应一个System.map文件，当klogd输出内核消息时，会通过/boot/System.map来将函数、变量地址转换为名称，方便用户理解。该文件对应不同的编译内核有对应的实现文件。**區別在於kallsyms是動態的，包含了增加模塊的符號**
### /proc/kallsyms的內容
内核提供控制变量 /proc/sys/kernel/kptr_restrict 来进行修改
kptr_restrict = 2	内核将符号地址打印为全0, root和普通用户都没有权限
kptr_restrict = 1	root用户有权限读取, 普通用户没有权限
kptr_restrict = 0	root和普通用户都可以读取
/proc/kallsyms的文件格式如下：
地址		類型		名稱
### 通過讀取/proc/kallsyms獲得符號信息
假設現在可以讀取/proc/kallsyms文件，簡單一段程序來讀取需要函數的地址，用來做ROP
```
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

int main(){
        FILE* fd = fopen("/proc/kallsyms","r");
        char buffer[100]={0};
        while(fgets(buffer,100,fd)){
                if(strstr(buffer,"commit_creds") || strstr(buffer,"prepare_kernel_cred")){
                        printf("%s\n",buffer);
                        char addr[20] = {0};
                        strncpy(addr,buffer,16);
                        //printf("%s\n",addr);
                        size_t t = 0;
                        sscanf(addr,"%llx",&t);
                        printf("%p\n",t);
                        return 0;
                }
        }
        return 0;
}
```
然後編寫Makefile文件
以上的例子獲得了commit_creds函數在內核中的地址，
但是如果要做ROP，則還需要知道vmlinux文件被加載到哪個地方，通過pwntools可以得到commit_creds函數距離vmlinux頭的距離
```
vmlinux = ELF("./vmlinux")
dis = hex(vmlinux.sym['commit_creds'] - 0xffffffff81000000)
```
Linux 内核的物理基址 - 0x1000000;(16M)
Linux 内核的虚拟基址 - 0xffffffff81000000.
所以，最後vmlinux在內核中的虛擬地址應該是
```
vmlinux_base = commit_creds - dis;
```
### 日誌
/proc/kmsg文件保存了内核从最开始启动到正常运行时的所有内核输出消息，是内核在运行过程中通过printk输出的，如果klogd启动，klogd读取/proc/kmsg文件的内容，然后通过syslogd程序，写到/var/log/messages文件中，当然，syslogd可以通过syslogd.conf文件进行配置。利用dmesg，其实也是读取/proc/kmsg文件内容，然后显示到终端。dmesg和klogd都是利用了System.map文件将内核地址转化为对应的函数名称，方便用户调试
/proc/sys/kernel/dmesg_restrict，此切换指示是否禁止无特权用户使用dmesg(8)查看内核日志缓冲区中的消息。当dmesg_restricted设置为(0)时，没有限制。当dmesg_restricted设置为(1)时，用户必须使用CAP_SYSLOG才能使用dmesg(8)。
## 內核模塊編寫
以經典的hellowrld的模塊爲例子，具體含義就不介紹了，可以參考《linux設備驅動程序》，編寫c語言模塊代碼hello.c：
```
#include <linux/init.h>
#include <linux/module.h>
MODULE_LICENSE("Dual BSD/GPL");
static int hello_init(void)
{
        printk(KERN_ALERT "Hello, world\n");
        return 0;
}
static void hello_exit(void)
{
        printk(KERN_ALERT "Goodbye, cruel world\n");
}
module_init(hello_init);
module_exit(hello_exit);
```
編寫MakeFfile文件：
```
obj-m := hello.o
all:
        make -C /lib/modules/$(shell uname -r)/build M=$(PWD) modules
clean:
        make -C /lib/modules/$(shell uname -r)/build M=$(PWD) clean
```
在當前目錄下會生成helloc.ko文件
裝載模塊：
```
insmod hello.ko
```
卸載模塊：
```
rmmod hello.ko
```
## gadget尋找
x86和x64的參數傳遞規則如下：
x86：函数参数在函数返回地址的上方
x64：System V AMD64 ABI (Linux、FreeBSD、macOS 等采用) 中前六个整型或指针参数依次保存在 RDI, RSI, RDX, RCX, R8 和 R9 寄存器中，如果还有更多的参数的话才会保存在栈上。内存地址不能大于 0x00007FFFFFFFFFFF，6 个字节长度，否则会抛出异常。
### ropper
使用規則如下：
```
$ ropper --file <afile> --semantic "<any constraint>"
```
生成文件之後直接在文件中尋找關鍵字就可以了
## gdb調試
qemu 内置有 gdb 的接口，即可以通过 -gdb tcp:port 或者 -s 来开启调试端口
另外通过 gdb ./vmlinux 启动时，虽然加载了 kernel 的符号表，但没有加载驱动 *.ko 的符号表，可以通过 add-symbol-file *.ko textaddr 加载
比如以21.2.19這個例子來說，通過下面的命令來啓動內核：
```
gdb ./vmlinux -q
```
通過下面的命令加載core.ko的符號表：
```
add-symbol-file ./core.ko 0xffffffffc018b000
```
其中0xffffffffc018b000這個地址需要在qemu中獲得，在這個例子中，更改init進程，修改啓動時/bin/sh的setuidgid數值爲0，這樣/bin/sh啓動的時候就是root權限，可以通過觀察/sys/modules/core/section/.text來得到core.ko在系統中的代碼段地址：
```
/ # cat /sys/module/core/sections/.text 
```
接着在下斷點，可以使用符號來下斷點，也可以使用內存地址來下斷點：
```
pwndbg> b core_read
pwndbg> b *(0xffffffffc018b000+0xCC)
```
啓動遠程連接：
```
target remote localhost:1234
```



