### mysql limit查询优化

#### 背景

用户信息表`user_login_info`，存储了用户`imei`信息，这个字段目前是没有索引，

因为一些需求，需要导出用户这个imei信息，新建一个表进行存储查询（建立索引）；

因为某些原因，不适用数据库的数据表复制方式实现，所以使用查询方式并记录上次处理的offset游标；



#### 查询方式

- 方式一

  使用`limit`查询，每次查询出一部分数据，然后写入新的表中：

  ```sql
  select Fimei from user_login_info limit offset, num;
  ```

  当数据量达到千万级别时，发现`offset`越大的时候，查询效率越慢，原因是因为使用`limit offset,num`，需要扫描数据定位到偏移量`offset`，导致速度较慢。

  

- 方式二

  换一种思考查询方式，用户信息表的`uid`肯定是唯一的，把`uid`当作游标进行查询数据，就可以实现遍历表了，这里`xxx`每次增加的值等于`num`就可以了；

  ```sql
  select Fimei from user_login_info where uid >= xxx limit num;
  ```

  优化原理：方式一普通查询是在数据文件上完成的，但是方式二利用了`uid`这个索引，是在索引上完成的，然后再顺序往后查询。



#### 扩展阅读

其他的优化方式是通过：`子查询`和`JOIN分页方式`来解决，具体可以阅读：https://juejin.im/post/5cd2d57951882540d928c2be

