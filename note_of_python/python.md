#### hashlib

```python
from hashlib import sha256

with open('words', 'r') as f:
    for line in f:
        hashword = sha256(line.rstrip()).hexdigest()
        print(hashword)
```



#### redis使用

使用`pipeline`优化速度

```python
from redis import Redis

#写入redis
r = Redis(host = '127.2.1.36',port= 1231,db = 0,password ='xxxx')
pipe = r.pipeline()

filename = "test.txt"
for line in open(filename, "wb+"):
    line = line.strip()
    line = line.lower()
    pipe.sadd(key_name, line)
    print "line:",line

records = pipe.execute()
print records
```

#### mysql

**时戳转换**

```python
import time

now = int(time.time())
sql = """update t_test set modified_time = from_unixtime(%d)""" % (now)

try:
    cursor = connections["test_db"].cursor()
    cnt = cursor.excute(sql)
    connection.commit()
exception Exception, e:
    log.debug("err:%s", str(e))
finally:
    log.debug("cursor cnt:%d", cnt)
```

**参数化查询**

python的mysql参数化查询，不是使用mysql的预编译语句，而是通过在mysqldb中通过转义字符串然后直接将他们插入到查询中，而不是使用`MYSQL_STMT_API`来完成的。因此，unicode字符串必须经过两个中间表示（编码字符串，转义编码字符串）才能被数据库接收。

```python
params = []
params.append(name)
params.append(passwd)
sql = "select * from t_user where name=%s and passwd=%s;"
cursor.execute(sql, params)
```

如果不使用参数化查询，上面`name='a or 1=1'`时，会导致where语句一直为True，导致查询任何用户都可以实现；



#### 获取url尾部文件名

```python
# s = "/usr/path/to/your/dir/test.txt"
# filename = get_filename(s)
# print(filename)
def get_filename(url):
	return url.rsplit("/", 1)[-1]
```

#### requests使用

[http://docs.python-requests.org/zh_CN/latest/user/quickstart.html](http://docs.python-requests.org/zh_CN/latest/user/quickstart.html)

```python
import json
import requests

r = requests.get("http://example.org")
print(r.status_code)
print(r.text.encode('utf-8'))
print(r.content)

```

#### logging使用例子

```python
import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger('my_logger')
handler = RotatingFileHandler('my_log.log', maxBytes=2000, backupCount=10)
logger.addHandler(handler)

for _ in range(100):
    logger.warning('hello')

```

#### Json使用

```python
import os
import json

data = {
    "name": "nick",
    "age": 24,
    "phoneNumber": "12716121267"
}

def save_to_file(filename, d):
    if os.path.exists(filename):
        os.remove(filename)
    with open(filename, 'wb') as fp:
        fp.write(json.dumps(d))
    return None

def load_from_file(filename):
    d = None
    if not os.path.exists(filename):
        return None
    with open(filename, 'rb') as fp:
        d = json.load(fp)
    return d

if __name__ == '__main__':
    filename = 'user.dat'
    save_to_file(filename, data)
    d = load_from_file(filename)
    print(d)

```



#### reload函数

- `reload`会重新加载已加载模块，但是原来使用的实例还是使用旧的模块，而新生产的实例会使用新的模块

- `reload`后还是原来的内存地址

- `reload`不支持`from xxx import xxx`格式的模块进行重新加载

  ```python
  from recommend import A
  reload(A)	# 这个不支持
  ```

  上面应该使用这种格式

  ```python
  import recommend
  
  reload(recommend)
  from recommend import A
  ```

- python3.0把`reload`内置函数移到了`imp标准模块中，需要导入才能使用

  ```python
  from imp import reload
  ```


#### types库使用

```
import types

dir(types)

data = ['a', 'b', 'c']
if types.ListType == type(data):

```

#### 关于*args和**kwargs

这里`args`和`kwargs`只是名字，是可以修改成其他名字的，关键点在于`*`和`**`，`*args`和`**kwargs`主要用于定义函数，表示可以处理可变参数，比如

```python
def myprint(first, *args, **kwargs):
	print("first variable: ", first)
    for arg in args:
        print("another variable in *argv:", arg)
    for k, v in kwargs.items():
        print("{0} == {1}".format(k, v))

myprint('a', 'b', 'd', c='c', f='f')
```

上面会输出：

```
('first variable: ', 'a')
('another variable in *argv:', 'b')
('another variable in *argv:', 'd')
c == c
f == f
```























