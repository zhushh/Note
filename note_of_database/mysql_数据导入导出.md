### mysql数据导入导出

1. 数据库导出：`mysqldump -uroot -h192.168.1.101 -p dbtest > dbtest.sql`
2. 数据内容导出：`mysql -usnsradio -h 192.168.1.101 -pdbtest  -P 4010 test_db -e "select userid, nickname from t_user_profile limit 100" > tmp.txt`
3. 数据库导入：`mysql -uroot -h192.168.1.101 -p dbtest < /tmp/dbtest.sql --default-character-set=utf8`
4. 数据表复制：`CREATE TABLE new_table SELECT * FROM old_table;`
5. 数据表重命名：`RENAME TABLE old_table TO new_table;`





### 参考

https://blog.csdn.net/albertsh/article/details/103324062