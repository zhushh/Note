---
name: rpc学习.md
date: 2017-01-04
update: 2017-01-04
keyword: rpc
---


什么是RPC
----

wiki链接[https://en.wikipedia.org/wiki/Remote_procedure_call](https://en.wikipedia.org/wiki/Remote_procedure_call)

简单点说，远程过程调用(RPC)就是通过网络从远程计算机上请求服务，而不需要了解底层网络技术的协议。
这是客户-服务器（client-server）模型的交互形式，主要用过请求-响应（request-response）的消息传递系统实现。


RPC调用步骤
----

1. 客户端调用客户端句柄（client stub），这个过程是本地调用，会把参数等数据放到栈里；
2. 客户端句柄封装这些参数到一个消息体，然后发起一个系统调用发送消息体；这个过程叫[marshalling](https://en.wikipedia.org/wiki/Marshalling_(computer_science))
3. 客户端操作系统通过网络把消息体发送给远程服务器端的机器；
4. 服务器端操作系统接收消息体，并解析发送给服务端句柄；
5. 服务器端句柄，解析消息体，得到调用参数等信息；这个过程是[unmarshalling](https://en.wikipedia.org/wiki/Unmarshalling)
6. 服务器句柄调用服务器过程，把执行后的结果按相同的方式发送回给客户端；

注：
[序列化和marshalling的异同](http://stackoverflow.com/questions/770474/what-is-the-difference-between-serialization-and-marshaling)


为什么需要RPC
----
RPC远程调用使调用过程透明，不需要去关心里面的实现细节，可以方便业务的解耦；
RPC是一个软件结构概念，是构建分布式应用的理论基础；


python的RPC简单例子
----

客户端代码
```python
#!/usr/bin/env python3

import pickle

class RPCProxy:
    def __init__(self, connection):
        self._connection = connection

    def __getattr__(self,name):
        def do_rpc(*args, **kwargs):
            self._connection.send(pickle.dumps((name, args, kwargs)))
            result = pickle.loads(self._connection.recv())
            if isinstance(result, Exception):
                raise result
            return result

        return do_rpc

from multiprocessing.connection import Client

c = Client(('localhost', 17000), authkey=b'zhushh')
proxy = RPCProxy(c)
print(proxy.add(2, 3))      # 5
print(proxy.sub(3, 4))      # -1
```

服务器端代码
```python
#!/usr/bin/env python3

import pickle

class RPCHandler:
    def __init__(self):
        self._functions = {}

    def register_function(self, func):
        self._functions[func.__name__] = func

    def handle_connection(self, connection):
        try:
            while True:
                # Receive a message
                func_name, args, kwargs = pickle.loads(connection.recv())
                # Run the rpc and send a response
                try:
                    r = self._functions[func_name](*args, **kwargs)
                    connection.send(pickle.dumps(r))
                except Exception as e:
                    connection.send(pickle.dumps(e))
        except EOFError:
            pass

from multiprocessing.connection import Listener
from threading import Thread 

def rpc_server(handler, address, authkey):
    sock = Listener(address, authkey=authkey)
    while True:
        client = sock.accept()
        t = Thread(target=handler.handle_connection, args=(client, ))
        t.daemon = True
        t.start()

# some remote functions

def add(x, y):
    return x+y

def sub(x, y):
    return x-y

# Receive with a handler
handler = RPCHandler()
handler.register_function(add)
handler.register_function(sub)

# Run the server
rpc_server(handler, ('localhost', 17000), authkey=b'zhushh')
```


推荐阅读
----

[https://en.wikipedia.org/wiki/Remote_procedure_call](https://en.wikipedia.org/wiki/Remote_procedure_call)

[https://waylau.com/remote-procedure-calls/](https://waylau.com/remote-procedure-calls/)
