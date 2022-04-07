## Ubuntu14.04安装LEMP

1.安装Mysql
----

数据库安装：
```
  sudo apt-get update
  sudo apt-get install mysql-server mysql-client
```
终端输入下面命令安装配置数据库安全防护：
```
  mysql_secure_installation
```

2.安装Nginx
----

如果已经安装了apache2，可以先删除在装nginx：
```
  sudo service apache2 stop
  sudo apt-get purge apache2*
  sudo apt-get autoremove apache2
```

使用Nginx安装包安装：
```
  sudo apt-get update
  sudo apt-get install nginx
```
安装完成后可以访问http://localhost访问查看是否成功

3.安装php
----

ubuntu上面可以安装php5：
```
  sudo apt-get update
  sudo apt-get install php5 php5-fpm php5-mysql php5-cli php5-cgi php5-curl
```

4.配置Nginx
----

使用下面命令打开配置文件/etc/nginx/nginx.conf：`sudo vim /etc/nginx/nginx.conf`（此处可选）使用lscpu查看cpu的信息，可以把worker_processes的值修改成lscpu显示的CPU(s)的值,保存后退出;

查看nginx.conf文件的`http {}`里的信息，看默认的虚拟主机文件在哪里配置，一般有两种情况，如果是出现：
```
  include /etc/nginx/conf.d/*.conf;
```
那么默认虚拟主机的配置信息就在/conf.d/目录下的以.conf后缀的文件定义；如果是出现下面这种：
```
  include /etc/nginx/site-available/*.conf;
```
就说明是在/site-available目录下的.conf后缀文件定义，其他以此类推；
假设默认的虚拟主机在/etc/nginx/conf.d/目录下配置，我们使用下面命令创建一个虚拟主机文件：
```
  sudo vim /etc/nginx/conf.d/example.conf
```
然后复制下面这些配置信息：
```
server {
  listen 80;

  root /usr/share/nginx/html;
  index index.php index.html index.htm;
  server_name example.localhost;

  location / {
     #try_files $uri $uri/ /index.html;
     index index.php;
     if (-f $request_filename) {
         break;
     }
     rewrite ^/(.+)$ /index.php?url=$1 last;
     break;
  }

  error_page 404 /404.html;

  # redirect server error pages to the static page /50x.html
  #
  error_page 500 502 503 504 /50x.html;
  location = /50x.html {
  root /usr/share/nginx/html;
  }

  # proxy the PHP scripts to Apache listening on 127.0.0.1:80
  #
  #location ~ \.php$ {
  # proxy_pass http://127.0.0.1;
  #}

  # pass the PHP scripts to FastCGI server listening on 127.0.0.1:9000
  #
  location ~ \.php$ {
  try_files $uri =404;
  fastcgi_pass 127.0.0.1:9000;
  fastcgi_index index.php;
  fastcgi_param SCRIPT_FILENAME /scripts$fastcgi_script_name;
  include fastcgi_params;
  }
}
```

5.配置hosts, php-cgi, php-fpm以及让php-fpm使用TCP来链接
----

配置好nginx后，下面开始配置hosts，php-cgi和php-fpm

(1).先打开/etc/hosts文件，配置上面nginx里的server_name，配置如下：
```
  127.0.0.1 example.localhost
```
(2).之后，打开/etc/php5/fpm/php.ini文件，找到cgi.fix_pathinfo，并配置为下面：
```
  cgi.fix_pathinfo=0
```
(3).再打开/etc/nginx/fastcgi_params文件，配置以下信息：
```
  fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
```
(4).然后打开`/etc/php5/fpm/pool.d/www.conf`文件，其中有下面这行：
```
listen = /var/run/php5-fpm.sock
```
意思是让php-fpm使用socket链接，注释掉上面的listen，换成下面这个配置，使得php-fpm用TCP来链接：
```
listen = 127.0.0.1:9000
```

6.测试
----

新建一个php文件/usr/share/nginx/html/info.php:
```
sudo vim /usr/share/nginx/html/info.php
```
并输入下面内容：
```
<?php
phpinfo();
?>
```
在浏览器访问[http://example.localhost/info.php](http://example.localhost/info.php)，就可以看到php的输出信息；

参考链接
----

1.https://www.digitalocean.com/community/tutorials/how-to-install-linux-nginx-mysql-php-lemp-stack-on-ubuntu-14-04​
2.http://www.linuxidc.com/Linux/2016-05/131154.htm​
3.http://www.linuxidc.com/Linux/2016-05/131154.htm