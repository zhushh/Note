查看主机内部的信息
----

```
cat /proc/cpuinfo
less /proc/cpuinfo
lspci
lscpu
```
长按super键可以查看有哪些快捷键

一 基础命令操作
----

man : 用来查询指令；

man [man] : 可以用来查看man的使用方法；

man -f [man] : 显示那些跟man有关的说明文件
```
   可用于查找文件的说明（很方便哦）
   man page的使用：(以man date为例)
   最顶部的一行为： DATE(1)   User Commands       Date(1)
        其中Date(1) 的数字1表示：用户在shell环境中可以操作的命令或可执行文件
        另有：
            3 —— 一些常用的function与library，大部分为C的函数库(library)
            4 —— 设备文件说明，通常在/dev下的文件
            5 —— 配置文件或者是某些文件的格式
            8 —— 系统管理员可用的管理命令
            9 —— 跟kernel有关的文件
   关键字的查找：
       /string :
   向下查询string
       ？string :向上查询string
        n, N: 上一页或下一页（相对而言）
        q : 退出man page
```

man -k [man] : 把含有man的关键字的说明文件都列出来

/usr/share/doc 目录：许多说明文件文档的储存库

nano [filename] : 创建或打开filename文件，并使用nano文本编辑器进行编辑；

date : 时间显示；

date +%H:%M : 显示小时：分钟；

date +%Y/%m/%d : 显示年月日（2010/09/21格式）；

cal [年份] : 显示所选年份的日历表；

cal [月份] [年份] : 显示所选年份的所选月份的月历；

cal : 显示当前的时间，用月历的方式；

info : 类似于man的操作；

who : 显示当前在线用户；

bc : 进入计算器界面，可进加减乘除取余(%)，指(^)数等运算

whatis [命令或者是数据] ： 等价于 man -f [命令或者数据]；

apropos [命令或者数据] : 相当于 man -k [命令或者数据]；

ps -aux: 查看后台执行的程序；

netstat -a: 查看网络的联机状态；

sync : 将数据同步写入硬盘中；

shutdown : 关机命令
```
$ shutdown -h now   # 立即关机；
$ shutdown -h 20:25     # 今天20：25关机或者明天20：25关机(今天已过20：25)；
$ shutdown -h +10   # 十分钟后关机；
$ shutdown -r now   # 系统立即重启；
$ shutdown -r +30 'The system will reboot'  # 30分钟后重启并通知所有用户后面的消息；
$ shutdown -k now 'This system will reboot'     # 仅发出警告并不关机；
```

reboot, halt, poweroff : 重启，关机

init : 切换系统运作模式；(0-关机， 3-纯命令行模式， 5-含图形界面，6-重启)；

su - 账户名 ： 切换账户；(su - shuhuang)

二 文件属性与权限有关
----

chgrp : 改变文件所属用户组
```
   chgrp [-R] dirname/filename ...(e.g: chgrp shuhuang file1);
```

chown : 改变文件所有者
```
    chown [-R] 帐号名称 文件或目录
    chown [-R] 帐号名称：组名 文件或目录
    另外，chown还可以改变文件或目录的用户组：
    $ chown user:group filename 或者 chown user.group filename
    仅改变用户组：
    $ chown .group filename
```

chmod : 改变文件的权限
```
    chmod [-R] xyz 文件或者目录
    参数：
        xyz : 数字类型的权限(rwx属性数值的相加)；
        -R ：进行递归的持续更改（同目录下的所有子目录）
    字符型：(u-user, g-group, o-others, a-all)
    chmod u=rwx,go=rx .bashrc (符号类型改变权限)
    chmod a+r .bashrc (所有人属性加r)
```

1) 权限对文件的重要性：
```
**************************************************
* r | 可读取此文件的实际内容
**************************************************
* w | 可编辑，新增或修改该文件的内容
**************************************************
* x | 该文件具有被执行的权限
**************************************************
```

2) 权限对目录的重要性：
```
******************************************************************************
* r | 具有读取目录树结构链表的权限，如查询文件名数据
******************************************************************************
* w | 更改该目录结构链表的权限，如新建，删除，重命名，转移文件或目录
******************************************************************************
* x | 代表用户是否可以进入该目录，没有此权限就进入不了该目录，就什么的都没法做～
******************************************************************************
```

dos2unix: 把windows的文件转换成unix文件
```
$ dos2unix < dosFilename > unixFilename
```

unix2dos: 把unix的文件转换成windows的文件 
```
$ unix2dos < unixFilename > dosFilename
```

三 文件与目录管理
----

cd :
```
cd [相对路径或绝对路径]
cd ~ : 回到主目录;
cd .. : 回到上层；
cd - : 回到刚才目录；
```

pwd :
```
pwd [-P]
参数：
    -P ： 当前路径，而非连接路径
```

mkdir :
```
mkdir [-mp] 目录名称
参数：
   -m : 配置文件权限；
   -p : help递归创建；
```

rmdir:
```
rmdir [-p] 目录名称
参数：
   -p : 连上层的空目录也删除；
```

echo $PATH : 显示目前路径；

ls :
```
参数：
    -a : 全部文件，包含隐藏；
    -d : 进列出目录本身，不列出目录内的文件数据；
    -h : 文件容量用易读方式(GB，KB)表示；
    -i : 列出文件所占用的inode号码
    -l : 列出长数据串，包含文件属性与权限等数据；
```

cp :
```
参数：
    -a : 相当与pdr;
    -i : 若目标文件存在时询问；
    -r : 递归复制（用于目录）；
    -v : 显示出正在copy的文件
```

rm :
```
参数：
    -f : force;
    -r : 递归删除，最常用的目录删除；
```

mv : 移动目录/文件/更名

rename : 更改大量文件的文件名，还支持正则表达式

cat : 显示文件内容
```
-n : 列出行号(cat -n filename)
```

tac : 反向显示
```
tac /filename
```

nl : 显示文件内容(顺便标出行号)
```
参数：
(-b, -n, -w)
```


more : 查看文件内容
```
操作：
space : 向下翻一页；
Enter : 向下滚一行；
/string : 向下搜索"string";
q : quit;
b/ ^b : 往回翻页
```

less : 查看文件内容
```
操作：
space : 向下翻一页
PageDown :
PageUp :
/string : search "string"
n : 向前一个查询
N ： 向后一个查询
q ： quit
```

head : 
```
head [-n number] filename
参数：
    -n : 后面接数字，代表显示几行的意思
```

tail : 
```
tail [-n number] filename
参数：
-n : 后面接数字，代表显示几行
```

od : 显示二进制文件
```
od [-t TYPE] filename
参数：
t : 后面可接类型：
    a ： 默认字符输出
    c ： 使用ASCII字符输出
    d[size] : 10进制输出
    f[size] : flaoting输出
    o[size] : octal输出
    x[size] : 十六进制输出
```

touch :
```
touch [-acdmt] filename
参数:
-a : 仅修改访问时间
-c : 修改文件时间，若文件不在则新建文件
-d : --date="时间或日期"; (touch -d "2 days ago" filename)
-m : 仅修改mtime；
-t : 后面可接欲修改的时间，而不用目前时间，格式[YYMMDDhhmm]
```

umask : 查看文件默认权限(用户在新建文件活目录时的权限默认值),显示的权限要取反

umask -S : 文件权限的字符类型输出

chattr : change file attributes
```
    chattr [+-=][ASacdistu] 文件或目录
    + : 增加某一个特殊参数
    - : 删除某一个特殊参数
    = : 仅有后面的参数
        a : 文件只能增加数据，不能删除和修改数据(root)
        i : 不能被改名/删除/设置连接/写入/添加数据等等(root)
        c : 自动将文件压缩，在读取时自动解压缩
        d : 当dump程序执行时设置d属性的文件不会被dump备份
        s : 文件被删除时，它将会完全从这个硬盘空间被删除
```

lsattr : list file attributes
```
    lsattr [-adR] 文件或目录
    -a : 隐藏文件的属性也秀出来
    -d : 仅列出目录本身属性
    -R : 连同子目录数据也一并列出
```

SUID, SGID, SBIT:
```
    说明:
    SUID的限制和功能:(出现在文件所有者的x权限位置)
        1.SUID仅对二进制程序有效(shell script也没有)
        2.执行者对该程序有X(可执行)的权限
        3.本权限仅在执行该程序的过程中有效
        4.执行者将具有该程序所有者的权限
        e.g.
            shuhuang@shuhuang:~$ ls -ld /tmp; ls -l /usr/bin/passwd
            # 此时passwd这个程序就具有s的属性

    SGID的功能:(出现在文件用户组的x权限位置)
        1.SGID对二进制程序有用
        2.执行者对于该程序来说，需要具备x的权限
        3.执行者在执行的过程将会获得该程序的用户组的支持
        若SGID使用在目录上，即该目录设置了SGID权限:
            1.用户若具有r和x的权限时，该用户能够进入此目录
            2.用户在此目录下的有效用户组将会变成该目录的用户组
            3.若用户在该目录下具有w(新建文件)的权限，则用户所创建的新文件的用户组与此目录相同
        e.g.
            shuhuang@shuhuang:~$ ll /usr/bin/locate /var/lib/mlocate/mlocate.db # /usr/bin/locate 具有s属性在用户组的x位置
    SBIT(Sticky Bit)仅对目录有效:
        当用户对于此目录具有w，x权限时，即具有写入的权限时:
        若用户在该目录下新建文件或目录，仅有自己和root才有权利删除该文件
    设置操作:
    SUID/SGID/SBIT 的设置：使用chmod命令在"三个数字"的组合的前面在加一个数子设置即可
    其中: 4 表示设置SUID，2 表示设置SGID， 1 表示设置SBIT
    e.g.
        shuhuang@shuhuang:~$ chmod 4755 filename
```

file : 查看文件基本数据
which : (脚本文件名的查询)
```
    which [-a] command
    -a : 将所有由PATH目录中可以找到的命令均列出
```

whereis : (文件名的查找)
```
    whereis [-bmsu] filename/directory
    -b : 只找二进制文件
    -m : 只找说明文件manual路径下的文件
    -s : 只找source源文件
    -u : 查找非上述文件的其他特殊文件
```

locate : (有时需更新数据库)
```
    locate [-ir] keyword
    -i : 忽略大小的差异
    -r : 后面可接正则表达式
```

updatedb : 更新数据库

find : 
```
    find [PATH] [option] [action]
    1 与时间有关参数：
        -atime, -ctime, -mtime
        -mtime n : n为数字，查找n天之前一天内被更改过的文件
            例如：-mtime 4 寻找的就是从4-5天内的文件名
        -mtime +n : 列出n天之前（不含n）被更改过的文件
        -mtime -n : 列出n天之内（含n）被更改过的文件
        -newer file : file为存在文件，列出比file还要新的文件
    2 与用户组有关的参数：
        -uid n : n为数字（用户帐号的ID，即UID，记录在/etc/passwd的与帐号名称相对应的数字）
        -gid n : n为数字（用户组的ID，即GID）
        -user name : name为帐号名称
        -group name : name为用户组名
        -nouser : 寻找文件所有者不存在/etc/passwd的人
        -nogroup : 寻找用户组不存在/etc/group中的文件
    3 与文件权限有关的参数：
        -name filename : 查找文件名为filename的文件
        -size [+-]SIZE : 查找比SIZE还要大(+)或小(-)的文件。
            c : 代表byte， k : 代表1024bytes
        -type TYPE : 查找文件的类型为TYPE；
        -perm mode : 查找文件属性等于"mode"的文件，mode为类似chmod的属性值(e.g 4755)
        perm -mode : 查找文件权限"必须全部包括mode的权限"的文件
        perm +mode : 查找文件权限"包含任一mode的权限"的文件
        e.g.
            shuhuang@shuhuang:~$ find /home/shuhuang/* -perm 644
            # 查找文件权限值为 644 的文件
            shuhuang@shuhuang:~# find / -perm 4000 
            # 查找具有 SUID 限制的文件
            shuhuang@shuhuang:~# find / -perm 2000 
            # 查找具有SGID 限制的目录或程序
    4 其他可进行的操作:
        -exec command : command为其他命令(不能是链接命令)，-exec后面可再接其他命令来处理查找到的结果
            e.g. 
            shuhuang@shuhuang~$ find / -perm +7000 -exec ls -l {} \;
            从 -exec 到 \; 是关键字，{}表示由find找到的内容，find的结果会被放置到{}中。
        -print : 将结果打印到屏幕上（默认操作）
        此外，find还可以使用通配符，如：*
    5 命令行应用：
      把当前目录下所有的shell脚本都新增可执行权限
      $ chmod a+x `find -name "*.sh"`
      
      查找当前目录下，所有以.cpp结尾的文件例子
      $ find ./ -name "*.cpp"
      
      如果想指定目录查找，比如在/data/home/zhushh/code下面查找.cpp结尾文件：
      $ find /data/home/zhushh/code -name "*.cpp"
      
      查找文件名为album的文件或目录，当前目录./默认是可以不用写的：
      $ find ./ -name "album"
      $ find -name "album"
      
      与xargs命令一起使用，搜索文件内容包含某字段的地方，比如搜索"album" 或者"process"字段：
      $ find -name "*.cpp" | xargs grep "album"
      $ find -name "*.h" | xargs grep "process"
```

