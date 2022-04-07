### Linux环境安装配置java

检查并删掉默认的openjdk [可选]
----
以centos环境为例子，（如果不想删除原来的就忽略此步骤）

查看命令如下：
```shell
$ rpm -qa | grep openjdk | grep -v grep
java-1.7.0-openjdk-1.7.0.75-2.5.4.2.el7_0.x86_64
java-1.6.0-openjdk-devel-1.6.0.34-1.13.6.1.el7_0.x86_64
java-1.7.0-openjdk-headless-1.7.0.75-2.5.4.2.el7_0.x86_64
java-1.6.0-openjdk-1.6.0.34-1.13.6.1.el7_0.x86_64
java-1.7.0-openjdk-devel-1.7.0.75-2.5.4.2.el7_0.x86_64
```

删除命令如下：
```shell
# rpm -e --nodeps java-1.7.0-openjdk-1.7.0.75-2.5.4.2.el7_0.x86_64
# rpm -e --nodeps java-1.6.0-openjdk-devel-1.6.0.34-1.13.6.1.el7_0.x86_64
# rpm -e --nodeps java-1.7.0-openjdk-headless-1.7.0.75-2.5.4.2.el7_0.x86_64
# rpm -e --nodeps java-1.6.0-openjdk-1.6.0.34-1.13.6.1.el7_0.x86_64
# rpm -e --nodeps java-1.7.0-openjdk-devel-1.7.0.75-2.5.4.2.el7_0.x86_64
```


下载安装并配置oracle的jdk
----
到官网网址[http://www.oracle.com/technetwork/java/javase/downloads/index.html](http://www.oracle.com/technetwork/java/javase/downloads/index.html)下载jdk-8u51-linux-x64.tar.gz，然后执行下面命令进行解压及安装：
```shell
# tar -zxvf jdk-8u51-linux-x64.tar.gz
# mv jdk1.8.0_51 /usr/java/jdk1.8.0_51
```

配置环境变量
```shell
# echo "export JAVA_HOME=/usr/java/jdk1.8.0_51" >> /etc/profile
# echo -e 'export CLASSPATH=.:$JAVA_HOME/jre/lib/rt.jar:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar'
# echo -e 'export PATH=$PATH:$JAVA_HOME/bin'
```


完整脚本
----
为方便以后配置使用，编写成脚本如下：

centos
```shell
#!/bin/bash

jdk_source=$1
if [[ -z $jdk_source ]]; then
    jdk_source=./jdk-8u51-linux-x64.tar.gz
fi

if [[ "$jdk_source" == "help" ]]; then
    echo "Usage: $0 [jdk_source_option]"
    echo "Example 1: $0"
    echo "Example 2: $0 /tmp/jdk-8u51-linux-x64.tar.gz"
    exit 0
fi

#for i in $(rpm -qa | grep openjdk | grep -v grep)
#do
#	echo "Delete rpm -> "$i
#	rpm -e -nodeps $i
#done

#if [[ ! -z $(rpm -qa | grep openjdk | grep -v grep) ]]; then
#	echo "--->Failed to remove openjdk"
#else
	echo "Check jdk source ..."
	if [[ ! -e $jdk_source ]]; then
	    echo "Jdk doesn't exist, start downloading ..."
	    wget --no-cookies --no-check-certificate --header "Cookie: gpw_e24=http%3A%2F%2Fwww.oracle.com%2F; oraclelicense=accept-securebackup-cookie" "http://download.oracle.com/otn-pub/java/jdk/8u51-b16/jdk-8u51-linux-x64.tar.gz"
	    jdk_source=./jdk-8u51-linux-x64.tar.gz
	    echo "Download jdk8 from oracle success."
	else
	    echo "Install jdk from source "$jdk_source
	fi

	echo "Check /usr/java directory exist ..."
	# 解压tar并安装到/usr/java中
	if [[ ! -e /usr/java ]]; then
	    mkdir /usr/java || exit 1
	fi

	echo "Check jdk1.8.0_51 directory exist ...."
	if [[ ! -e jdk1.8.0_51 ]]; then
	    tar -zxvf $jdk_source || exit 2
	fi

	echo "Move jdk1.8.0_51 to /usr/java"
	mv jdk1.8.0_51 /usr/java/jdk1.8.0_51 || exit 3

	# 配置java环境变量
	echo "setup java exvironment ..."
	echo "export JAVA_HOME=/usr/java/jdk1.8.0_51" >> /etc/profile
	echo -e 'export CLASSPATH=.:$CLASSPATH:$JAVA_HOME/jre/lib:$JAVA_HOME/lib' >> /etc/profile
	echo -e 'export PATH=$PATH:$JAVA_HOME/bin:$JAVA_HOME/jre/bin' >> /etc/profile

	echo "Reload source /etc/profile"
	source /etc/profile

	echo "Install success."
#fi
```

ubuntu
```shell
#!/bin/bash

jdk_source=$1
if [[ -z $jdk_source ]]; then
    jdk_source=./jdk-8u51-linux-x64.tar.gz
fi

if [[ "$jdk_source" == "help" ]]; then
    echo "Usage: $0 [jdk_source_option]"
    echo "Example 1: $0"
    echo "Example 2: $0 /tmp/jdk-8u51-linux-x64.tar.gz"
    exit 0
fi

if [ -z `which java | grep java` ]; then
    echo "Check jdk source ..."
    if [[ ! -e $jdk_source ]]; then
        echo "Jdk doesn't exist, start downloading ..."
        wget --no-cookies --no-check-certificate --header "Cookie: gpw_e24=http%3A%2F%2Fwww.oracle.com%2F; oraclelicense=accept-securebackup-cookie" "http://download.oracle.com/otn-pub/java/jdk/8u51-b16/jdk-8u51-linux-x64.tar.gz"
        jdk_source=./jdk-8u51-linux-x64.tar.gz
        echo "Download jdk8 from oracle success."
    else
        echo "Install jdk from source "$jdk_source
    fi

    echo "Check jdk1.8.0_51 directory exist ...."
    if [[ ! -e jdk1.8.0_51 ]]; then
        tar -zxvf $jdk_source || exit 1
    fi

    echo "Move jdk1.8.0_51 to /usr/java"
    mv jdk1.8.0_51 /opt/jdk1.8.0_51 || exit 2

    # 配置java环境变量
    echo "setup java exvironment ..."
    echo "export JAVA_HOME=/opt/jdk1.8.0_51" >> /etc/profile
    echo -e 'export CLASSPATH=.:$CLASSPATH:$JAVA_HOME/jre/lib:$JAVA_HOME/lib' >> /etc/profile
    echo -e 'export PATH=$PATH:$JAVA_HOME/bin:$JAVA_HOME/jre/bin' >> /etc/profile

    echo "Reload source /etc/profile"
    source /etc/profile

    echo "Install success."

else
    echo "Java has installed."
fi

```
