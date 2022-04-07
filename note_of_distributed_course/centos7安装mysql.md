下载Mysql官方的YUM Repository
----
```
# wget http://repo.mysql.com//mysql57-community-release-el7-8.noarch.rpm
```


安装YUM
----
```
# yum -y install mysql57-community-release-el7-8.noarch.rpm
```


安装Mysql服务端
----
```
# yum search mysql-com
# yum -y install mysql-community-server.x86_64
```


启动Mysql服务
----
```
# systemctl start mysqld.service
```
查看是否启动成功
```
# systemctl status mysqld.service
```
显示 active (running) 则表示已经正常启动


登录数据库
----
第一次启动Mysql服务，mysql会生成一个临时的初始密码，密码保存在 mysql 进程的日志里，即(/var/log/mysqld.log)，查看密码：
```
# cat /var/log/mysqld.log | grep "password"
```
然后登录
```
# mysql -uroot -p
```

修改root密码
----
登录进去后，使用官方建议的修改密码操作
```
mysql> ALTER USER 'root'@'localhost' IDENTIFIED BY 'new_password';
```
设置的密码有要求，密码长度要大于8，包含大小写字母、数字和特殊符号；


参考链接
----
* [https://my.oschina.net/Laily/blog/713023](https://my.oschina.net/Laily/blog/713023)
