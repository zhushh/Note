## Ubuntu下的防火墙 ufw&iptables

ufw
----

### 简介

一款相对iptables来说简单很多的主机端的防火墙配置工具，目的是提供给用户一个可以轻松驾驭的界面

### 简单使用

#### 启动和设置默认规则
```shell
$ sudo ufw default deny
$ sudo ufw enable
```
设置默认规则为deny，按上面设置，除了指明打开的端口，其他的端口默认都是关闭状态；

然后启动ufw(注意下次重启机器的时候，ufw也会自动启动)；

#### 开放特定的端口或协议
```shell
$ sudo ufw allow 22     # 开启端口22访问
$ sudo ufw allow ssh    # 开启ssh访问
$ sudo ufw allow smtp   # 允许所有外部ip访问本机的25/tcp（smtp）端口
$ sudo ufw deny smtp    # 禁止外部访问smtp协议
```
/etc/services文件里面定义了端口号对应的服务名，例如：22对应的协议就是ssh

#### 查看防火墙的状态：
```shell
$ sudo ufw status
```

#### 删除已经添加的规则：
```shell
$ sudo ufw delete allow 22
```

#### 打开特定端口且限制特定协议：
```shell
$ sudo ufw allow 22/tcp
```

#### 允许特定ip访问全部端口及删除
```shell
$ sudo ufw allow from 192.168.254.254
$ sudo ufw delete allow from 192.168.254.254
```

#### 设置特定ip，协议和端口号限制：
```shell
$ sudo ufw allow proto tcp from 192.168.0.1 any port 22
```

#### 关闭防火墙：
```shell
$ sudo ufw disable
```


iptables
----

### 简介

一款防火墙软件

### 简单使用

#### iptables的匹配顺序
```
对于每一个报文，iptables依次测试每一条规则，看报文与规则是否相匹配；一旦找到一条匹配的规则，就根据规则中指定的动作对报文进行处理，而对后面的规则不在进行测试；因此，最好是先设置ACCEPT的规则，在配置DROP的规则；
```

#### 列出当前的配置规则
```shell
$ sudo iptables -L
Chain INPUT (policy ACCEPT)
target     prot opt source               destination
Chain FORWARD (policy ACCEPT)
target     prot opt source               destination
Chain OUTPUT (policy ACCEPT)
target     prot opt source               destination
```
默认是没有配置ip规则

#### 允许已建立的链接接收数据
```shell
$ sudo iptables -A INPUT -m state --state ESTEBLISHED,RELATED -j ACCEPT
```

#### 开放特定的端口
```
$ sudo iptables -A INPUT -p tcp -i eth0 --dport ssh -j ACCEPT
```
上面的意思是，一条规则会被追加到INPUT规则列表（-A表示追加）；根据上面规则，所有从接口eth0（-i指出通过哪个接口的报文运用此规则）接收到的目标端口为22(--dport指定端口ssh是与22端口对应的服务名)的tcp报文（-p指明了是tcp报文），iptables要执行ACCEPT动作（-j指明报文与规则相匹配时应采取的行动）；

#### 开放80端口
```
$ sudo iptables -A INPUT -p tcp -i eth0 --dport 80 -j ACCEPT
```

#### 阻断通信
```
$ sudo iptables -A INPUT -j DROP
```
上面的命令是指，丢弃所有的报文；所以除了之前已经配置过的ACCEPT规则里的报文，其他报文都会被丢弃

#### 编辑iptables
如果被设置了`$ sudo iptables -A INPUT -j DROP`后，环回接口(lookback)也被阻断了，所以我们可以编辑iptables来插入一条匹配lo接口规则解决这个问题，如下：
```
$ sudo iptables -I INPUT 4 -i lo -j ACCEPT
```
`-I`表示插入,'4'表示插入到第几个规则

#### Logging记录
```
$ sudo iptables -I INPUT 5 -m limit --limit 5/min -j LOG --log-prefix "iptables denied: " --log-level 7
```
在INPUT规则的第5行插入日志动作的规则，日志的格式是"iptables denied: " + 错误信息，日志级别为7

#### 保存设置相关命令
默认时，iptables的设置会在重启的时候被清空，所以可以使用`iptables-save`和`iptables-restore`来保存和恢复设置

#### 开机自动加载配置
先将防火墙规则保存到/etc/iptables.up.rules文件中
```
$ iptables-save > /etc/iptables.up.rules
```
然后修改脚本/etc/network/interfaces，使系统能自动应用这些规则(下面最后一行是手动添加)
```
auto eth0
iface eth0 inet dhcp
pre-up iptables-restore < /etc/iptables.up.rules
```
另外，你可以通过下面的设置使得iptables在网络接口关闭后，使用另一套规则
```
auto eth0
iface eth0 inet dhcp
pre-up iptables-restore < /etc/iptables.up.rules
post-down iptables-restore < /etc/iptables.down.rules
```

#### 自动加载与保存配置
配置/etc/network/interfaces文件
```
pre-up iptables-restore < /etc/iptables.up.rules
post-down iptables-save > /etc/iptables.up.rules
```

#### 禁用iptables防火墙
```
$ sudo iptables -F
```

参考链接
----

[http://wiki.ubuntu.org.cn/IptablesHowTo](http://wiki.ubuntu.org.cn/IptablesHowTo)

[http://forum.ubuntu.org.cn/viewtopic.php?f=169&t=292611](http://forum.ubuntu.org.cn/viewtopic.php?f=169&t=292611)