四 磁盘与文件系统管理
----

dumpe2fs : 查看文件系统
```
    dumpe2fs [-bh] 设备文件名
    -h : 仅列出superblock的数据，不列出其他的区段
```

df : 列出文件系统的整体磁盘使用量，可将系统内的所有文件系统列出来
```
    df [-ahikHTm] [目录或文件名]
    -h : 以人们较易阅读的(GB, MB, KB)等格式列出
    -i : 不用硬盘容量，而以inode的数量显示
```

du : 评估文件系统使用量
```
    du [-ahskm] 文件或目录的名称
    -s : 列出总量
    -k : 以KB的容量显示
    -m : 以MB的容量显示
```

ln : 设置链接文件
```
    ln sourcefilename objectfilename (硬连接)
    ln -s 源文件 目标文件 (软连接)
```

fdisk : 处理disk partition table
```
    fdisk [-l] 设备名称
    -l：列出设备后面的所有分区内容
    m : print this menu
    d : delete a partition
    n : add a new partition
    q : quit without saving changes
    w : write table to disk and exit(一般write之后用partprobe更新分区表)
    p : print the partition table
```

fdisk -l : 查阅系统目前所有的分区

partprobe : 更新分区表

mkfs:   磁盘格式化
```
    mkfs [-t 文件系统格式] 设备文件名
    -t : 可以接受的文件系统格式
```

mke2fs：    磁盘格式化
```
    mke2fs [-b block_size] [-i block_size] [-L 卷标] [-cj] 设备
    -b : 每个block的大小
    -i : 每个inode的容量
    -L : 接卷标名称
    -j : 主动加入journal成为ext3格式
```

fsck:   磁盘检验
```
    fsck [-t 文件系统] [-ACay] 设备名称
```

mount:  文件挂载
```
    mount -a
    mount [-l]
    mount [-t 文件系统] [-L Label名] [-o 额外选项] [-n] 设备文件名 挂载点
        -a : 依照/etc/fstab 的数据将所有未挂载的磁盘都挂载上来
        -l : 单纯出入mount会显示目前挂载的信息，加上-l可增加列Lable名称
        -L : 系统除了利用设备名称之外，还可以利用文件系统的卷标名称来挂载
        -o : 后面接一些需要挂载时额外的参数（如帐号/密码/读写权限等）
        ro, rw :  挂载的文件系统成为只读/读写
        async, sync: 此文件系统是否使用同步（sync）或异步（async）写入内存机制
        auto, noauto: 允许此分区被mount -a 自动挂载
        dev, nodev: 是否允许此分区可创建设备文件
        exec, noexec: 是否允许此分区上拥有可执行binary文件
        defaults : 默认值rw, suid, dev, exec, auto, nouser, and async
        remount : 重新挂载
    如果想要挂在U盘时，可以先使用命令fdisk -l查看U盘设备文件名来挂在
```

/etc/fstab 文件:
```
    该文件是开机挂载的文件，可将外部设备的信息写在里面，以后每次开机都可以自动挂载
```

umount:     文件卸载
```
    umount [-fn] 设备文件名或挂载点
    -f : 强制卸载
    -n : 不更新/etc/mtab的情况下卸载
```

blkid: 查看设备文件的UUID和TYPE
```
    blkid 设备文件名
    e.g:
        使用root账号直接在命令行下面直接输入: blkid
```

mknod:
```
    mknod 设备文件名 [bcp] [Major] [Minor]
    b : 设备名称成为一个外部存储设备，如硬盘
    c : 设备名称成为一个外部输入设备，如鼠标，键盘等
    p : 设备名称成为一个FIFO文件
    Major : 主设备代码(可用 ll /dev/sda*查看或者ll /dev/hdc*)
    Minor : 次设备代码(可用 ll /dev/sda*查看或者ll /dev/hdc*)
        e.g.
        shuhuang@shuhuang:~$ ll /dev/sda*
        brwxr----- 1 root disk 22, 0 Oct 24 15:33 /dev/sda1
        brwxr----- 1 root disk 22, 1 Oct 20 13:10 /dev/sda2
        ...
        brwxr----- 1 root disk 22, 6 Oct 20 13:20 /dev/sda7
        上面的disk后面的22和0-6就是主代码和此代码
```

e2label:    修改卷标
```
    e2label 设备名称 新的label名称
```

tune2fs:
```
    tune2fs [-jlL] 设备代号
    -l: 类似dumpe2fs -h 的功能(读取super block内的数据)
    -j: ext2转成ext3
    -L: 类似e2label的功能，修改文件系统的Label
```

hdparm:
```
    -T : 测试暂存区(cache)的访问性能
    -t : 测试硬盘的实际访问性能
    i.e. ~$ hdparm /dev/sda
```

dd if=/dev/zero of=filename bs=1M count=512
```
    if: input file, /dev/zero是会一直输出0的设备
    of: output file, 将一堆0写入到后面接的文件中
    bs: 每个block的大小，就像文件系统那样的block
    count: bs的数量
```

mkswap:     创建swap文件
```
    mkswap filename
```

swapon:     启动swap文件
```
    swapon filename
```

swapoff:    关掉swap file
```
    swapoff filename
```

du -sb filename:    列出文件的大小(bytes为单位, 更接近所占用的实际大小)

du -sm filename:    列出文件的大小(MB为单位, 更接近实际分配的内存大小)

parted:     分区命令
```
    parted [设备] [命令 [参数]]
    命令功能：
        新增分区:   mkpart [primary | logical | extended ] [ext3 | vfat] 开始 结束
        分区表:    print
        删除分区:   rm [partition]
        example:
        # parted /dev/hdc print
        # parted /dev/hdc mkpart logical ext3 19.2GB 19.7GB
        # parted /dev/hdc rm 8(删除/dev/hdc8)
```

五 文件与文件系统的压缩与打包
----

compress:
```
    压缩: compress [-rcv] filename/directory
    解压缩: uncompress filename.Z
        -r: 同目录下的文件也同时给予压缩
        -c: 将压缩数据输出成为standard output（输出到屏幕）
        -v: 显示压缩后的一些信息以及压缩过程中的一些文件名的变化
```

gzip:
```
    gzip [-cdtv#] filename
        -c: 压缩内容输出到屏幕上              (gzip -c filename)
        -d: 解压缩                            (gzip -d filename.gz)
        -t: 检验一个压缩文件的一致性，看文件有无错误
        -v: 显示原文件/压缩文件比等信息       (gzip -v filename)
        -#: '#'为数字1~9,速度逐减,压缩比逐增  (gzip -9 -c filename)
    zcat: 查看压缩文件的内容
        zcat filename.gz
```

bzip2:
```
    bzip2 [-cdkzv#] filename
        -c: 输出到屏幕        (bzip2 -c filename)
        -d: 解压缩            (bzip2 -d filename.bz2)
        -k: 保留原文件不删除原始文件
        -z: 压缩的参数        (bzip2 -z filename)
        -v: 显示原文件/压缩文件的压缩比等信息
        -#: 与gzip同样的      (bzip2 -9 -c filename > filename.bz2)
    bzcat: 查看压缩文件的内容
        bzcat filename.bz2
```

tar: 
```
    打包与压缩: tar [-j|-z] [cv] [-f newfilename] filename
    查看文件名: tar [-j|-z] [tv] [-f newfilename]
    解压缩:    tar [-j|-z] [xv] [-f newfilename] [-C 目录]
    -c: 新建打包文件，可搭配-v查看过程中被打包的文件名
    -t: 查看打包文件的内容含有哪些文件名，重点查看文件名
    -x: 解打包/压缩的功能，可搭配-C在特定的目录中解开
    -j: 通过bzip2的支持进行压缩/解压缩，文件名最好为*.tar.bz2
    -z: 通过gzip的支持进行压缩/解压缩，此时文件名最好为*.tar.gz
    -v: 显示正在处理的文件
    -C 目录: 用在解压缩时，若要在特定的目录解压缩，可以使用这个参数
    -p: 保留备份数据的原本权限和属性，常用于备份-c重要的配置文件
    -P(大写): 保留绝对路径
    --exclude=FILE： 压缩过程中不要将FILE打包
        example：
        # tar -jcv -f filename.tar.bz2 filename
        # tar -jtv -f filename.tar.bz2
        # tar -xjv -f filename.tar.bz2 -C directory
        # tar zcvf directory.tar.gz directory
        # tar zxvf directory.tar.gz
```

dump:   完整备份整个文件系统
```
    dump [-Suvj] [-level] [-f 备份文件] 待备份数据
    dump -W
    -S: 仅列出后面的待备份数据需要多少空间才能够备份完毕
    -u: 这次的dump时间记录到/etc/dumpdates文件中
    -v: 将dump的文件过程显示出来
    -j: 加入bzip2的支持，将数据进行压缩，默认bzip2的压缩等级为2
    -level: -0 ~ -9的等级
    -f: 类似tar后面接的产生文件
    -W: 列出/etc/fstab里面的具有dump设置的分区是否有备份过
```

restore:    恢复备份文件
```
    restore -t [-f dumpfile] [-h]
    restore -C [-f dumpfile] [-D 挂载点]
    restore -i [-f dumpfile]
    restore -r [-f dumpfile]
    -t: 查看dump起来的备份文件含有什么重要数据，类似tar -t功能
    -C: 比较dump与实际文件
    -i: 进入互动模式，可以仅还原部分文件，用于dump还原时(进入模式后可用help查询帮助)
    -r: 将整个文件系统还原
    -h: 查看完整备份数据中的inode与文件系统label等信息
    -D: 与-C进行搭配，可以查出后面接的挂载点与dump的不同的文件
    -f: 后面接需要处理的dump文件
```

dd: 备份整块分区或磁盘
```
    dd if="input file" of="output file" bs="block size" count="number"
    if : 就是inputfile，也可是设备
    of : output file, 也可以是设备
    bs : 规划一个block的大小，默认是512bytes
    count : 多少个block
    e.g.
        shuhuang@shuhuang:~$ dd if=/dev/zero of=/home/shuhuang/test bs=4k count=3
```

cpio:
```
    cpio -ovcB > [file | device]
    cpio -ivcdu < [file | device]
    cpio -ivct < [file | device]
    备份时的参数:
    -o : 将数据copy输出到文件或设备上
    -B : 改变默认的block，（大文件的储存速度加快）
    还原时的参数:
    -i : 将数据自文件或设备复制到系统当中
    -d : 自动新建目录
    -u : 自动将比较新的文件覆盖较旧的文件
    -t : 需配合-i参数，可用在查看cpio新建的文件或设备的内容
    -v : 显示存储过程中的文件名
    -c : 一种较新的portable format放式存储
```

dos2UNIX:   windows和linux文件转换
```
    dos2UNIX [-kn] file [newfile]
    -k : 把dos文件转成linux下的文件
```

