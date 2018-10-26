## SQL

### left join, right join, inner join and full join

![](https://raw.githubusercontent.com/zhushh/Note/master/img/sql_join.png)


### SQL注入及参数化查询

#### SQL注入

SQL注入，通过一定手段，将某些命令插入到后台sql语句中，达到欺骗服务器从而获取信息的目的。

例子
```sql
select * from tbl_user where name = 'nick' and passwd = 'k'
```
这查询的个人信息，如果将name的值改为`'nick' or 1 = 1 #`，那么上面查询语句变成
```sql
select * from tbl_user where name = 'nick' or 1 = 1 # passwd = 'k'
```
由于`#`是mysql的注释符，所以上面的语句实际上是：
```sql
select * from tbl_user where name = 'nick' or 1 = 1
```
这样一来，攻击者就不需要输入密码就可以获取用户信息了。

#### 参数化查询

参数化查询（Parameteried Query）是访问数据库时，在需要填入数值或数据的地方，使用参数（Parameter）来给值。在使用参数化查询的情况下，数据库服务器不会将参数的内容视为SQL指令的一部分来处理，而是数据库完成SQL指令的编译后，才代入参数运行，因此就算参数中含有指令，也不会被数据库运行。
