## Ubuntu安装mongodb

1.导入软件源的公钥
----

```
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv EA312927
```

2.为mongodb创建软件源list文件
----

ubuntu12.04
```
echo "deb http://repo.mongodb.org/apt/ubuntu precise/mongodb-org/3.2 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.2.list
```

ubuntu14.04
```
echo "deb http://repo.mongodb.org/apt/ubuntu trusty/mongodb-org/3.2 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.2.list
```

ubuntu16.04
```
echo "deb http://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/3.2 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.2.list
```

3.更新软件源并安装mongodb
----

```
sudo apt-get update
sudo apt-get install -y mongodb-org
```
如果想要安装特定的版本，使用下面命令：
```
sudo apt-get install -y mongodb-org=3.2.9 mongodb-org-server=3.2.9 mongodb-org-shell=3.2.9 mongodb-org-mongos=3.2.9 mongodb-org-tools=3.2.9
```

4.配置启动文件
----

如果是ubuntu16.04的版本，需要手动新建/lib/systemd/system/mongod.service文件，并写入下面内容：
```
[Unit]
Description=High-performance, schema-free document-oriented database
After=network.target
Documentation=https://docs.mongodb.org/manual

[Service]
User=mongodb
Group=mongodb
ExecStart=/usr/bin/mongod --quiet --config /etc/mongod.conf

[Install]
WantedBy=multi-user.target
```

5.启动、重启和关闭命令
----

```
sudo service mongod start
sudo service mongod restart
sudo service mongod stop
```

6.mongodb的完全卸载
----

先停止运行mongodb
```
sudo service mongod stop
```

再卸载软件
```
sudo apt-get purge mongodb-org*
```
删除数据库和日志文件
```
sudo rm -r /var/log/mongodb
sudo rm -r /var/lib/mongodb
```

7.添加php的mongodb扩展
----

```
# pecl install mongodb
# echo "extension=mongodb.so" >> `php --ini | grep "Loaded Configuration" | sed -e "s|.*:\s*||"`
```

参考链接
----

https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/
http://mongodb.github.io/mongo-php-driver/