六 认识与学习bash
----

type: 查看外部命令与内置命令
```
    type [-tpa] name
    -t : 显示字眼(file, alias, builtin)
    -p : 外部命令显示完整名
    -a : PATH变量定义中，显示所有含有name的命令
```

\(反斜杠): 表示转义

echo: 变量的显示(显示变量前需要有'$'符号)
```
    echo $variable
    echo ${variable}
```

变量的设置规则:
```
    1 变量与变量内容用等号链接("name=shuhuang")
    2 等号两边不能直接接空格("name = shuhuang"错误)
    3 变量名只能是英文字母和数字(数字不能开头)
    4 变量内容若有空格,则使用单引号或双引号(单引号内的特殊字符被转化成ASCII,双引号则保留原本字符属性)
    5 转义字符可将特殊字符转成一般字符(纯文本)
    6 命令里面包含其他命令,可用反单与引号(`命令`)或“$(命令)”
    7 若想增加变量内容,使用"$变量名称"或"${变量名称}"
    8 若变量需要在其他子程序执行,需要用export使变量变成环境变量
    9 系统默认变量为大写,自行设置变量可以使用小写
    10 取消变量的方法是"unset 变量名称"("unset name")
```

env: 查看环境变量与常见环境变量说明
```
    HOME : 用户主文件夹
    SHELL : 目前使用的shell是那个程序,默认/bin/bash
    HISTSIZE : 与历史命令有关,曾经执行过的命令的最大条数
    MAIL : 使用mail命令在收信时系统会读取的邮件信箱文件
    PATH : 文件查找路径(:分隔)
    LANG : 语系数据,
    RANDOM : 随机数值
```

set: 查看所有变量（环境变量和自定义变量）
```
    PS1 : 提示符设置
        \d : 显示星期月日 ("Mon Feb 2")
        \H : 完整主机名
        \h : 取主机名第一个小数点之前的名字("www.shuhuang.tsai"的"www")
        \t : 显示时间(24h, "HH:MM:SS")
        \T : 显示时间(12h, "HH:MM:SS")
        \A : 显示时间(24h, "HH:MM")
        \@ : 显示时间(12h, "HH:MM")
        \U : 目前用户帐号名称
        \w : 完整工作目录名称（主文件夹用'~'代替）
        \W : 仅列出工作目录最后一个名称
        \# : 执行第几个命令
        \$ : 提示符(root为'#'其他'$')
```

$:   当前shell的线程代号，即所谓的PID(PID号码)  (echo $$)
?:   上个命令你执行的回传码(命令执行成功回传0)  (echo $?)

export:    自定义变量转成环境变量
```
    子程序仅会继承父程序的环境变量,不会继承父程序的自定义变量
    export variable
```

read:
```
    read [-pt] variable
        -p : 后面可以接提示符
        -t : 后面可以接等待的秒数
```

declare/typeset:
```
    declare [-aixr] variable
        -a : 把variable定义为数组类型
        -i : integer
        -x : variable变成环境变量(declare +x variable 取消variable是环境变量)
        -r : variable设置为readonly,不能更改内容
        -p : 可以单独列出变量类型
        说明:
            变量的默认类型是"字符串"("1+2"为字符串，不是数值3)
                $sum=1+2               (sum 是字符串 1+2)
                $declare -i sum=1+2    (sum 是数字 3)
            bash的数值运算默认最多为整数类型(1/3=0)
```

ulimit:     限制参数
```
    ulimit [-SHacdflut] [配额]
        -H : hard limit,必不能够超过的数值
        -S : soft limit,警告设置,可以超过，但有警告信息
        -a : 后不接参数，列出所有的限制额度
        -c : 限制每个内核文件的最大容量
        -f : 此shell可以创建的最大容量，单位为KB
        -d : 进程可以使用的最大断裂内存(segment)容量
        -l : 可用于锁定(lock)的最大容量
```

变量相关:
```
${variable#关键字}              删除从头开始符合"关键字"的最短数据
${variable##关键字}             删除从头开始符合"关键字"的最长数据
${variable%关键字}              删除从尾向前符合"关键字"的最短数据
${variable%%关键字}             删除从尾开始符合"关键字"的最长数据
${variable/旧字符串/新字符串}   第一个符合旧字符串被新字符串替换
${variable//旧字符串/新字符串}  全部符合旧字符串的内容被新字符串替换

变量存在的判断：
#################################################################
#   ~$ echo $username
#        <<没有任何输出，可能为空变量，可能不存在
#   ~$ username=${username-root}
#   ~$ echo $username
# root    <<被赋值为root
#   ~$ username="shu huang"
#   ~$ username=${username-value}
#   ~$ echo $variable
# shu huang   <<没有被改变值，因为username现在是存在的变量
#   ~$ username=""
#   ~$ username=${username-root}
#   ~$ echo $username
#        <<空变量也不会被改变值
#   ~$
##################################################################
    说明:'-'符号，若variable不存在,则新声明variable,并赋值为value(value可以自己设置)

若username未设置或者为空字符串，则将username内容设置为root
#######################################################################
#  shuhuang@shuhuang:~$ username=""
#  shuhuang@shuhuang:~$ username=${username-root}
#  shuhuang@shuhuang:~$ echo $username
#        <<username被设置为空字符串所以保留空字符串
#  shuhuang@shuhuang:~$ username=${username:-root}
#  shuhuang@shuhuang:~$ echo $username
#  root  <<加上":"后，若变量内容为空或者未设置，都能够以后面的内容替换
########################################################################
```

history:    历史命令查看
```
    history [n]
    history [-c]
    history [-raw] histfiles
参数：
n   : 数字，是要列出最近n条命令的意思
-c  : 将目前shell中的所有history内容全部消除
-a  : 将目前新增的history命令新增入histfiles中，若没有加histfiles，则默认写入 ～/.bash_history
-r  : 将目前histfiles的内容读到目前这个shell的history记忆中
-w  : 将目前的history记忆内容写入到histfiles中

!number:    执行第几条命令的意思
!command:   由最近的命令开头向前搜寻命令串开头为command的那个命令，并执行；
!!:         就是执行上一个命令（相当于按 向上箭头，再按Enter）
```

bash登录与显示信息的编辑：  /etc/issue，/etc/motd
```
编辑/etc/issue的内容即可修改登录bash的界面，相关参数如下：
###############################################
# \d    本地端的时间和日期
# \l    显示第几个终端机接口
# \m    显示硬件的等级
# \n    显示主机网络名称
# \o    显示domain name
# \r    操作系统的版本(相当于uname -r)
# \t    显示本地端时间的时间
# \s    操作系统的名称
# \v    操作系统的版本
###############################################
```

bash的环境配置文件：
```
- login shell：取得bash时需要完整的登录流程，e.g. tty1～tty6登录，需要帐号和密码，此时取得的bash称login shell
- non-login shell：取得bash接口的方法不需要重复登录的举动，如以X Window登录后，再以X的图形界面启动终端机，此时
- 那个终端接口并没有需要再次输入帐号与密码，那个bash则称为non-login shell。在bash环境下再次使用bash这个命令，
- 同样没有输入密码和帐号，所以也是属于non-login shell。
```

source 配置文件名： 将配置文件的设置读入目前的bash环境中。(或者小数点". 配置文件")

stty,set:
```
    stty -a:    列出所有按键与按键内容
    说明:
        eof:    End of file
        erase:  向后删除字符
        intr:   送出一个interrupt的信号给当前正在运行的程序
        kill:   删除在目前命令行上的所有文字
        quit:   送出一个quit信号给目前正在有运行的程序
        start:  在某个进程停止后，重新启动它的输出
        stop:   停止目前屏幕的输出
        susp:   送出一个terminal stop的信号给正在运行的进程
    e.g.想要设置[ctrl]+h来进行字符的删除：
        shuhuang@shuhuang:~$ stty erase ^h
    
    set [-uvCHhmBx]
    说明:
        -u  默认不启用，若启用后，当使用未设置变量时会显示错误信息
        -v  默认不启用，若启用后，在讯息被输出前会显示信息的原始内容
        -x  默认不启用，若启用后，命令被执行前会显示命令内容（前面有++）
            -h  默认启用，与历史命令有关
        -H  默认启用，与历史命令有关
        -m  默认启用，与工作管理有关
        -B  默认启用，与括号[]的作用有关
        -C  默认不启用，使用 > 等时，若文件存在，该文件不会被覆盖
```

bash默认热键组合：
```
    Ctrl+C:     终止目前的命令
    Ctrl+D:     输入EOF
    Ctrl+M:     就是Enter
    Ctrl+S:     暂停屏幕的输出
    Ctrl+Q:     回复屏幕的输出
    Ctrl+U:     在提示符下，将整行命令删除
    Ctrl+Z:     暂停目前的命令
```

通配符与特殊符号：
```
    *       代表0～无穷多个任意字符
    ？      代表一定有一个任意字符
    []      代表一定有一个括号内的字符，如[abcd]表示一定有一个字符是a/b/c/d
    [-]     代表在编码顺序内的所有字符，如[0-9]表示0-9之间的所有数字
    [^]     代表一定有一个非括号内的字符，如[^abc]表示！[abc]
```

数据流重定向：
```
    file  ---standard input--->  command  ---standard output---> file/device
                                    |
                                standard error
                                    |
                                file/device
    stdin: 代码为0，使用< 或 <<
    stdout: 代码为1，使用 > 或 >>
    stderr: 代码为2，使用 2> 或 2>>
    e.g
    ************************************************
    * shuhuang@shuhuang:~$ ll / > ~/rootfile
    * **********************************************
    步骤：
        1.该文件(~/rootfile)若不存在，系统会自动将他创建起来
        2.当该文件存在时，系统会将这个文件内容清空，然后再将数据写入
        3.也就是若以 > 输出到一个已存在的文件，那么这个文件就会被覆盖掉
        4.如果不想覆盖掉文件，可以使用 >>, 此时数据会被附加到文件末尾
    e.g:
     1. ***************************************
        * shuhuang@shuhuang:~$ cat > catfile
        ***************************************
            此时键盘的输入就会被输出到catfile文件，(按ctrl+d结束)
     2. **************************************************
        * shuhuang@shuhuang:~$ cat > catfile < ~/.bashrc
        **************************************************
            此时catfile文件的输入就是～/.bashrc文件，相当于copy
     3. **************************************************
        * shuhuang@shuhuang:~$ cat > catfile << "eof"
        **************************************************
        此时键盘的输入的内容就是catfile的内容，直到输入字符串"eof"时才结束输入。(此时不需要ctrl+d)
```

特殊符号说明(;,&&,||):
```
    ';':    cmd; cmd;...
    '&&':   cmd1 && cmd2 ...
    '||':   cmd1 || cmd2 ...
```

管道命令(pipe):
```
    ***********************************************
    * shuhuang@shuhuang:~$ ls -al /etc | less
    ***********************************************
    执行了ls -al /etc 命令后把输出到屏幕的数据流重新输入到less命令中，这样就可以使用less方便地查看输出
```

选取命令：cut, grep
```
    cut -d '分隔字符' -f fields
    cut -c 字符范围
    e.g:
        shuhuang@shuhuang:~$ echo $PATH | cut -d ':' -f 3
        # 以':'为分隔符，取第3段内容
        shuhuang@shuhuang:~$ echo $PATH | cut -d ':' -f 3,5
        # 以':'为分隔符，取第3，5段内容
        shuhuang@shuhuang:~$ export | cut -c 12-
        # 取第12列(包括12)之后的所有内容

    grep [-acinv] [--color=auto] '查找字符串' filename
        -a:     将binary文件以text文件的方式查找数据
        -c:     计算找到'查找字符串'的次数
        -i:     忽略大小写的不同
        -n:     顺便输出行号
        -v:     反向选择，显示没有包含查找字符串的行
        --color:可以把查找到的关键字部分加上颜色显示
    e.g:
        shuhuang@shuhuang:~$ last | grep 'root'
        shuhuang@shuhuang:~$ last | grep -v 'root'
        shuhuang@shuhuang:~$ grep --color=auto 'MANPATH' /etc/man.config
```

