## 文件解析
给定了3个文件

* rootfs.cpio：文件
* bzImage：系统映像
* boot.sh：启动脚本

进入rootfs.cpio，打开init脚本，这是系统的init进程，发现其加载了babydriver模块，在、lib目录下可以找到该模块，使用IDA反汇编这个文件，可以得到主逻辑。
## 思路
没有用户态传统的溢出等漏洞，但存在一个伪条件竞争引发的 UAF 漏洞。也就是说如果我们同时打开两个设备，第二次会覆盖第一次分配的空间，因为 babydev_struct 是全局的。同样，如果释放第一个，那么第二个其实是被是释放过得，这样就造成了一个 UAF。可以修改 cred 来提权到 root。
cred的大小可以通过阅读源码得到，也可以通过编译一个内核模块来查看写一个模块
```
#include <linux/init.h>
#include <linux/module.h>
#include <linux/cred.h>

MODULE_LICENSE("Dual BSD/GPL");
static int hello_init(void){    
    printk(KERN_ALERT "sizeof cred: %d", sizeof(struct cred));    
    return 0;
}
static void hello_exit(void){
    printk(KERN_ALERT "exit module!");}
    module_init(hello_init);module_exit(hello_exit);
｝
```
覆盖前0x8a的直接为0，则uid，guid就被覆盖为0，为root
具体代码可以看exp.c