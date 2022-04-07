## Ubuntu or linux network configuration file /etc/network/interfaces

Example 1
----
```
auto lo
iface lo inet loopback

# The primary network interface
auto eth0
iface eth0 inet static
address 192.168.0.42
network 192.178.0.0
netmask 255.255.255.0
broadcast 192.168.0.255
gateway 192.168.0.1
```

- 第1行跟第5行说明lo接口和eth0接口会在系统启动时被自动配置；
- 第2行将lo接口设置为本地回还（loopback）地址；
- 第6行说明eth0接口是一个静态（static）IP地址；
- 第7-11行分别设置eth0接口的ip、网络号、子网掩码、广播地址和网关；


Example 2
----
```
auto eth0
iface eth0 inet static 
address 192.168.1.42
network 192.168.1.0
netmask 255.255.255.128
broadcast 192.168.1.0

up route add -net 192.168.1.128 netmask 255.255.255.0 gw 192.168.1.2
up route add default gw 192.168.1.200
down route del default gw 192.168.1.200
down route del -net 192.168.1.128 netmask 255.255.255.0 gw 192.168.1.2
```

- 第7-8行配置的是在接口启用的时候，添加一条静态路由和一个缺省路由；
- 第9-10行配置是在接口禁用的时候，删掉这两条路由配置；


Example 3
----
```
auto eth0 eth0:1

iface eth0 inet static
address 192.168.0.100
network 192.168.0.0
netmask 255.255.255.0
broadcast 192.168.0.255
gateway 192.168.0.1

iface eth0:1 inet static 
address 192.168.0.200
network 192.168.0.0
netmask 255.255.255.0
```

- 第10-13行在eth0上面配置了另一个地址，这种配置方式在配置一块网卡有多个地址的时候很常见；
- 其中eth0冒号后面的数字可以随便选择，只需要确保配置的名字不重复就可以；


Example 4
----
```
auto eth0
iface eth0 inet dhcp
pre-up [ -f /etc/network/local-network-ok ]
```

- 第3行配置说明在激活eth0之前会检查/etc/network/local-network-ok文件是否存在，存在才激活；