sort:
```
    sort [-fbMmrtuk] [file or stdin]
    -f:     忽略大小写差异
    -b:     忽略最前面空格部分
    -M:     以月份的名字来排序
    -n:     纯数字排序
    -r:     反向排序
    -u:     相同的数据中只显示一行(uniq)
    -t:     分隔符，默认是tab
    -k:     以那个区间来排序
    e.g:
        shuhuang@shuhuang:~$ cat /etc/passwd | sort
        shuhuang@shuhuang:~$ cat /etc/passwd | sort -t ':' -k 3
        shuhuang@shuhuang:~$ cat /etc/passwd | sort -t ':' -k 3 -n
        shuhuang@shuhuang:~$ last | cut -d ' ' -f 1 | sort
```

uniq:
```
    uniq [-ic]
    -i:     忽略大小写字符的不同
    -c:     进行计数
    e.g:
        shuhuang@shuhuang:~$ last | cut -d ' ' -f 1 | sort | uniq
        shuhuang@shuhuang:~$ last | cut -d ' ' -f 1 | sort | uniq -c
```

wc:
```
    wc [-lwm]
    -l:     仅列出行
    -w:     仅列出多少字
    -m:     多少个字符
    e.g:
        shuhuang@shuhuang:~$ cat /etc/man.config | wc
        shuhuang@shuhuang:~$ last | grep [a-zA-Z] | grep -v 'wtmp' | wc -l
```

tee: 双向重定向
```
    standard input  --->  tee  --->  Screen
                           |
                         file
    tee [-a] file
    -a:     累加的方式将数据加入file中
    e.g:
        shuhuang@shuhuang:~$ last | tee last.list | cut -d " " -f 1
        shuhuang@shuhuang:~$ ls -l /home | tee ~/homefile | more
        shuhuang@shuhuang:~$ ls -l / | tee -a ~/homefile | more
```


#####文件内容处理:

tr [-ds] SET1 ...
```
    -d:     删除信息当中的SET1这个字符串
    -s:     替换掉重复的字符
        shuhuang@shuhuang:~$ last | tr '[a-z]' '[A-Z]'
        shuhuang@shuhuang:~$ cat /etc/passwd | tr -d ':'
        shuhuang@shuhuang:~$ cp /etc/passwd /home/passwd && UNIX2dos /home/passwd
        shuhuang@shuhuang:~$ cat /home/passwd | tr -d '\r' > /home/passwd.linux
```

col [-xb]
```
    -x:     将tab键转换成对等的空格
    -b:     在文字内有反斜杠时，仅保留反斜杠最后接的那个字符
```

join [-ti12] file1 file2
```
    -t:     join默认以空格分隔数据，并且对比“第一个字段”的数据，
        如果两个文件相同，则将两条数据连成一行，且第一个字段放在第一个
    -i:     忽略大小写差异
    -1:     后面接数字，代表第一个文件要用哪个字段来分析
    -2:     后面接数字，代表第二个文件要用哪个字段来分析
        shuhuang@shuhuang:~$ head -n 3 /etc/passwd /etc/shadow
        shuhuang@shuhuang:~$ join -t ':' /etc/passwd /etc/shadow
        shuhuang@shuhuang:~$ join -t ':' -1 4 /etc/passwd -2 3 /etc/group
```

paste [-d] file1 file2
```
    -d:     后面可以接分隔字符，默认以tab分隔
    -:      如果file部分写成-，表示来自standard input的数据
        shuhuang@shuhuang:~$ paste /etc/passwd /etc/shadow
```

expand [-t] file
```
    -t:     后面接数字，一般一个tab用8个空格替换，我们可以自定义一个tab按键代表多少个字符
        shuhuang@shuhuang:~$ grep '^MANPATH' /etc/man.config | head -n 3 | expand -t 6 - | cat -A
```

split:  文件分割
```
    split [-bl] file PREFIX
    -b:     后面接欲切割成文件的大小，可加单位，例如b，k，m等
    -l:     以行数来进行切割
    PREFIX: 代表前导符，可作为切割文件的前导文字
```

正则表达式：
```
    [:alnum:]       代表英文大小写字符及数字(0-9,a-z,A-Z)
    [:alpha:]       代表任何英文大小写字符(a-z,A-Z)
    [:blank:]       代表空格键或tab键
    [:cntrl:]       代表键盘上的控制键(CR, LF, Tab, Del)
    [:digit:]       代表数字(0-9)
    [:graph:]       代表除了空格符之外的所有字符
    [:lower:]       代表小写字符
    [:upper:]       代表大写字符
    [:print:]       任何可以被打印出来的字符
    [:punct:]       任何标点符号(punctuation symbol),即(",'?!:;#$)
    [:space:]       任何产生空白的字符(含Tab, CR)
    [:xdigit:]      十六进制数字(0-9,A-F,a-f)

    ^word           待查找字符串word在行首                              grep -n '^#' regular_express.txt
    word$           待查找字符串在行尾                                  grep -n '!$' regular_express.txt
    .(point)        代表一定有一个任意字符                              grep -n 'e.e' regular_express.txt
    \               转义字符，去除特殊符号的特殊意义                    grep -n \' regular_express.txt
    *               重复0-无穷多个的前一个字符                          grep -n 'ess*' regular_express.txt
    [list]          从字符集合的RE字符里面找出想要选取的字符            grep -n 'g[ld]' regular_express.txt
    [n1-n2]         从字符集合里选取想要的字符范围                      grep -n '[0-9]' regular_express.txt
    [^list]         从字符集合的RE字符里找出不要的字符串或范围          grep -n 'oo[^t]' regular_express.txt
    \{n,m\}         连续n到m个前一个RE字符，若为\{n\}则是连续前n个的前一个RE字符，若为\{n,\}则表示前n个以上的前一个RE字符
```

扩展正则表达式：
```
    +       重复一个或以上的前一个RE字符
    ？      0或1个前一个RE字符
    |       用或(or)的方式找出数个字符串
    ()      找出“组”字符串(里面字符串用|分开)
    ()+     多个重复组的判别
```

grep高级:
```
    grep [-A] [-B] [-n] [--color=auto] '搜寻字符' filename
    -A:     后面可加数字，为after，除了该行以外，后续n(n为数字)行也列出来
    -B:     后面可加数字，为before,列出该行及之前n行
    -n:     显示行号
    --color:    可将正确的那个选取数据列出颜色
```

sed:    stream editor
```
    sed [-nefr] [action]
    -n:     使用silent模式，一般会输出到屏幕上，加上-n不会有输出到screen
    -e:     直接在命令行模式上进行sed的动作编辑(默认)
    -f:     直接将sed的动作写在一个文件内， -f filename 则可执行filename内的sed动作
    -r:     支持扩展正则表达式
    -i:     直接修改读取的文件内容，而不是由屏幕输出（注意是直接修改源文件）
    action:
        [n1[,n2]]function
        n1,n2:      代表选择进行动作的行数,如："10,20[动作行为]"
        function参数：
            a:  新增，a后面可接字符串
            c:  替换，c后面可接字符串，这些字符串会替换n1，n2之间的行
            d:  删除，
            i:  插入
            p:  打印(通常和sed -n一起)
            s:  替换(可搭配正则表达式)
    e.g:
        shuhuang@shuhuang:~$ nl /etc/passwd | sed '2,5d'
        shuhuang@shuhuang:~$ nl /etc/passwd | sed '2d'
        shuhuang@shuhuang:~$ nl /etc/passwd | sed '3,$d'
        shuhuang@shuhuang:~$ nl /etc/passwd | sed '2a drink tea'
        shuhuang@shuhuang:~$ nl /etc/passwd | sed '2a drink tea ...... \
        > drink beer ?'
        shuhuang@shuhuang:~$ nl /etc/passwd | sed '2,5c No 2-5 number'
        shuhuang@shuhuang:~$ nl /etc/passwd | sed -n '5,7p'
        shuhuang@shuhuang:~$ ifconfig   (先查看一下)
        shuhuang@shuhuang:~$ ifconfig | grep 'inet addr' | sed 's/^.*addr//g' | cut -d ' ' -f 1 (获取ip地址)
        shuhuang@shuhaung:~$ cat /etc/manpath.config | grep 'MAN' | sed 's/#.*$//g' | sed '/^$/d'
```

printf: 类似C语言的printf

awk:    数据处理工具
```
    awk '条件类型1 {action1} 条件类型2 {action2} ...' filename
    每一行的每一个字段都有变量名称，分别为: $1, $2, $3, ......以此类推，$0代表一整行的数据
    NF  表示每一行($0)拥有的字段总数
    NR  目前awk所处理的是第几行的数据,e.g: shuhuang@shuhuang:~$ last -n 5 | awk '{print $1 "\tlines: " NR "\tcolumes: " NF}'
    FS  目前分隔字符，默认是空格键，如: shuhuang@shuhuang:~$ cat /etc/passwd | awk '{FS=':'} $3 < 10 {print $1}'
    BEGIN   开始条件, 如：  shuhuang@shuhuang:~$ cat /etc/passwd | awk 'BEGIN {FS=':'} $3 < 10 {print $1}'
    END     结束条件
    变量可以直接使用,如： total = $1 + $2 + $3
```

diff:   按行文件比较
```
    diff [-bBi] from-file to-file
    from-file:      作为欲比较文件的文件名
    to-file:        作为目的比较文件的文件名
    frome-file and to-file can be replaced by '-' which stands for "standard input"
    -b:     忽略一行中仅有多个空白的区别
    -B:     忽略空白行的区别
    -i:     忽略大小写的不同
```

cmp:    按字节文件比较
```
    cmp [-s] file1 file2
    -s:     将所有的不同点的字节处都列出来(默认仅列出第一个发现的不同)
```

test:   真值表达式测试
```
    文件类型相关:  test -e filename
    -e filename:    该文件名是否存在
    -f filename:    该文件名是否存在且为文件(file)
    -d filename:    该文件名是否存在且为目录(directory)
    -b filename:    改文件名是否存在且为一个block device
    -c filename:    该文件名是否存在且为一个character device
    -S filename:    该文件名是否存在且为一个Socket文件
    -p filename:    该文件名是否存在且为一个FIFO(pipe)文件
    -L filename:    该文件名是否存在且为一个链接文件

    文件权限相关:  test -r filename
    -r filename:    检测该文件名存在且具有可读的权限
    -w filename:    检测该文件名存在且具有可写的权限
    -x filename:    检测该文件名存在且具有可执行的权限
    -u filename:    检测该文件名存在且具有"SUID"的属性
    -g filename:    检测改文件名存在且具有"SGID"的属性
    -k filename:    检测该文件名存在且具有"Sticky bit"的属性
    -s filename:    检测该文件名存在且为非空文件

    文件比较: test file1 -nt file2
    -nt(newer than)     判断file1是否比file2新
    -ot(older than)     判断file1是否比file2旧
    -ef(equal file)     判断file1和file2是否为同一文件

    两个整数之间的判断: test n1 -eq n2
    -eq     两个整数n1和n2是否相等
    -nq     两个整数不相等
    -gt     大于
    -lt     小于
    -ge     大于等于
    -le     小于等于

    判定字符串数据:
    test -z string      判断字符串是否为0，即空字符串
    test -n string      判断字符串是否为非0
    test str1 = str2    判断str1 是否等于 str2
    test str1 != str2   判断不相等

    多重判断: -a  -o  !
    test -r filename -a -x filename     同时判断是否具有可读和可写的权限
    test -r file -o -x file
    test ! -x file                      当file不具有x权限时，回传true
```


七 Linux 帐号管理与 ACL权限设置
----

/etc/passwd:
```
    1.每一行代表一个帐号
    2.用':'作为分隔符，共7段，分别为:
        帐号名称，
        密码: 0表示管理员，1-499是系统管理帐号，之后的是可登录帐号
        UID，
        GID，
        用户信息说明，
        主文件夹，
        Shell
```

