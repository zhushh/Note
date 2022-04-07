---
name: kvm相关技术.md
date: 2017-04-02
update: 2017-04-02
keywords: kvm libvirt ubuntu 虚拟机 虚拟机技术
---


什么是KVM？
----

```
Kernel-based Virtual Machine的简称，是一个开源的系统虚拟化模块；
它可以在不改变linux镜像的情况下，同时运行多个虚拟机，把linux内核转换成一个虚拟机监视器(Hypervisor);
```
[维基百科](https://zh.wikipedia.org/wiki/%E5%9F%BA%E4%BA%8E%E5%86%85%E6%A0%B8%E7%9A%84%E8%99%9A%E6%8B%9F%E6%9C%BA)

[kvm wiki](https://en.wikipedia.org/wiki/Kernel-based_Virtual_Machine)

[kvm百科](http://baike.baidu.com/link?url=VBJtn9Sfnh5Diap_0HXYYEzhrMcLyewXF8oWLVS-7An6CqQGfvO-JaDrVSp7wzFK92EjCW7zD4QO1aUj9CM-uGizDHDoh2lPgZvTu_GJ7rndpGbe6js1H5Hm6HSlL5ra)

[Hypervisor](https://zh.wikipedia.org/wiki/Hypervisor)

安装KVM准备
----

- 确定机器有VT（virtualization Tech）

    ```
    $ grep vmx /proc/cpuinfo
    ```

- 确保BIOS开启了VT

- 确保内核版本较新(2.6.20以上)，支持KVM
    ```
    $ uname -a
    ```

Ubuntu安装KVM
----
* 安装必要的包

    这些必要的包是安装虚拟机服务器版本(没有图形界面)的必要的包
    ```
    $ sudo apt-get install kvm qemu-kvm libvirt-bin ubuntu-vm-builder bridge-utils
    ```
    说明一下
    ```
    1.libvirt-bin提供libvirtd，可以用来管理qemu和kvm实例
    2.qemu-kvm是kvm的后端服务
    3.ubuntu-vm-builder为构建虚拟机提供强大的命令行工具
    4.bridge-utils为虚拟机和网卡之间提供网桥
    ```

* 添加用户到用户组

    使用下面命令把你当前用户添加到libvirtd和kvm用户组：
    ```
    $ sudo adduser `id -un` kvm
    $ sudo adduser `id -un` libvirtd
    ```

* 重启后验证是否安装成功

    使用下面这个命令来检测安装是否成功
    ```
    $ virsh list --all
    Id Name         State
    --------------------------

    $
    ```

* 虚拟机管理

    1.列出正在运行的虚拟机
    ```
    $ virsh list
    ```
    2.启动一个虚拟机
    ```
    $ virsh start web_devel
    ```
    3.在启动时开始一个虚拟机
    ```
    $ virsh autostart web_devel
    ```
    4.重启一个虚拟机
    ```
    $ virsh reboot web_devel
    ```
    5.将虚拟机的状态保存到文件中，一旦保存虚拟机将不再运行
    ```
    $ virsh save web_devel-170408.state
    ```
    6.唤醒经过保存的虚拟机
    ```
    $ virsh restore web_devel-170408.state
    ```
    7.关闭虚拟机
    ```
    $ virsh shutdown web_devel
    ```
    8.把CDROM设备挂载到虚拟机上面
    ```
    $ virsh attach-disk web_devel /dev/cdrom /media/cdrom
    ```


* 虚拟机管理器

    如果想要使用桌面环境，那么需要先安装virt-manager，virt-manager包含有一组图形化的程序用以管理本地和远程的虚拟机，
    输入下面命令进行安装virt-manager:
    ```
    $ sudo apt-get install virt-manager
    ```
    链接到本地libvirt服务：
    ```
    $ virt-manager -c qemu:///system
    ```
    如果想要链接到另一台计算机上面的libvirt服务，可以使用下面的命令：
    ```
    $ virt-manager -c qemu+ssh://virtnode1.mydomain.com/system
    ```
    上面的命令是假设你已经设置好ssh管理和virtnode1.domain.com的连通，更多细节设置参看[OpenSSH服务器](https://help.ubuntu.com/lts/serverguide/openssh-server.html)


* 虚拟机查看器

    virt-viewer程序可以链接到虚拟机，运行virt-viewer需要虚拟机支持图形界面；
    安装virt-viewer命令：
    ```
    $ sudo apt-get install virt-viewer
    ```
    运行虚拟机后，使用下面命令到控制台：
    ```
    $ virt-viewer web_devel
    ```
    和virt-manager相似，virt-viewer也可以通过授权ssh远程链接到远方主机:
    ```
    $ virt-viewer -c qemu+ssh://virtnode1.mydomain.com/system web_devel
    ```

* 参考链接

    [KVM installation - ubuntu help](https://help.ubuntu.com/community/KVM/Installation)

    [libvirt - ubuntu help](https://help.ubuntu.com/lts/serverguide/libvirt.html)


了解QEMU
----
qemu是一个开源的hosted hypervisor,配合kvm一起使用，虚拟机的运行速度可以达到原生硬件的运行速度；
详细的可以查看相关的wiki链接：[qemu wiki](https://en.wikipedia.org/wiki/QEMU)

可看qemu相关网站：[qemu-project.org](http://wiki.qemu-project.org/Features/KVM)


vncviewer是什么？
----

```
Virtual Network Computing（VNC）是一个远程系统，允许你和网络上的另一台计算机的虚拟桌面进行交互；
使用VNC，你可以运行图形界面应用，并在你本地上面显示；VNC的客户端和服务端都支持多个操作系统；
```
下载网址[https://github.com/TigerVNC/tigervnc/releases](https://github.com/TigerVNC/tigervnc/releases)

ubuntu可以使用下面命令进行安装配置：
```
$ mkdir vncviewer && cd vncviewer
$ wget https://dl.bintray.com/tigervnc/stable/tigervnc-1.7.1.x86_64.tar.gz 
$ tar zxvf tigervnc-1.7.1.x86_64.tar.gz 
$ sudo cp -r tigervnc-1.7.1.x86_64/usr/* /usr/
```


制作镜像模板
----

* 创建镜像文件

    ```
    $ qemu-img create -f qcow2 centos.img 10G
    ```

* 启动kvm虚拟机，进行系统安装

    ```
    $ qemu-system-x86_64 -enable-kvm -m 2048 -cdrom CentOS-7-x86_64-DVD.iso -drive file=centos.img,if=virtio  -boot d -usbdevice tablet -nographic -vnc :51
    ```

* 启动vncviewer链接到kvm虚拟机进行系统安装

    ```
    $ vncviewer ip:port
    ```
    其中，ip是本地的ip地址；port是上面启动kvm命令最后`-vnc`后面指定的端口；

    链接进去后，就按照正常的系统安装完成整个虚拟系统的安装即可；

* 安装完成后再次进入系统

    启动kvm虚拟机命令：
    ```
    $ qemu-system-x86_64 -enable-kvm -m 2048 -drive file=centos.img,if=virtio -net nic,model=virtio -net user -boot c -nographic -usbdevice tablet  -vnc :51
    ```
    如果在上一步安装完成后，命令行中无法关掉qemu-system-x86_64命令，使用kill杀掉进程就可以了；

    使用vncviewer链接到虚拟机命令：
    ```
    $ vncviewer ip:port
    ```
    重新链接进去就可以进行登录；
    
 
xrdp安装
----
为了使虚拟镜像系统支持远程链接，需要安装xrdp，xrdp是一个开源的远程桌面协议服务器；
详细链接参考: [xrdp官网](www.xrdp.org)
 
* CentOS虚拟镜像系统安装xrdp
 
    使用下面命令新建xrdp.repo文件
    ```
    # vim /etc/yum.repos.d/xrdp.repo
    ```
    然后在文件中输入下面内容
    ```
    [xrdp]
    name=xrdp
    baseurl=http://li.nu.ro/download/nux/dextop/el7/x86_64/
    enabled=1
    gpgcheck=0
    ```
    配置好后，再使用下面命令安装xrdp:
    ```
    # yum -y install xrdp tigervnc-server
    ```
    安装完成后，使用下面命令开启xrdp服务，并检查是否启动成功
    ```
    # systemctl enable xrdp.service
    # systemctl start xrdp.service
    # netstat -antup | grep xrdp
    ```
    看到输出success说明安装启动成功，现在来开启xrdp的防火墙端口：
    ```
    # firewall-cmd --permanent --zone=public --add-port=3389/tcp
    # firewall-cmd --reload
    ```
