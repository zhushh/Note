安装前准备
----
* 检查是否已安装java环境

    参考[Java环境安装与配置](https://github.com/zhushh/Note/blob/master/note_of_distributed_course/java%E7%8E%AF%E5%A2%83%E5%AE%89%E8%A3%85%E4%B8%8E%E9%85%8D%E7%BD%AE.md)

安装eclipse
----

* 下载eclipse-luna版压缩包并解压

    ```
    $ wget http://ftp.yz.yamagata-u.ac.jp/pub/eclipse/technology/epp/downloads/release/luna/SR2/eclipse-java-luna-SR2-linux-gtk-x86_64.tar.gz
    $ sudo tar -zxvf eclipse-java-luna-SR1-linux-gtk-x86_64.tar.gz -C /opt/
    ```

* 创建链接目录

    ```
    $ sudo ln -s /opt/eclipse/eclipse /usr/bin/eclipse 
    ```
    
* 创建桌面启动器

    使用下面命令进行编辑
    ```
    $ vim /usr/share/applications/eclipse.desktop
    ```
    在文件中输入以下内容
    ```
    [Desktop Entry]
    Encoding=UTF-8
    Name=Eclipse 4.4.1
    Comment=Eclipse Luna
    Exec=/usr/bin/eclipse
    Icon=/opt/eclipse/icon.xpm
    Categories=Application;Development;Java;IDE
    Version=1.0
    Type=Application
    Terminal=0
    ```
    
* 完成安装

    在应用程序->编程里看一下是否有图标即可
 
