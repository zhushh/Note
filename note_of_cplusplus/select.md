---
name: select.md
date: 2017-03-24
update: 2017-03-24
keywords: c++ select IO多路复用
---

select头文件及相关操作接口
----
```c++
#include <sys/time.h>
#include <sys/types.h>
#include <sys/select.h> 

/*
 * nfds： 监听中最大的文件描述符+1
 * readfds: 监听读操作的fds
 * writefds: 监听写操作的fds
 * exceptfds: 监听发生异常的fds
 * timeout: 设置定时，如果timeout为0，表示立即返回，timeout为NULL表示一直监听
 ***********************/
int select(int nfds, fd_set *readfds, fd_set *writefds, fd_set *exceptfds, struct timeval *timeout);
FD_SET(int fd, fd_set *fdset);    // 设置fdset中的fd位
FD_CLR(int fd, fd_set *fdset);    // 清除掉fdset中的fd位
FD_ISSET(int fd, fd_set *fdset);  // 如果fdset中的fd位被设置，那么返回非0值； 否则返回0
FD_ZERO(fd_set *fdset);           // 用于初始化fd_set
```
select简单运行例子
----
```c++
// simple_select.cpp
#include <iostream>
#include <string>
using namespace std;

#include <stdio.h>
#include <stdlib.h>
#include <errno.h>

#include <unistd.h>
#include <sys/time.h>
#include <sys/types.h>

#define STDIN 0

int main()
{
    struct timeval tv;

    tv.tv_sec = 2;
    tv.tv_usec = 5000;

    fd_set reads;

    FD_ZERO(&reads);
    FD_SET(STDIN, &reads);

    if (select(STDIN+1, &reads, NULL, NULL, &tv) == -1) {
        perror("select");
        exit(1);
    }

    if (FD_ISSET(STDIN, &reads)) 
    {
        std::string input;

        std::cin >> input;
        std::cout << "You input: " << input << std::endl;
    } 
    else 
    {
        printf("Timeout\n");
    }

    return 0;
}
```
编译运行
```
$ g++  simple_select.cpp
$ ./a.out   # 一直不输入等待
Timeout
$ ./a.out
Hello
You input: Hello
$ 
```

参考链接
----
* [select网络编程例子](https://github.com/zhushh/cplusplus/tree/master/network_programming/select)
* [select main page](http://www.mkssoftware.com/docs/man3/select.3.asp)
* [Beej's Guide to Network programming](http://beej.us/guide/bgnet/output/html/multipage/index.html)
* [Linux IO模式及 select、poll、epoll详解](https://segmentfault.com/a/1190000003063859)