/etc/shadow:
```
    1.与/etc/passwd的行相对应
    2.每段如下:
        帐号名称，
        密码，
        最近更动密码的日期: 就是最近修改密码的日期(数字为天数，1970.1.1为数字1开始累加)
        密码不可被修改的日期(相对于最近更动的日期): 距离上次修改几天后才能重新修改密码，0表示任何时候都可以
        密码需要修改的天数(相对于最近更动的日期): 距离上次几天之内需要再次重新修改密码，否则密码过期
        密码需要修改期限前的警告天数(相对于第五字段相比): 密码过期前多少天发出提醒
        密码过期后的帐号宽限时间(密码失效日): 密码过期了之后的宽限天数还可以修改密码(此时用户还可以登录)
        帐号失效日期:   此时用户的密码将不能登录也不能重新修改，必须找管理员帮忙~~
```

修改密码的命令: passwd

/etc/group:(':'分隔，共四列)
```
    1.用户组名称
    2.用户组密码
    3.GID
    4.此用户组支持的帐号名称
    有效用户组(effective group)与初始用户组(initial group)
        /etc/passwd第四段的GID就是初始用户组
```

/etc/gshadow:
```
    1.用户组名
    2.密码列，开头为！表示无合法密码，所以无用户组管理员
    3.用户组管理员帐号
    4.该用户组的所属帐号
```

groups: 显示当前有效与支持的用户组(第一个显示的为有效用户组)

newgp:
```
    newgp 用户组
    有效用户组的切换(此时shell也会变成新用户组的shell，可以使用exit返回原来的shell)
```

useradd:
```
    useradd [-u UID] [-g initial group name] [-G 次要用户组] [-mM] [-c 说明栏] [-d 主文件夹绝对路径] [-s shell] 用户帐号名
    -u:     后接UID，直接指定一个特定的UID帐号给这个帐号
    -g:     后接用户组名，设置为初始用户组
    -G:     后面接的组名是这个帐号还可以加入的用户组
    -M:     强制，不要创建用户主文件夹(系统帐号默认)
    -m:     强制，要创建用户主文件夹(一般帐号默认)
    -c:     /etc/passwd第五列说明内容
    -d:     指定某个目录成为主文件夹
    -r:     创建一个系统帐号(UID会有限制，参考/etc/login.defs)
    -s:     后接一个shell，默认/bin/bash
    -e:     后面接一个日期"YYYY-MM-DD"，帐号失效日的设置
    -f:     后面接shadow第七字段，指定密码是否会失效，0为立刻失效，-1为永远不失效
    e.g.
        shuhuang@shuhuang:~# useradd zhuzhu
        shuhuang@shuhuang:~# passwd zhuzhu  (设置密码)

        shuhuang@shuhuang:~# useradd -u 1010 -g shuhuang zhuzhu
        shuhuang@shuhuang:~# ll -d /home/zhuzhu
        shuhuang@shuhuang:~# useradd -r test    (创建系统帐号)
        shuhuang@shuhuang:~# grep test /etc/passwd /etc/shadow /etc/group
    useradd 参考文件:
        shuhuang@shuhuang:~# useradd -D
        # 说明：
        GROUP=100           <== 默认的用户组
        HOME=/home          <== 默认主文件夹所在目录
        INACTIVE=-1         <== 密码失效日，在shadow内的第七列
        EXPIRE=             <== 帐号失效日，在shadow内的第8列
        SHELL=/bin/bash     <== 默认的shell
        SKEL=/etc/skel      <== 用户主文件夹的内容参考目录
        CREATE_MAIL_SPOOL=yes       <== 是否主动帮用户创建邮箱(mailbox)
```

passwd:
```
    passwd [--stdin]        <== 所有用户均可使用
    passwd [-l] [-u] [--stdin] [-S] [-n 日数] [-x 日数] [-w 日数] [-i 日期] 帐号    <== root功能
    --stdin:    通过前一个管道的数据作为密码输入，对shell script有帮助
    -l:         是lock的意思，会将/etc/shadow第二列前面加上'!'使密码失效
    -u:         与-l相对，unlock
    -S:         列出密码相关
    -n:         后接天数，shadow的第四段，多久不可能修改密码天数
    -x:         后接天数，shadow的第五段，多久内必须改动密码
    -w:         后接天数，shadow的第六段，密码过期前的警告天数
    -i:         后接日期，shadow的第七段，密码失效日期
```

chage:
```
    chage [-ldEImMW] 帐号名
    -l:     列出该帐号的详细密码参数
    -d:     后接日期，修改shadow的第三字段(最近一次更改日期)，格式YYYY-MM-DD
    -E:     后接日期，修改shadow的第八字段(帐号失效日期)，格式YYYY-MM-DD
    -I:     后接天数，修改shadow的第七字段(密码失效日期)，
    -m:     后接天数，修改shadow的第四字段(密码最短保留天数)
    -M:     后接天数，修改shadow的第五字段(密码多久需要进行修改)
    -W:     后接天数，修改shadow的第六字段(密码过期前警告日期)
    e.g.
        shuhuang@shuhuang:~$ useradd test
        shuhuang@shuhuang:~$ echo "test" | passwd --stdin test
        shuhuang@shuhuang:~$ chage -d 0 test
        # test这个帐号在第一次登录后必须修改密码，然后以新密码重新登录
```

usermod:
```
    usermod [-cdegGlsuLU] username
    -c:     后接帐号的说明，即/etc/passwd的第五列
    -d:     后接帐号主文件夹，即修改/etc/passwd第六字段
    -e:     后接日期，格式YYYY-MM-DD，即/etc/shadow的第八字段
    -f:     后接天数，为shadow第七字段
    -g:     后接初始用户组，修改/etc/passwd第四字段(GID)
    -G:     后接次要用户组，修改这个用户能够支持的用户组
    -a:     与-G合用，可增加次要用户组的支持而非设置
    -l:     后接帐号名称，/etc/passwd的第一列
    -s:     后接Shell 的实际文件，
    -u:     后接UID，
    -L:     暂时冻结用户密码，无法登录
    -U:     解冻
    e.g.
        shuhuang@shuhuang:~# useradd username
        shuhuang@shuhuang:~# echo "123456" | passwd --stdin username
        shuhuang@shuhuang:~# usermod -c "Shuhuang's test'" username
        shuhaung@shuhuang:~# usermod -e "2015-12-13" username
        shuhuang@shuhuang:~# grep username /etc/shadow

        shuhuang@shuhuang:~# ll -d ~username
        shuhuang@shuhuang:~# cp -a /etc/skel /home/username
        shuhuang@shuhuang:~# chown -R username:username /home/username      (-R 递归修改)
        shuhuang@shuhuang:~# chmod 700 /home/username
        shuhuang@shuhuang:~# ll -a ~username
```

userdel:
```
    userdel [-r] username
    -r:     连通用户的主文件夹也一起删除
```

finger:     user information lookup program
```
    finger [-s] username
    -s:     仅列出用户的帐号，全名，终端机代号和登录时间等
```

chfn:       change real user name and infomation
```
    chfn [-foph] [帐号名]
    -f:     后面接完整的大名
    -o:     你办公室的房间号码
    -p:     办公室的电话号码
    -h:     家里的电话号码
```

chsh:       change loin shell
```
    chsh [-ls]
    -l:     列出系统上目前可以使用的shell
    -s:     设置自己的shell
    e.g.
        shuhuang@shuhuang:~$ chsh -l
        shuhuang@shuhuang:~$ chsh -s /bin/csh
```

id:     print real user effective user and group IDs
```
    id [username]
    e.g.    shuhuang@shuhuang:~$ id
```

groupadd:
```
    groupadd [-g gid] [-r] 用户组名
    -g:     设置gid号码
    -r:     新建系统用户组
    shuhuang@shuhuang:~# groupadd group1; grep group1 /etc/group /etc/gshadow
```

groupmod:
```
    groupmod [-g gid] [-n group_name] 用户组名
    e.g.
        shuhuang@shuhuang:~$ groupmod -g 201 -n mygroup group1; grep mygroup /etc/group /etc/gshadow
```

groupdel:
```
    groupdel [groupname]
    e.g.
        shuhuang@shuhuang:~$ groupdel mygroup
    注意:   只能删除/etc/passwd文件内不存在的group，否则就要连那个用户帐号也一起删除，或者修改那个帐号的GID
```

gpasswd:
```
    gpasswd groupname
    gpasswd [-A user1, user2, ...] [-M user3, ...] groupname
    gpasswd [-rR] groupname
    -A:     后面的账户将成为用户组管理员
    -M:     将后面的帐号加入该用户组
    -r:     将groupname的密码删除
    -R:     让groupname的密码失效

    用户组管理员的操作
    gpasswd [-ad] user groupname
    -a:     将user加入到group中
    -d:     将user从用户组中删除

    e.g:
        shuhuang@shuhuang:~# groupadd testgroup
        shuhuang@shuhuang:~# gpasswd testgroup
        shuhuang@shuhuang:~# gpasswd -A shuhuang testgroup; grep testgroup /etc/group /etc/gshadow
```

#### ACL(Access control list)的使用:

setfacl: 设置某个文件/目录的ACL规定
```
    setfacl [-bkRd] [{-m | -x} acl paramater] dest_filename
    -m:     设置后续的acl参数给文件使用，不可与-x合用
    -x:     删除后续的acl参数，不可与-m合用
    -b:     删除所有的acl设置参数
    -k:     删除默认的acl参数
    -R:     递归设置acl，亦即包括子目录都会被设置起来
    -d:     设置默认acl参数，只对目录有效，在该目录新建的数据会引用此默认值
    e.g.
        shuhuang@shuhuang:~$ touch acl_test
        shuhuang@shuhuang:~$ ll acl_test
        shuhuang@shuhuang:~$ setfacl -m u:zhuzhu:rwx acl_test
        shuhuang@shuhuang:~$ ll acl_test
        # 利用 "u:用户名:权限" 来设置
        # 权限部分多了一个'+'，且与原本的权限会有区别
        
        shuhuang@shuhuang:~$ setfacl -m u::rwx acl_test
        # 上面是设置该文件所有者
        
        shuhuang@shuhuang:~$ setfacl -m g:zhuzhu:rwx acl_test
        # 设置组 "g:用户组:权限"

        shuhuang@shuhuang:~$ setfacl -m m:rx acl_test
        # 设置mask "m:权限"
        # 设置有效权限mask，用户或组所设定的权限必须要存在于mask的权限设置范围内才有效
        # 比如acl_test 具有rwx权限范围，那么设置给zhuzhu的rx就都会有效
        # 但是如果acl_test 仅只有r权限范围，那么设置给zhuzhu的rx就只有r有效，x权限木有效果

        shuhuang@shuhuang:~$ setfacl -m d:u:zhuzhu:rx /srv/project
        # 设置默认权限 "d:[ug]:用户列表:[rwx]"
        # 加上d之后，在目录下新建的文件/目录又具有acl权限规定，否则没有

        shuhuang@shuhuang:~$ setfacl -b /srv/project
        # 删除所有acl设置
```

getfacl: 取得某个文件/目录的ACL设置项目
```
    getfacl filename
```

#####用户身份切换:

su:
```
    su [-ml] [-c command] [username]
    '-':    "su -"使用login-shell的变量方式来登录系统，没有在后面加上username则是切换为root
    -l:     与'-'类似，但后面需要加用户名
    -m:     表示使用目前的环境设置，不读取新用户的配置文件
    -c:     仅执行一次命令
    e.g.
        shuhuang@shuhuang:~$ su -
        shuhuang@shuhuang:~$ exit
        shuhuang@shuhuang:~$ su - -c "head -n 3 /etc/shadow"
```

扩展阅读一:Linux下 su命令与su - 命令有什么区别？

- su 是切换到其他用户，但是不切换环境变量（比如说那些export命令查看一下，就知道两个命令的区别了）

- su - 是完整的切换到一个用户环境


扩展阅读二:su和sudo的区别

