---
name: ssh命令.md
date: 2017-04-05
update: 2017-04-05
keywords: ssh ssh命令
---

ssh命令
----
* ssh命令介绍

    ssh命令用于远程登录linux上的主机

* 命令格式

    ```
    ssh [-l login_name] [-p port] [user@]hostname
    ```
    其中hostname可以是ip地址或者远程主机的hostname；更详细命令格式使用`ssh -h`查看；

* 查看是否已经安装和运行了ssh服务

    查看是否安装ssh服务：
    ```
    $ ps -e | grep ssh
    ```
    如果输出类似如下就说明安装了ssh并且已经正在运行，如果什么都没有说明没有安装ssh服务：
    ```
    904 ？       00:00:00 sshd
    ```

* ssh服务的配置文件

    ssh服务的默认配置文件在/etc/ssh/ssh_config，可以编辑这个文件进行ssh配置；
    例如，修改ssh开启的默认端口（防止端口扫描）,修改如下面：
    ```
    #Port 22
    ```
    改成如下(假设在8918开启ssh服务)
    ```
    Port 8918
    ```

* Ubuntu安装ssh服务

    默认情况下，ubuntu没有安装ssh服务，需要使用手动安装配置；可以使用下面命令进行安装配置:
    ```
    $ sudo apt-get install openssh-server
    ```
    再次检查看ssh服务：
    ```
    $ ps -e | grep ssh
    6759 ?        00:00:00 sshd
    ```
    如果还是没有看到上面的输出，那么可以使用命令运行ssh服务：
    ```
    $ sudo /etc/init.d/ssh start
    ```
    ubuntu 16.04使用下面命令：
    ```
    $ systemctl restart sshd.service
    ```

* 例子

    登录本地ssh服务
    ```
    $ ssh localhost
    ```
    不指定用户登录
    ```
    $ ssh 192.168.0.11
    ```
    指定用户登录
    ```
    $ ssh -l root 192.168.0.11
    $ ssh root@192.168.0.1
    ```
    指定端口登录(前提是已经修改了ssh服务的端口，假设把默认的22端口改成8918)
    ```
    $ ssh -p 8918 192.168.0.11
    $ ssh -p 8918 root@192.168.0.11
    ```