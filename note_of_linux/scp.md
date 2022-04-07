#### scp

文件传输/拷贝命令



##### 传输文件例子

```
$ scp local_file root@127.0.0.1:/home/zhushh/code
```

上面的命令执行，会把本地的`local_file`传输到远程`127.0.0.1`地址的`/home/zhushh/code`目录下，需要输入账号`root`的密码。



##### 拷贝下载文件例子

```
$ scp root@127.0.0.1:/home/zhushh/code/remote_file .
```

上面命令执行，会把远程`127.0.0.1`服务器的`/home/zhushh/code/remote_file`拷贝到本地当前目录，需要输入账号`root`的密码。