- 由于su 对切换到超级权限用户root后，权限的无限制性，所以su并不能担任多个管理员所管理的系统。如果用su 来切换到超级用户来管理系统，也不能明确哪些工作是由哪个管理员进行的操作。特别是对于服务器的管理有多人参与管理时，最好是针对每个管理员的技术特长和管理范围，并且有针对性的下放给权限，并且约定其使用哪些工具来完成与其相关的工作，这时我们就有必要用到 sudo。

- 通过sudo，我们能把某些超级权限有针对性的下放，并且不需要普通用户知道root密码，所以sudo 相对于权限无限制性的su来说，还是比较安全的，所以sudo 也能被称为受限制的su ；另外sudo 是需要授权许可的，所以也被称为授权许可的su；

- sudo 执行命令的流程是当前用户切换到root（或其它指定切换到的用户），然后以root（或其它指定的切换到的用户）身份执行命令，执行完成后，直接退回到当前用户；而这些的前提是要通过sudo的配置文件/etc/sudoers来进行授权；

sudo:   /etc/sudoers

```
    sudo [-b] [-u new_username]
    -b:     将后面的命令让系统自行执行，而不与当前的shell产生影响
    -u:     后面接欲切换的用户，若没有username则表示切换为root
    e.g.
        shuhuang@shuhuang:~$ sudo -u zhuzhu touch /tmp/myzhuzhu
        shuhuang@shuhuang:~$ ll /tmp/myzhuzhu
        # 特别留意myzhuzhu这个文件是由zhuzhu所创建的
    sudo执行过程:
        1.系统于/etc/sudoers文件中查找该用户是否具有执行sudo的权限
        2.若用户具有可执行sudo的权限，便让用户输入密码来确认
        3.若密码正确则开始执行后续接的命令(root 执行sudo不需要密码)
        4.若欲切换的身份与执行者的身份相同，也不许要输入密码
```

visudo 与 /etc/sudoers
```
    1.单一用户可进行root所有命令与sudoers的语法
        /etc/sudoers 有如下一行
            root    ALL=(ALL)   ALL
        或者
            root    ALL=(ALL:ALL)   ALL
        那么，若新加入:
            shuhuang    ALL=(ALL)   ALL
        就是说明shuhuang这个帐号可以使用sudo执行任何系统管理命令
        字段说明:
            1.账户名称
            2.登录者的来源主机名
            3.可切换的身份
            4.可执行的命令(命令使用绝对路径)
            ALL 表示任何身份
    2.利用用户组名及免密码的功能处理visudo
        /etc/sudoers 有如下一行
            %admin  ALL=(ALL)   ALL
            # 在最左边加上 %，后面接 groupname， 这样任何加入admin用户组的用户都可以执行root命令
        若是下面这样：
            %admin ALL=(ALL)    NOPASSWD:   ALL
            # 比上面多加了 NOPASSWD:，有了该关键字，就可以不需要输入密码
    3.有限制的操作命令
        shuhuang    ALL=(root)  !/usr/bin/passwd, /usr/bin/passwd [A-Za-z]*, !/usr/bin/passwd root
        # '!'表示不允许执行，'/usr/bin/passwd [A-Za-z]*'表示可以修改任意帐号的密码，但是最后限制了修改root密码
        # 此时shuhuang这个帐号就可以帮root管理帐号密码的修改～～
    4.通过别名设置visudo
        visudo的别名有:
            用户别名:   User_Alias
            命令别名:   Cmnd_Alias
            主机别名:   Host_Alias
        e.g.
            shuhuang@shuhuang:~# visudo
            User_Alias ADMPW = pro1, pro2, pro3, myuser1, myuser2
            Cmnd_Alias ADMPWCOM = !/usr/bin/passwd, /usr/bin/passwd [A-Za-z]*, !/usr/bin/passwd root
            ADMPW   ALL=(root)  ADMPWCOM
            # 如此设置之后，pro1，pro2，pro3，myuser1，myuser2就可以使用root的passwd管理其他人的密码
```

#### Linux 主机信息传递

w，who，last，lastlog:  查看当前登录者和最近登录者
```
    shuhuang@shuhuang:~$ w
    shuhuang@shuhuang:~$ who
    shuhuang@shuhuang:~$ last
    shuhuang@shuhuang:~$ lastlog
```

write, mesg, wall:      发送信息
```
    write username [terminal]
    # 前提是username 这个用户有开启接受mesg，开启命令是: shuhuang@shuhuang:~$ mesg y
    e.g.
        shuhuang@shuhuang:~$ who
        shuhuang@shuhuang:~$ write zhuzhu
        # 以ctrl+d结束
    mesg [y/n]
    e.g.
        shuhuang@shuhuang:~$ mesg y
        shuhuang@shuhuang:~$ mesg n
    wall
    e.g.
        shuhuang@shuhuang:~# wall "I will shutdown my linux server..."
```

mail:   邮件
```
    mail username
```

pwck:   检查/etc/passwd 帐号配置

grpck:  检查/etc/group 组帐号配置

pwconv: convert to and from shadow passwords and groups
```
    1.比较/etc/passwd 及/etc/shadow，若/etc/passwd的帐号并没有/etc/shadow密码对应时，
        pwconv会去/etc/login.defs取用相关的密码数据，并新建该帐号的/etc/shadow数据
    2.若/etc/passwd内存在加密后的密码数据时，则pwconv会将改密码列移动到/etc/shadow内，
        并将原本的/etc/passwd内相应的密码列变成x
```

pwuconv:
```
    1.将/etc/shadow内的密码数据列写回/etc/passwd并删除/etc/shadow文件
```

chpasswd:   update passwords in batch mode
```
    chpasswd -m username:password
    shuhuang@shuhuang:~$ echo "zhuzhu:12345" | chpasswd -m
```

特殊帐号的手工创建
```
    1.先新建所需要的用户组              (vi /etc/group)
    2.将/etc/group与/etc/gshadow同步    (grpconv)
    3.新建帐号的各个属性                (vi /etc/passwd)
    4.将/etc/passwd与/etc/shadow同步    (pwconv)
    5.新建该帐号的密码                  (passwd accountname)
    6.新建用户主文件夹                  (cp -a /etc/skel /home/accountname)
    7.更改用户主文件夹的属性            (chown -R accountname:group /home/accountname)
```

八 磁盘配额(quota)与高级文件系统管理
----

Quota:
```
    用途:
        1.针对WWW Server，限制每个人的网页的容量限制
        2.针对mail Server，每个人的邮件空间限制
        3.针对file Server，每个人最大的可用网络硬盘空间
        4.限制某一用户组所能使用的最大磁盘配额
        5.限制某一用户的最大磁盘配额
        6.以link方式使邮件可以作为限制的配额
    使用限制:
        1.仅能针对整个文件系统
        2.内核必须支持quota
        3.只对一般用户身份有效
    规范设置选项
        1.容量限制和文件数量限制(inode/blocks)
        2.soft/hard
            可以超过soft，但是有警告信息和处理磁盘的宽限时间，超过宽限时间则soft变成hard
            hard限制，超过后用户不能新建任何文件，因为已经没有磁盘空间可以使用
```

quotacheck:     扫描文件系统并新建quota配置文件
```
    quotacheck [-avgufM] [/mount_point]
    -a:     扫描所有在/etc/mtab内，含有quota支持的文件系统，此时mount_point可省略
    -u:     针对用户扫描文件与目录的使用情况，会建aquota.user
    -g:     针对用户组扫描文件与目录的使用情况，会建aquota.group
    -v:     显示扫描过程的信息
    -f:     强制扫描文件系统，并写入quota配置文件
    -M:     强制以读写的方式扫描文件系统，只有在特殊情况下才使用
    e.g.
        shuhuang@shuhuang:~$ quotacheck -augv
        # 若出现"quotacheck: Can't find filesystem to check or filesystem not mounted with quota"
        # 则说明此时没有任何文件系统启动quota支持
```

quota启动，关闭与限制设置:
```
    quotaon [-avgu]
    quotaon [-vug] [/mount_point]
    -u:     针对用户启动quota
    -g:     针对用户组启动quota
    -v:     显示启动过程相关信息
    -a:     根据/etc/mtab内的文件系统设置启动相关的quota，若没有加上-a则后面需要加特定的那个文件系统
    e.g.
        shuhuang@shuhuang:~$ quotaon -auvg
        # /dev/hda3 [/home]: group quotas turned on
        # /dev/hda3 [/home]: user quotas turned on
        shuhuang@shuhuang:~$ quotaon -uv /var
        # 启动/var 的user quota

    quotaoff [-a]
    quotaoff [-ug] [/mount_point]
    -a:     全部文件系统的quota都关闭
    -u:     仅针对mount_point 关闭user quota
    -g:     仅针对mount_point 关闭group quota

    edquota [-u username] [-g groupname]
    edquota -t          # 修改宽限时间
    edquota -p 范本帐号 -u 新帐号
    -u:     进入quota编辑界面设置username的限制值
    -g:     进入quota编辑界面取设置groupname的限制值
    -t:     可以修改限制时间
    -p:     复制范本，范本帐号是已存在并且已设置好的quota用户
    e.g.
        shuhuang@shuhuang:~$ edquota -u myquota1
        shuhuang@shuhuang:~$ edquota -p myquota1 -u myquota2
        shuhuang@shuhuang:~$ edquota -g myquotagrp
        shuhuang@shuhuang:~$ edquota -t
```

quota限制值的报表
```
    quota [-uvs] [username]
    quota [-gvs] [groupname]
    -u:     后面可以接username，表示显示该用户的quota限制值，若没有username，则显示执行者的quota限制值
    -g:     后可接groupname，表示显示该用户组的quota限制值
    -v:     显示每个用户在文件系统的quota值
    -s:     使用1024为倍数来指定单位
    e.g.
        shuhuang@shuhuang:~$ quota -uvs myquota1 myquota2
        shuhuang@shuhuang:~$ quota -gvs myquotagrp
```

repquota -a [-vugs]
```
-a:     直接到/etc/mtab查询具有quota标志的文件系统，并报告quota的结果
-v:     输出的数据将含有文件系统相关的详细说明
-u:     显示出用户的quota限值
-g:     显示出个别用户组的quota限值
-s:     使用M，G为单位显示结果
e.g.
    shuhuang@shuhuang:~$ repquota -auvs
```

warnquota:  超过限额者发出警告信息

setquota [-u | -g] 名称 block(soft) block(hard) inode(soft) inode(hard) filesystem
```
    shuhuang@shuhuang:~# quota -uv myquota1
    shuhuang@shuhuang:~# setquota -u myquota1 100000 200000 0 0 /home
    shuhuang@shuhuang:~# quota -uv myquota1
```

#####软件磁盘阵列:

mdadm:
```
    mdadm --detail /dev/md0
    mdadm --create --auto=yes /dev/md[0-9] --raid-devices=N --level=[015] --spare-devices=N /dev/sdx /dev/hdx...
    --create:           为新建RAID的参数
    --auto=yes:         决定新建后面接的软件磁盘阵列设备，即/dev/md0，/dev/md1等
    --raid-devices=N:   使用几个磁盘作为磁盘阵列的设备，N为数字
    --spare-devices=N:  使用几个磁盘作为备用(spare)设备，N为数字
    --level=[015]:      设置这组磁盘阵列的等级
    --detail:           后面接的磁盘阵列的详细信息
```

九 例行性工作(crontab)
----

#####仅执行一次的工作调度

atd启动与at运行方式：
```
    shuhuang@shuhuang:~# /etc/init.d/atd restart
    # 重新启动atd
```

