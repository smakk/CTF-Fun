## 內核gadget尋找
使用ropper：
```
ropper --file ./vmlinux --nocolor > g1
```
使用ROPgadget：
```
ROPgadget --binary ./vmlinux > g2
```
如果沒有vmlinux，使用extract-vmlinux腳本（文件位於linux內核目錄linux/scripts/extract-vmlinux下）先提取出vmlinux：
```
./extract-vmlinux ./bzImage > vmlinux
```
## 啓動
修改了start.sh的-m選項，設置未128M
刪除了init中定時關機的設置腳本
## 解析
在init文件中，將/proc/kallsyms放到了/tmp/kallsyms中，可以讀取到內核函數地址
增加了模塊core.ko，應該是漏洞存在的地方
core.ko中存在這樣的問題：
1. init_module() 注册了 /proc/core
2. exit_core() 删除 /proc/core
3. core_ioctl() 定义了三条命令，分别调用 core_read()，core_copy_func() 和设置全局变量 off
4. core_read() 从 v4[off] 拷贝 64 个字节到用户空间，但要注意的是全局变量 off 使我们能够控制的，因此可以合理的控制 off 来 leak canary 和一些地址
5. core_copy_func() 从全局变量 name 中拷贝数据到局部变量中，长度是由我们指定的，当要注意的是 qmemcpy 用的是 unsigned __int16，但传递的长度是 signed __int64，因此如果控制传入的长度为 0xffffffffffff0000|(0x100) 等值，就可以栈溢出了
6. core_write() 向全局变量 name 上写，这样通过 core_write() 和 core_copy_func() 就可以控制 ropchain 了
## 解答
通过 ioctl 设置 off，然后通过 core_read() leak 出 canary
通过 core_write() 向 name 写，构造 ropchain
通过 core_copy_func() 从 name 向局部变量上写，通过设置合理的长度和 canary 进行 rop
通过 rop 执行 commit_creds(prepare_kernel_cred(0))
返回用户态，通过 system("/bin/sh") 等起 shell
## 總結
### /proc/kallsyms
kallsyms抽取了内核用到的所有函数地址(全局的、静态的)和非栈数据变量地址，生成一个数据块，類似與System.map，System.map是磁盘中真实存在的文件，存储内核中静态编译的函数和变量地址，每个新编译内核对应一个System.map文件，当klogd输出内核消息时，会通过/boot/System.map来将函数、变量地址转换为名称，方便用户理解。该文件对应不同的编译内核有对应的实现文件。**區別在於kallsyms是動態的，包含了增加模塊的符號**
内核提供控制变量 /proc/sys/kernel/kptr_restrict 来进行修改
kptr_restrict = 2	内核将符号地址打印为全0, root和普通用户都没有权限
kptr_restrict = 1	root用户有权限读取, 普通用户没有权限
kptr_restrict = 0	root和普通用户都可以读取
/proc/kallsyms的文件格式如下：
地址			類型			名稱
### 內核函數
proc_create：
remove_proc_entry：
commit_creds(prepare_kernel_cred(0))：其中，prepare_kernel_cred()创建一个新的cred，参数为0则将cred中的uid, gid设置为0，对应于root用户。随后，commit_creds()将这个cred应用于当前进程。此时，进程便提升到了root权限。这些方法的地址，可以通过/proc/kallsyms获取。不过，有时为了安全，管理员会隐藏内核符号的地址，此时便无法通过这一方式获取地址。