---
name: apache_cgi.md
date: Sat 31 Dec 2016 01:38:27 PM CST
update: Sat 31 Dec 2016 01:38:27 PM CST
keyword: 
---

Apache 安装
----

* 安装前环境准备

    Arp安装，下载地址[http://www-us.apache.org/dist//apr/apr-1.5.2.tar.gz](http://www-us.apache.org/dist//apr/apr-1.5.2.tar.gz)
    ```
    $ wget http://www-us.apache.org/dist//apr/apr-1.5.2.tar.gz && tar zxf apr-1.5.2.tar.gz && cd apr-1.5.2
    $ ./configure
    $ make
    $ sudo make install
    ```

    Arp-Util安装，下载地址[http://www-us.apache.org/dist//apr/apr-util-1.5.4.tar.gz](http://www-us.apache.org/dist//apr/apr-util-1.5.4.tar.gz)
    ```
    $ wget http://www-us.apache.org/dist//apr/apr-util-1.5.4.tar.gz && tar zxf apr-util-1.5.4.tar.gz && cd apr-util-1.5.4
    $ whereis apr
    apr: /usr/local/apr
    $ ./configure --with-apr=/usr/local/apr
    $ make
    $ sudo make install
    ```

    Pcre安装，下载地址[http://exim.mirror.fr/pcre/pcre-8.38.tar.gz](http://exim.mirror.fr/pcre/pcre-8.38.tar.gz)
    ```
    $ wget http://exim.mirror.fr/pcre/pcre-8.38.tar.gz && tar zxf pcre-8.38.tar.gz && cd pcre-8.38
    $ ./configure
    $ make
    $ sudo make install
    ```

* Apache安装

    官网地址 [http://httpd.apache.org/docs/2.4/install.html](http://httpd.apache.org/docs/2.4/install.html)
    
    下载解压后，进入解压后的目录，输入下面该命令进行apache的源码编译安装
    ```
    $ wget http://apache.fayea.com//httpd/httpd-2.4.25.tar.gz && tar zxf httpd-2.4.25.tar.gz && cd httpd-2.4.25
    $ ./configure
    $ make
    $ sudo make install
    ```

* 检测安装成功

    运行下面命令：
    ```
    $ sudo /usr/local/apache2/bin/apachectl -k start
    ```
    然后如果看到输出如下错误：
    ```
    $ sudo /usr/local/apache2/bin/apachectl -k start
    /usr/local/apache2/bin/httpd: error while loading shared libraries: libpcre.so.1: cannot open shared object file: No such file or directory
    ```
    表示依赖链接出错，使用ldd命令检测依赖：
    ```
    $ ldd /usr/local/apache2/bin/httpd
        linux-vdso.so.1 =>  (0x00007ffcc8f17000)
        libpcre.so.1 => not found
        libaprutil-1.so.0 => /usr/local/apr/lib/libaprutil-1.so.0 (0x00007f6433144000)
        libapr-1.so.0 => /usr/local/apr/lib/libapr-1.so.0 (0x00007f6432f10000)
        libpthread.so.0 => /lib/x86_64-linux-gnu/libpthread.so.0 (0x00007f6432cf3000)
        libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007f643292a000)
        libexpat.so.1 => /lib/x86_64-linux-gnu/libexpat.so.1 (0x00007f6432700000)
        libcrypt.so.1 => /lib/x86_64-linux-gnu/libcrypt.so.1 (0x00007f64324c8000)
        libdl.so.2 => /lib/x86_64-linux-gnu/libdl.so.2 (0x00007f64322c4000)
        /lib64/ld-linux-x86-64.so.2 (0x0000564a25a4e000)
    ```
    发现`libpcre.so.1 => not found`，因为之前装过pcre，所以使用下面命令创建链接即可：
    ```
    $ sudo ln -s /usr/local/lib/libpcre.so.1 /lib
    ```
    再次启动apache服务看一下：
    ```
    $ sudo /usr/local/apache2/bin/apachectl -k start
    ```
    没有报错，然后访问浏览器[http://localhost](http://localhost)， 就可以看到下面输出
    ```
    It works!
    ```

* 参考链接

    [http://xpleaf.blog.51cto.com/9315560/1740221](http://xpleaf.blog.51cto.com/9315560/1740221)



CGI介绍及配置
----

*  CGI简单介绍

    Common Gateway Interface(cgi), 通用网关接口， CGI是外部应用程序（CGI程序）与Web服务器之间的接口标准，是在CGI程序和Web服务器之间传递信息的过程。wiki链接[https://en.wikipedia.org/wiki/Common_Gateway_Interface](https://en.wikipedia.org/wiki/Common_Gateway_Interface)

* 配置Apache加载cgi模块
    
    编辑刚刚安装配置好的apache配置文件/usr/local/apache2/conf/http.conf来进行配置，找到下面这行内容
    ```
    #LoadModule cgid_module modules/mod_cgid.so
    ```
    去掉注释
    ```
    LoadModule cgid_module modules/mod_cgid.so
    ```

* 设置cgi脚本文件路径

    找到下面的映射路径
    ```
    ScriptAlias /cgi-bin/ "/usr/local/apache2/cgi-bin/"
    ```
    上面设置的意思是，当你通过浏览器访问/cgi-bin/时，实际上访问的是/usr/local/apache2/cgi-bin/目录；
    将其改成你cgi源代码所在的目录就可以：
    ```
    ScriptAlias /cgi-bin/ "/home/zhushh/Rick/apache-cgi/"
    ```
    注意上面的"/home/zhushh/Rick/apache-cgi/"路径的最后一个"/"不能省略；

* 设置cgi的访问权限

    大概在http.conf的198行：
    ```
    <Directory />
        AllowOverride none
        Require all denied
    </Directory>
    ```
    把上面的内容替换成下面的：
    ```
    <Directory "/home/zhushh/Rick/apache-cgi/">
       AllowOverride None
       Options +ExecCGI
       Order allow,deny
       Allow from all
    </Directory>
    ```
    如果这里没有修改，浏览器会提示以下错误：
    ```
    Forbidden
    You don't have permission to access /cgi-bin/hello.py on this server.
    ```

* 设置apache可解释的cgi脚本文件

    找到下面这行内容，大概在389行左右：
    ```
    #AddHandler cgi-script .cgi
    ```
    去掉注释，然后添加自己需要支持的cgi脚本文件，比如python的，就设置如下：
    ```
    AddHandler cgi-script .cgi .py .pl
    ```
    其他的类似，配置好这一步就基本配置好cgi，重启一下apache服务就可以；
    ```
    $ sudo /usr/local/apache2/bin/apachectl restart
    ```

* 添加cgi的脚本文件

    在/home/zhushh/Rick/apache-cgi目录下创建下面的python文件进行测试，文件命名为hello.py
    ```python
    #!/usr/bin/env python

    print "Content-type:text/html"
    print ""
    print "<html>"
    print "<head>"
    print "<title>Hello</title>"
    print "</head>"
    print "<body>"
    print "<h2>Hello world!</h2>"
    print "<p>This is my first cgi program</p>"
    print "</body>"
    print "</html>"
    ```
    设置文件权限为755:
    ```
    $ chmod 755 hello.py
    ```
    如果浏览器提示500错误，请检查是否在第一行有`#!/usr/bin/env python`.

* 通过浏览器访问cgi文件

    在浏览器中输入http://localhost/cgi-bin/hello.py　或者　http://127.0.0.1/cgi-bin/hello.py　
    看到如下输出：
    ```
    Hello world!

    This is my first cgi program
    ```
    如果是遇到以下错误：
    ```
    Forbidden
    You don't have permission to access /cgi-bin/hello.py
    ```
    那么，请确认一下`/home/zhushh/`目录的权限保证为'755'以上；也可以查看ａｐａｃｈｅ的日志；
    
    ### ａｐａｃｈｅ的日志在: /usr/local/apache2/logs 目录下 ###
    其中，错误日志文件为：　`error_log`;访问日志文件为： `access_log`;遇到任何解决不了的问题请查看日志；

* 用C++编写cgi脚本并在浏览器访问，程序如下：

    ```c++
    #include <iostream>
    using namespace std;

    int main() {
        cout << "Content-type:text/html" << endl << endl;
        cout << "<html>" << endl;
        cout << "<head>" << endl;
        cout << "<title>Hello</title>" << endl;
        cout << "</head>" << endl;
        cout << "<body>" << endl;
        cout << "<h2>Hello, World!</h2>" << endl;
        cout << "<p>The cpp program for cgi.</p>" << endl;
        cout << "</body>" << endl;
        cout << "</html>" << endl;
        return 0;
    }
    ```
    需要注意的是，语句`cout << "Content-type:text/html" << endl << endl;`一定要有两个换行，
    因为这是http协议响应的报文结构决定的;另外，还需要注意编译好后的可执行程序没有后缀名，那可以直接重命名为hello.cgi；
    这样就可以通过http://localhost/cgi-bin/hello.cgi 或者 http://127.0.0.1/cgi-bin/hello.cgi 来访问刚刚编译好的cpp可执行程序;