at:
```
at的运行方式:
    1.先寻找/etc/at.allow这个文件，写在这个文件中的用户才能使用at，没有在这个文件内的用户不能使用at(即使没在at.deny中)
    2.如果/etc/at.allow不存在，就寻找/etc/at.deny这个文件，若写在at.deny的用户则不能使用at，没有即可以使用at
    3.如果两个文件都存在，仅有root可以使用at

at [-mldv] TIME
at -c work_id
    -m:     当at工作完成后，以email通知用户工作完成
    -l:     at -l 相当于 atq，列出系统上面的所有该用户的at调度
    -d:     at -d 相当于 atrm，可以取消一个在at调度中的工作
    -v:     可以使用较明显的时间格式列出at调度中的任务列表
    -c:     可以列出后面接的该项工作的实际命令内容
    TIME:   时间格式，可以定义什么时候要进行at这项工作的时间，格式有:
        HH:MM               ex> 04:00
            HH:MM时刻进行，若以超过，则明天的HH:MM时刻进行此项工作
        HH:MM YYYY-MM-DD    ex> 04:00 2015-03-17
            强制规定在某年某月某日的某时刻进行该工作
        HH:MM[am | pm] [Month] [Date]   ex> 04pm March 17
            也是一样，强制某月某日进行
        HH:MM[am | pm] + number [minutes | hours | days | weeks]        ex> now + 5 minutes
            ex> 04pm + 3 days
    e.g.
        shuhuang@shuhuang:~$ at now + 5 minutes
        at> /bin/mail root -s "testing at job" < /root/.bashrc
        at> <EOF>

        shuhuang@shuhuang:~$ at now + 10 minutes
        at> /usr/bin/mail root -s "test at job" < /root/.bashrc
        at> <EOF>

        shuhuang@shuhuang:~$ at -c 4
        # 查看第4项工作内容

        shuhuang@shuhuang:~$ at 23:00 2015-03-17
        at> /bin/sync
        at> /bin/sync
        at> /sbin/shutdown -h now
        at> <EOF>
        # 设置在2015-03-17日23:00自动关机
```

atq: 用来查看at工作

atrm [jobnumber]:   at工作删除
```
        shuhuang@shuhuang:~$ atq
        5   2015-03-17 23:00 a shuhuang
        # jobnumber = 5, start_time = 2015-03-17 23:00, excutor = shuhuang
        shuhuang@shuhuang:~$ atrm 5
        # rm the job whose jobnumber is 5
```

batch:  系统有空时才执行后台程序(cpu工作负载小于0.8的时候才进行你所执行的工作任务)
```
        shuhuang@shuhuang:~$ batch 23:00 2015-03-17
        at> /bin/sync
        at> /bin/sync
        at> /sbin/shutdown -h now
        at> <EOF>       # ctrl + d
```

##### 循环执行的例行性工作调度(由cron这个系统服务控制)

crontab:    新建循环型工作调度
```
/etc/cron.allow:
    将可以使用crontab的帐号写入其中，若不在这个文件内的用户则不可以使用crontab
/etc/cron.deny:
    将不可以使用crontab的帐号写入其中，若未记录到这个文件当中的用户，就可以使用crontab
    /etc/cron.allow比/etc/cron.deny的优先级高(与at类似)

当使用crontab这个命令新建工作调度之后，该项工作会被记录到/var/spool/cron里面，而且是以帐号来作为判别

crontab [-u username] [-l|-e|-r]
    -u:     只有root才能进行这个任务，即帮其他用户新建/删除crontab工作调度
    -e:     编辑crontab的工作内容
    -l:     查阅crontab的工作内容
    -r:     删除所有的crontab的工作内容，若仅删除一项，请用-e编辑
    e.g.
        shuhuang@shuhuang:~$ crontab -e
        # minute hour  day   month  weeks command
        #  0~59  0~23  1~31  1~12   0~7
        # weeks的0和7都表示星期天
        # 特殊字符:
            '*':    for 'any'
            ',':    代表分隔时段，比如执行工作是3:00和6:00,就是:    0  3,6  * * * commmand
            '-':    表示一段时间范围,如8点到12点的每20分都进行一项工作: 20  8-12 * * * command
            '/n':   n是数字，每隔n单位间隔的意思，如每五分钟进行一次:   */5  * * * * command    # '*'与'/5'搭配,等价于0-59/5
        shuhuang@shuhuang:~$ crontab -e
        编辑:
            */5 * * * * /home/shuhuang/test.sh
        # 每五分钟会执行/home/shuhuang/test.sh
```

/etc/crontab:   系统的配置文件
```
    如果是系统的例行性工作，那么只需编辑/etc/crontab这个文件就OK
    'crontab -e' 是/usr/bin/crontab 这个执行文件，但是 /etc/crontab是个纯文本文件，可用root身份编辑一下
    若相让系统每小时帮你执行某个命令，将该命令写成script，并将该文件放置到/etc/cron.hourly/目录下即可
```

cron进行例行性的工作的注意事项:
```
    1.资源分配不均匀问题，当有多个crontab在同一时间点执行时，系统变得非常繁忙
        解决:   用','分隔时段进行那些工作，降低系统资源分配不均匀问题
    2.取消不要的输出选项，如果执行结果有输出数据，则会mail给MAILTO设置的帐号，那当有调度出错时，会一直法信息(如DNS的检测系统，
        若DNS上层主机挂掉，那么就是一直发送错误信息)，
        解决:   使用数据流重定向，将输出结果输出到 /dev/null
    3.安全的检验，检查/var/log/cron的内容来查看是否有非你设置的cron被执行
    4.周与日，月不可同时并存，就是设置了周，那么日和月就不要设置，反之，设置了日和月份，那么周就不要设置
```

##### 可唤醒停机期间的工作任务

anacron:
```
    anacron会去分析现在的时间与时间记录文件所记载的上次执行anacron的时间，
    若有发现某些时刻没有进行crotab，此时就会进行未那些没有被执行的crontab任务
    anacron运行时间:    1.系统开机期间运行  2.写入crontab的调度中

    anacron [-sfn] [job]..
    anacron -u [job]..
    -s:     开始连续执行各项工作，会依据时间记录文件的数据判断是否进行
    -f:     强制进行，而不去判断时间记录文件的时间戳
    -n:     立刻进行未进行的任务，而不延迟(delay)等待时间
    -u:     仅更新时间记录文件的时间戳，不进行任何工作
    job:    由/etc/anacrontab定义的各项工作名称
```

/etc/anacron:
```
    SHELL=/bin/sh
    PATH=/sbin:/bin:/usr/sbin:/usr/bin
    MAILTO=root

    1   65  cron.daily      run-parts /etc/cron.daily
    7   70  cron.weekly     run-parts /etc/cron.daily
    30  75  cron.monthly    run-parts /etc/cron.monthly
    # day   delay_time  workname    command
    # workname can be defined by yourself, command is same to the crontab's command
    "anacron -s cron.daily":
        1.由/etc/anacrontab分析cron.daily这项工作名称的天数为1
        2.由/var/spool/anacron/cron.daily取出最近一次执行anacron的时间戳
        3.由上个步骤与目前的时间相比较，若差异天数为1天以上(含一天),就准备进行命令
        4.若准备执行命令，根据/etc/anacrontab的设置将延迟65分钟
        5.延迟时间过后，开始执行后续命令，即"run-parts /etc/cron.daily"
        6.执行完毕后，anacron程序结束
```


十 程序管理与SELinux初探
----

程序:   通常为二进制程序放置在存储媒介，以物理文件的形式存在

进程:
```
被加载到内存当中运行的程序，那么在内存内的那个数据就被称为进程(process)
程序被触发后，执行者的权限与属性，程序的代码与所需的数据都会被加载到内存中，
操作系统并给予这个内存的单元一个标识符(PID),进程就是一个正在运行的程序
```

前台:   你可以控制与执行命令的这个环境称为前台(foreground)

后台:   可以自行运行的工作，你无法使用[ctrl]+c终止，可以使用bg/fg调用该工作(background)

子进程/父进程


'&':将工作丢到后台(终端模式)中
```
    e.g.    shuhuang@shuhuang:~$ tar -zjc -f /tmp/etc.tar.gz /etc &
            shuhuang@shuhuang:~$ tar -zjcv -f /tmp/etc.tar.gz /etc > /tmp/log.txt 2>&1 &
```

jobs:
```
    jobs [-lrs]
    -l:     列出job number与命令串，同时列出PID号码
    -r:     仅列出正在后台(终端模式)run的工作
    -s:     仅列出正在后台(终端模式)当中暂停(stop)的工作
    e.g.
        shuhuang@shuhuang:~$ jobs -l
        [1]- 10314 Stopped          vim ~/.bashrc
        [2]+ 10833 Stopped          find / -print
        # [1]: job number,     '-'/'+': 最近/最近最后第2个被放置到bg的工作码,  10314: PID,  Stopped: states
```

fg: 取出后台(终端模式)程序到前台
```
    fg %jobnumber
    jobnumber:  工作号码，'%'可有可无
    e.g.
        shuhuang@shuhuang:~$ fg
        # 默认取最近一个被放置到后台(终端模式)的工作
        shuhuang@shuhuang:~$ jobs
        shuhuang@shuhuang:~$ fg %1
```

bg: 让程序在后台(终端模式)运行
```
    bg %jobnumber
    e.g.
        shuhuang@shuhuang:~$ jobs ; bg %3; jobs
```

kill:   管理后台(终端模式)工作
```
    kill -signal %jobnumber
    kill -l
    -l:         列出目前kill能够使用的信号(signal)
    -signal:    工作指示(可用man 7 signal查看相关)
        -1:     重新读取一次参数的配置文件
        -2:     代表与由键盘输入 [ctrl]+c 同样操作
        -9:     立刻强制删除一个工作(多用在删除不正常的工作)
        -15:    以正常的程序方式终止一项工作(与-9 不一样，多用在删除正常的工作，以正常步骤结束)
    若直接使用kill + number命令令结束工作，那么那个number默认是表示PID,
    e.g.
        shuhuang@shuhuang:~$ kill 10833     # 删除掉PID为10833的程序
        shuhuang@shuhuang:~$ jobs
        # 先查看有哪些jobs可以kill
        shuhuang@shuhuang:~$ kill -15 %1
        shuhuang@shuhuang:~$ jobs
        shuhuang@shuhuang:~$ kill -SIGTERM %1
```

nohup:  脱机管理命令
```
    nohup [命令与参数]
    nohup [命令与参数] &
```

#### 进程的查看:
ps:
```
ps aux      <== 查看系统所有的进程数据
ps -lA      <== 也是能够查看系统的数据
ps axjf     <== 连同部分进程树状态
-A:     显示所有进程
-a:     不与terminal有关的进程
-u:     有效用户(effective user)相关的进程
x:      与-a一起使用，列出比较完整信息
l:      较长，较详细地将信息列出
j:      工作的格式(jobs format)
-f:     更完整的输出
e.g.
    shuhuang@shuhuang:~$ ps -l
    说明:
        F:  进程标志(process flags),说明这个进程权限，常见码:
            4   -   此进程的权限为root
            1   -   此进程仅可复制(fork),无法实际执行(exec)
        S:  进程的状态(STAT),主要状态有:
            R(Running): 该进程处于运行中
            S(Sleep):   该进程属于睡眠(idle),但可以被唤醒(signal)
            D:          不可被唤醒的睡眠状态
            T:          停止状态，可能是工作控制或除错(traced)状态
            Z:          "僵尸"状态，进程已终止，但是无法被删除至内存外
        UID:    该进程被UID所拥有
        PID:    该进程PID
        PPID:   该进程父进程PId
        C:      CPU使用率(单位%)
        PRI/NI:     priority/Nice 缩写,CPU所执行的优先级，数值越小表示越快被CPU所执行  
        ADDR:       kernel function，表示该进程在内存的哪个部分，如果是running，一般会显示'-'
        SZ:         表示用掉多少内存
        WCHAN:      表示内存是否正在运行中，'-'表示正在运行
        TTY:        终端机位置
        TIME:       使用掉的CPU时间，此进程实际花费CPU运行的时间
        CMD:        command
    shuhuang@shuhuang:~$ ps aux
    说明:
        USER:   该进程属于哪个用户帐号
        PID:    该进程的进程标识符
        %CPU:   该进程使用掉的CPU资源百分比
        %MEM:   该进程所占用的物理内存
        VSZ:    该进程使用掉的虚拟内存量(KB)
        RSS:    该进程占用的固定的内存量(KB)
        TTY:    该进程在哪个终端机运行，与终端机无关则显示?，若是pst/0等，则表示为由网络链接进主机的进程
        STAT:   该进程目前的状态
        START:  该进程被触发启动的时间
        TIME:   该进程实际CPU运行时间
        COMMAND:    该进程实际命令
```

