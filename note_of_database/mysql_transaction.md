#### 事务隔离级别

##### Read Uncommitted(未提交读)

一个事务读到了另一个未提交事务修改过的数据；

| 时间序列 | SessionA                                               | SessionB                                     |
| -------- | ------------------------------------------------------ | -------------------------------------------- |
| 1        | begin;                                                 |                                              |
| 2        |                                                        | begin;                                       |
| 3        | select name from user where id = 1;返回name = ‘rick’;  |                                              |
| 4        |                                                        | update user set name = ‘mongo’ where id = 1; |
| 5        | select name from user where id = 1;返回name = ‘mongo’; |                                              |

如果SessionB中的事务稍后进行了回滚，那么SessionA中的事务相当于读到了一个不存在的数据，这种现象也称为**脏读**。



##### Read Committed(已提交读)

即一个事务能读到另一个已经提交事务修改后的数据，如果其他事务均对该数据进行修改并提交，该事务也能查询到最新值；

| 时间序列 | SessionA                                               | SessionB                                     |
| -------- | ------------------------------------------------------ | -------------------------------------------- |
| 1        | begin;                                                 |                                              |
| 2        |                                                        | begin;                                       |
| 3        | select name from user where id = 1;返回name = ‘rick’;  |                                              |
| 4        |                                                        | update user set name = ‘mongo’ where id = 1; |
| 5        | select name from user where id = 1;返回name = ‘rick’;  |                                              |
| 6        |                                                        | commit;                                      |
| 7        | select name from user where id = 1;返回name = ‘mongo’; |                                              |



##### Repeatable Read(可重复读)

即事务能读到另一个已经提交的事务修改过的数据，但是第一次读过某条记录后，即使后面其他事务修改了该记录的值并且提交，该事务之后再读该条记录时，读到的仍是第一次读到的值，而不是每次都读到不同的数据;

| 时间序列 | SessionA                                              | SessionB                                     |
| -------- | ----------------------------------------------------- | -------------------------------------------- |
| 1        | begin;                                                |                                              |
| 2        |                                                       | begin;                                       |
| 3        | select name from user where id = 1;返回name = ‘rick’; |                                              |
| 4        |                                                       | update user set name = ‘mongo’ where id = 1; |
| 5        | select name from user where id = 1;返回name = ‘rick’; |                                              |
| 6        |                                                       | commit;                                      |
| 7        | select name from user where id = 1;返回name = ‘rick’; |                                              |



##### Serializable(串行)

串行化， 上面三种隔离级别可以进行 读-读 或者 读-写、写-读三种并发操作，而SERIALIZABLE不允许读-写，写-读的并发操作；

| 时间序列 | SessionA                                               | SessionB                                     |
| -------- | ------------------------------------------------------ | -------------------------------------------- |
| 1        | begin;                                                 |                                              |
| 2        |                                                        | begin;                                       |
| 3        | select name from user where id = 1;返回name = ‘rick’;  |                                              |
| 4        |                                                        | update user set name = ‘mongo’ where id = 1; |
| 5        | select name from user where id = 1;**waiting等待**     |                                              |
| 6        |                                                        | commit;                                      |
| 7        | select name from user where id = 1;返回name = ‘mongo’; |                                              |



#### TCC分布式事务

Try-Confirm-Cancel；



#### 知识点

- InnoDB默认是REPEATABLE-READ级别，此级别在其余数据库中是会引起幻读问题，InnoDB采用Next-Key Lock锁算法避免了此问题

- 行锁和表锁，在不同引擎还有所区别，MyISAM只有表锁，没有行锁，不支持事务。 InnoDB 有行锁和表锁，支持事务。



#### 参考

深入理解mysql事务：https://juejin.im/post/5cbc049de51d456e7b372089

