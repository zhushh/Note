#### mysql取前一天日期

错误写法：

```sql
select item_id, count(*) as Count from tbl_adv_reward_record where date(delivery_time) = curdate() - 1 group by item_id order by Count desc limit 30;
```



正确写法：

```sql
select item_id, count(*) as Count from tbl_adv_reward_record where date(delivery_time) = date_sub(curdate(),interval 1 day) group by item_id order by Count desc limit 30;
```





#### 参考

https://blog.csdn.net/woshizhangliang999/article/details/48001021