top:    动态查看进程状态
```
    top [-d number] | top [-bnp]
    -d:     后接数字，就是整个进程界面更新的秒数，默认5s
    -b:     以批次的方式执行top，通常搭配数据重定向
    -n:     后接数字，与-b搭配，需要进行几次top的输出结果
    -p:     指定PID来进行查看监测
    在top执行过程中，可使用下面按键命令:
        ?:  显示top中可以输入的按键命令
        P:  以CPU的使用资源排序
        M:  以内存使用资源排序
        N:  以PID来排序
        T:  由该进程使用CPU的时间积累来排序(TIME+)
        k:  给与某个PID一个signal
        r:  给与某个PID重新制定一个nice值
        q:  离开top软件的按键
    e.g.
        shuhuang@shuhuang:~$ top -d 2
        说明:
            第一行(top...):     这一行显示的信息分别为
                目前的时间
                开机到现在所经过的时间
                已登录系统的用户人数
                系统在1，5，15分钟的平均工作负载: batch 工作方式为负载小于0.8就是这个负载
            第二行(Tasks...):   显示目前进程的总量与个别进程在什么状态(running, sleeping, stopped, zombie)
                                zombie指僵尸进程,如果不是0，那就存在进程已变成僵尸
            第三行(Cpus...):    显示CPU的整体负载，每个选项可用?查阅，需要注意的是%wa，是指I/Owait，
                                通常系统会变慢都是I/O产生的问题比较大。可以按"1"来切换成不同CPU的负载
            第四与第五行:       目前物理内存与虚拟内存(Mem/Swap)的使用情况，
            第六行:             top中输入命令显示状态的地方
```

pstree:
```
    pstree [-A|U] [-up]
    -A:     各进程树之间的链接以ASCII字符来链接
    -U:     各进程树之间的链接以utf-8码的字符来链接，某些终端口可能有error
    -p:     同时列出每个进程的PID
    -u:     同时列出每个进程的username
    e.g.
        shuhuang@shuhuang:~$ pstree -A
        shuhuang@shuhuang:~$ petree -Aup
```

signal:
```
    1   SIGHUP      启动被终止的进程，可让PID重读自己的配置文件，类似重启
    2   SIGINT      相当于用键盘输入[ctrl]+c来中断一个进程的进行
    9   SIGKILL     代表强制中断一个进程的进行，类似错误中断程序
    15  SIGTERM     以正常的结束进程来终止该进程
    17  SIGSTOP     相当于键盘输入[ctrl]+z来暂停一个进程的进行
```

kill：杀死进程
```
    kill -signal PID
    killall [-iTe] [command name]
    -i:     interactive,交互式的，若需删除会出现提示符给用户
    -e:     exact，后面接的command name要一致，但整个完整的命令不能超过15个字符
    -I:     命令名称忽略大小写
    e.g.
        shuhuang@shuhuang:~$ killall -1 syslogd         # 给syslogd这个启动命令启动的PID一个SIGHUP的信号
        shuhuang@shuhuang:~$ killall -9 httpd           # 强制终止所有以httpd启动的进程
        shuhuang@shuhuang:~$ killall -i -9 bash         # 一次询问每个bash进程是否需要被终止
```

Priority 与 Nice值:
```
    Priority,即PRI值，越低代表越优先，PRI值是有内核动态调整，用户无法直接调整PRI值，查看命令: "ps -l"
    PRI值无法修改，所以要调整进程的优先执行时，可修改Nice值(NI)，有: PRI(new) = PRI(old) + nice
    nice值有正有负，并且:
        1.nice值可调整范围为:   -20~19
        2.root可随意调整自己或他人进程的Nice值，且范围是:   -20~19
        3.一般用户仅可以调整自己的进程的Nice值，且范围为:   0~19

    nice命令：
        nice [-n number] command
        -n:     后接树值，范围是: -20~19
        e.g.
            shuhuang@shuhuang:~$ nice -n 5 vi &
            # '&'指后台执行
    renice命令：
        renice [number] PID
        e.g.
            shuhuang@shuhuang:~$ ps -l
            # 用于查看进程的PID
            shuhuang@shuhuang:~$ renice 10 PID
```

#### 系统资源的查看

free:   内存查看
```
    free [-b|-k|-m|-g] [-t]
    -b: free默认单位是KB,使用-b(bytes),-k(KB),-m(MB),-g(GB)
    -t: 输出swap和内存总量
    e.g.
        shuhuang@shuhuang:~$ free -m
        shuhuang@shuhuang:~$ free -m -t
```

uname:  查看系统与内核相关信息
```
    uname [-asrmpi]
    -a: 所有系统相关的信息
    -s: 系统内核名称
    -r: 系统内核版本
    -m: 本系统的名称
    -p: CPU类型
    -i: 硬件平台
```

uptime: 查看系统启动时间与工作负载(top命令的第一行信息)
```
    e.g.    shuhuang@shuhuang:~$ uptime
```

netstat:    跟踪网络
```
    netstat -[atunlp]
    -a: 将目前系统上所有的链接，监听，socket数据都列出来
    -t: 列出tcp网络数据包的数据
    -u: 列出udp网络数据包的数据
    -n: 不列出进程的服务名称，以端口号(port number)来显示
    -l: 列出目前正在网络监听(listen)的服务
    -p: 列出该网络服务的进程PID
    e.g.
        shuhuang@shuhuang:~$ netstat
        说明:
            Active Internet connections (w/o servers)
                Proto:      网络的数据包协议，主要分为TCP/UDP数据包
                Recv-Q:     非由用户进程链接到此socket的复制的总字节数
                Send-Q:     非由远程主机传送过来的acknowledged总字节数
                LocalAddress:   本地IP端口情况
                ForeignAddress: 远程主机的IP端口情况
                State:      链接状态，主要建立(ESTABLISED)及监听(LISTEN)
            Active UNIX domain sockets (w/o servers)
                Proto:      一般就是unix
                RefCnt:     链接到此socket的进程的数量
                Flags:      链接标识
                Type:       socket访问类型，主要有确认链接的STREAM与不需要确认的DGRAM
                State:      若为CONNECTED表示多个进程之间以建立链接
                Path:       链接到此socket的相关程序的路径，或者是相关数据输出的路径
        shuhuang@shuhuang:~$ netstat -ntlp
        # 找出目前系统上已在监听的网络链接及其PID
```

dmesg:  查看内核检测的信息
```
        shuhuang@shuhuang:~$ dmesg | less
```

vmstat: 检测系统资源变化
```
    vmstat [-a] [delay [count]]
    vmstat [-fs]
    vmstat [-S 单位]
    vmstat [-d]
    vmstat [-p 分区]
    -a:     使用inactive/active代替buffer/cache的内存输出信息
    -f:     开机到目前为止系统复制的进程
    -s:     将一些事件(开机至当前)导致的内存变化情况列表说明
    -S:     后面可以接单位，让显示的数据有单位，如K/M代替bytes的容量
    -d:     列出磁盘的读写总量统计表
    -p:     后面列出分区，可显示该分区的读写总量统计
    e.g.
        shuhuang@shuhuang:~$ vmstat 1 3     # 每1s更新一次，总共更新3次
        说明:
            procs选项:
                r:  等待运行中的进程数量
                b:  不可唤醒的进程数量
            memory选项:
                swpd:   虚拟内存被使用的容量
                free:   未被使用的容量
                buff:   用于缓冲存储器
                cache:  用于高速缓存
            swap选项:
                si: 由磁盘中将程序取出的量
                so: 由于内存不足而将没用到的程序写入到磁盘的swap的容量
            io(磁盘读写):
                bi: 由磁盘写入的块数量
                bo: 写入到磁盘去的块数量
            system(系统):
                in: 每秒被中断的进程次数
                cs: 每秒钟进行的事件切换次数
            CPU选项:
                us: 非内核层的CPU使用状态
                sy: 内核层所使用的CPU状态
                id: 闲置状态
                wa: 等待I/O所耗费的CPU状态
                st: 被虚拟机所盗用的CPU使用状态
        shuhuang@shuhuang:~$ vmstat -d      # 显示系统上面所有的磁盘读写状态
```

/proc/: 内存当中的数据写入到这个目录下
```
    /proc/cmdline文件:      加载kernel时执行的相关参数，可以了解系统如何启动
    /proc/cpuinfo文件:      本机的CPU的相关信息，包含频率，类型与运算功能
    /proc/devices文件:      这个文件记录系统各个主要设备的主要设备代号，与mknod有关
    /proc/filesystems:      目前系统已经加载的文件系统
    /proc/interrupts:       目前系统上面的IRQ分配状态
    /proc/ioports文件:      目前系统上面各个设备所配置的I/O地址
    /proc/kcore文件:        这个就是内存的大小
    /proc/loadavg:          top/uptime的三个平均数值
    /proc/meminfo:          使用free列出的内存信息
    /proc/modules文件:      目前我们的linux已经加载的模块列表，也可以想成驱动程序
    /proc/mounts文件:       系统已经挂载的数据，就是用mount这个命令调出的数据
    /proc/swaps文件:        记录使用的分区
    /proc/partitions:       记录fdisk -l会出现的所有分区
    /proc/pci文件:          在PCI总线上面每个设备的详细情况，可用lspci查询
```

fuser:  查看已打开或已执行程序打开的文件
```
    fuser [-umv] [-k [i] [signal]] file/dir
    -u:     除了进程的PID外，同时列出该进程的所有者
    -m:     后面接的文件名会主动提到该文件系统的所顶层
    -v:     可以列出每个文件与程序还有命令的完整相关性
    -k:     找出使用该文件/目录的PID，并试图以SIGKILL这个信号给与该PID
    -i:     必须与-k配合，在删除PID之前会现先询问用户意愿
    -signal:    如-1 -15等，若不加默认是SIGKILL(-9)
    e.g.
        shuhuang@shuhuang:~$ fuser -uv .
        说明:
        ACCESS选项的意义:
            'c':    此进程在当前目录下
            'e':    可被出发为执行状态
            'f':    是一个被打开的文件
            'r':    代表顶层目录(root directory)
            'F':    该文件被打开，不过在等待回应中
            'm':    可能为分享的动态函数库
```

lsof:   列出被进程打开的文件
```
    lsof [-aUu] [+d]
    -a:     多项数据需要同时成立才显示结果(and)
    -U:     仅列出unix like系统的socket文件类型
    -u:     后面接username，列出该用户相关进程所打开的文件
    +d:     后面接目录，找出目录下面被打开的文件
    e.g.
        shuhuang@shuhuang:~$ lsof       # 默认列出系统上所有已经打开的文件与设备
        shuhuang@shuhuang:~$ lsof -u root -a -U
        shuhuang@shuhuang:~$ lsof +d /dev
        shuhuang@shuhuang:~$ lsof -u root | grep bash
```

pidof:  找出某个正在执行的进程的PID
```
    pidof [-sx] program_name
    -s:     仅列出一个PID而不列出所有PID
    -x:     同时列出该program name可能的PPID那个进程的PID
    e.g.
        shuhuang@shuhuang:~$ pidof init bash
```

十一 认识系统服务(daemons)
----

十二 认识与分析日志文件
----

linux常见日志文件名
```
    /var/log/cron:      例行性工作调度
    /var/log/dmesg:     记录系统在开机的时候内核检测过程所产生的各项信息
    /var/log/lastlog:   可以记录系统上面所有帐号最近一次登录系统时的相关信息(lastlog命令)
    /var/log/mail*:     记录邮件往来信息
    /var/log/messages:  几乎系统发生的错误信息都会记录于此(very important)
    /var/log/secure:    只要牵涉到需要输入帐号密码，登录时都会被记录在此文件
    /var/log/wtmp,/var/log/faillog: 登录系统者的帐号信息
```
