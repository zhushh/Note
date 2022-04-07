---
name: docker.md
date: 2017-02-28
update: 2017-03-01
keywords: docker
---

Docker目录
----
* Docker基本概念
    
    * 镜像
    * 容器
    * 仓库

* Docker安装

    * Centos安装
    * Ubuntu安装
    * 镜像加速器

* Docker基础命令

    * 获取镜像
    * 列出镜像
    * 操作容器
    
* 参考链接


Docker基本概念
----

* **镜像**
  
    操作系统分为内核空间和用户空间,对于linux系统,内核启动后会挂在root文件系统为其提供用户空间支持;
    Docker镜像就相当于一个root文件系统,除了提供容器运行时所需要的程序,库,资源,配置等文件之外,
    还包含一些为运行时准备的配置参数;
    
    **镜像的分层存储**
    
    Docker利用Union FS技术,将文件系统设计为分层存储架构;
    在这里,镜像并非像一个ISO那样打包的文件,镜像只是一个虚拟的概念,
    其实际体现并非一个文件组成,而是由一组文件系统组成,或者说由多层文件系统组成;
    
    镜像构建时,会一层层构建,前一层是后一层的基础,每一层构建完就不会发生改变,后一层的任何改变只发生在自己这一层;
    比如,删除前一层文件的操作,实际不是删除前一层的文件,而是仅仅在当前层标记该文件已删除;
    运行容器时,虽然看不到删除了的前一层文件,但是实际上该文件会一直跟随镜像;
    因此,在构建镜像时,每一层尽量只包含该层需要的东西,任何额外的东西都应该在构建结束前清理掉;
  
* **容器**

    在Docker中,镜像和容器的关系,就像面向对象语言中的类和实例一样,镜像是静态的定义,容器是镜像运行时的实体;
    容器可以被创建/启动/停止/删除/暂停等;
  
    容器的实质是进程,但与直接在宿主主机上面运行的进程不一样,容器进程运行于属于自己的[命名空间](https://en.wikipedia.org/wiki/Linux_namespaces);
    因此,容器可以有自己的root文件系统,自己的网络配置,自己的进程空间,甚至自己的用户Id空间;
    容器的进程运行在一个隔离的环境,使用起来就像独立于宿主主机的系统环境下,这种特性使得容器封装应用比直接在宿主运行更安全;
  
    **容器存储层**
  
    每一个容器运行时,都是以镜像为基础,在其上面创建一个当前容器的存储层;然后在这个存储层里进行读写,这个存储层被称为容器存储层;
    容器存储层的生命周期和容器一样,容器消亡时,这个存储层也就没了,因此,任何保存在容器存储层的数据信息会随着容器被删除而丢失;
    按Docker最佳实践要求,容器不应该在存储层内写入任何数据,容器存储层要保持无状态化,所有文件操作都使用数据卷(Volume)或者绑定宿主目录,
    这样就可以跳过容器存储层直接对宿主主机发生读写;数据卷的生存周期独立于容器,容器消亡,数据卷里的数据也不会消失,重启容器数据又可以恢复;
  
* **仓库**

    Docker registry服务是一种用于集中存储,分发镜像的服务;里面可以包含有多个仓库,仓库里包含有多个`标签`,每个标签对应一个镜像;
    一般一个仓库会包含同一个软件不同版本的镜像,而标签通常就是这些版本号,我们可以通过`<仓库名>:<标签>`来选择软件哪个版本的镜像,
    如果省略标签,默认是以`latest`为标签;以Ubuntu镜像为例:ubuntu就是仓库名,14.04和16.04就是标签,可以通过ubuntu:14.04来获取
    ubuntu 14.04的版本镜像;如果省略掉14.04,直接使用ubuntu,那么默认就是`ubuntu:latest`;
    
    **两段式路径**
    
    仓库名很多时候是两段式路径形式,例如: `jwilder/nginx-proxy`;一般前面一个是指Docker Registry的多用户环境下的用户名,
    后面一个是软件的仓库名;
    

Docker安装
----

* Centos安装

    因为安装Docker需要安装在x64位系统，内核版本不低于3.10，所以centos最低支持centos7；脚本安装命令如下：
    ```
    $ curl -sSL https://get.docker.com/ | sh
    ```
    因为墙的缘故，国内可以使用阿里云安装脚本：
    ```
    $ curl -sSL http://acs-public-mirror.oss-cn-hangzhou.aliyuncs.com/docker-engine/internet | sh -
    ```

* Ubuntu安装

    如上面所说，Docker需要安装在x84 64位的内核版本不低于3.10的系统上，所以如果内核版本太低，可以使用下面命令升级：

    ubuntu 12.04 LTS
    ```
    $ sudo apt-get install -y --install-recommends linux-generic-lts-trusty
    ```

    ubuntu 14.04 LTS
    ```
    $ sudo apt-get install -y --install-recommends linux-generic-lts-xenial
    ```

    脚本安装命令如下：
    ```
    $ curl -sSL https://get.docker.com/ | sh
    ```
    同样，若是被墙，使用阿里云脚本安装：
    ```
    $ curl -sSL http://acs-public-mirror.oss-cn-hangzhou.aliyuncs.com/docker-engine/internet | sh -
    ```

* 镜像加速器

    为了更快的访问docker hub，可以配置镜像加速器；国内有以下云服务商提供了加速服务：

    - [阿里云加速器](https://account.aliyun.com/)
    - [DaoCloud加速器](https://www.daocloud.io/mirror#accelerator-doc)

    注册用户并申请加速器，得到类似 `https://jxus37ad.mirror.aliyuncs.com` 的网址；

    **ubuntu14.04配置加速器**

    编辑/etc/default/docker文件，在`DOCKER_OPTS`中添加获得加速器配置`--registry-mirror=<加速器地址>`；如：
    ```
    DOCKER_OPTS="--registry-mirror=https://jxus37ad.mirror.aliyuncs.com"
    ```
    重启服务
     ```
    $ sudo service docker restart
    ```

    **ubuntu16.04、Centos7配置加速器**

    使用`systemctl enable docker`后，编辑`/etc/systemd/system/multi-user.target.wants/docker.service`文件，
    找到`ExecStart=`这一行，在后面添加加速器地址`--registry-mirror=<加速器地址>`;如：
    ```
    ExecStart=/usr/bin/dockerd --registry-mirror=https://jxus37ad.mirror.aliyuncs.com
    ```
    重新加载配置并且重启动
    ```
    $ sudo systemctl daemon-reload
    $ sudo systemctl restart docker
    ```


Docker基础命令
----

在学习下面的命令之前,我们需要先明白Docker在运行时分为Docker引擎(也就是服务器守护进程)和客户端工具;
Docker的引擎提供了一组REST API,被称为[Docker Remote API](https://docs.docker.com/engine/api/),
而`docker`命令是客户端工具,它通过这组API与Docker引擎交互,从而完成各种功能;因此,表面上我们在执行
docker的各种功能,但实际上一切都是使用远程调用形式在服务器端(Docker引擎)完成;正是因为这种C/S设计,
让我们操作远程服务器的Docker引擎变得轻而易举;


* **获取镜像**

    从Docker Register获取镜像的命令是`docker pull`,命令格式为:
    ```
    docker pull [选项] [Docker Register地址]<仓库名>:<标签>
    ```
    Docker Register地址: 地址格式是`<域名/IP>[:端口号]`,默认地址是Docker Hub;
    
    仓库名: 仓库名使用两段式名称,既`<用户名>/<软件名>`;对于Docker Hub,如果不给出用户名,默认为library;
    
    使用`docker pull --help`可以查看详细命令信息,下面是获取ubuntu 14.04的例子:
    ```
    $ docker pull ubuntu:14.04
    14.04:  Pulling from    library/ubuntu
    bf5d46315322:   Pull    complete
    9f13e0ac480c:   Pull    complete
    e8988b5b3097:   Pull    complete
    40af181810e7:   Pull    complete
    e6f7c7e5c03e:   Pull    complete
    Digest: sha256:147913621d9cdea08853f6ba9116c2e27a3ceffecf3b49298
    3ae97c3d643fbbe
    Status: Downloaded  newer   image   for ubuntu:14.04
    ```


* **列出镜像**
 
    想要列出已经下载下来的镜像,可以使用`docker images`命令:
    ```
    $ docker images
    REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
    ubuntu              14.04               7c09e61e9035        17 hours ago        188 MB
    ```
    列出的列表包含: 仓库名, 标签, 镜像ID, 创建时间, 大小;
    
    **虚悬镜像(dangling image)**
    
    这类镜像没有仓库名,也没有标签;可以使用下面命令专门显示虚悬镜像:
    ```
    $ docker images -f dangling=true
    ```
    虚悬镜像一般没有什么价值,可以使用下面命令删除掉:
    ```
    $ docker rmi $(docker images -q -f dangling=true)
    ```
    
    **中间层镜像**
    
    为了加速镜像构建和重复利用资源,Docker会利用中间层镜像;可以使用下面命令查看中间层镜像:
    ```
    $ docker images -a
    ```
    
    **列出部分镜像**
    
    不加任何参数,`docker images`会列出所有的顶级镜像;我们也可以只列出我们希望看到的镜像;例如:
    
    根据仓库名列出镜像或指定仓库名和标签
    ```
    $ docker images ubuntu
    $ docker images ubuntu:14.04
    ```
    
    使用`--filter`(简写是`-f`)进行过滤,例如列出`mongo:3.2`之后建立的镜像:
    ```
    $ docker images since=mongo:3.2
    ```
    若想看某个镜像之前的镜像,就把`since`换成`before`即可;
    如果镜像构建的时候定义了label,那么可以使用label进行过滤:
    ```
    $ docker images -f label=com.example.version=0.1
    ...
    ```
    
    使用`-q`参数只列出镜像的ID:
    ```
    $ docker images -q
    ```
    比较常用的组合就是`--filter`和`-q`;
    
    列出镜像ID和仓库名:
    ```
    $ docker images --format "{{.ID}}: {{.Repository}}"
    5f515359c7f8:   redis
    05a60462f8ba:   nginx
    fe9198c04d62:   mongo
    00285df0df87:   <none>
    f753707788c5:   ubuntu
    f753707788c5:   ubuntu
    1e0c3dd64ccd:   ubuntu
    ```


* **操作容器**

    **运行容器**
    
    有了镜像后,就可以使用`docker run`命令运行;以上面ubuntu:14.04为例:
    ```
    $ docker run -it --rm ubuntu:14.04 bash
    root@e7009c6ce357:/# cat /etc/os-release
    NAME="Ubuntu"
    VERSION="14.04.5    LTS,    Trusty  Tahr"
    ID=ubuntu
    ID_LIKE=debian
    PRETTY_NAME="Ubuntu 14.04.5 LTS"
    VERSION_ID="14.04"
    HOME_URL="http://www.ubuntu.com/"
    SUPPORT_URL="http://help.ubuntu.com/"
    BUG_REPORT_URL="http://bugs.launchpad.net/ubuntu/"
    root@e7009c6ce357:/# exit
    exit
    ```
    `-it`参数是两个参数,`-i`表示交互操作,`-t`是终端,因为我们打算进入`bash`,所以需要交互式终端;
    
    `--rm`参数的意思是,在容器运行结束的时候自动将其删除;
    
    `ubuntu:14.04`就是上面我们pull下来的镜像,这里就是使用这个镜像作为基础来运行容器;
    
    `bash`参数放在`ubuntu:14.04`镜像参数后面,是一个命令;
    
    运行容器后,我们便在镜像中启动了bash命令,然后输入了`cat /etc/os-release`和`exit`两个命令;

    **后台运行容器**
    
    另外,如果我们想启动一个容器,开启某一服务,然后在后台运行时,可以像这样执行:
    ```
    $ docker run --name webservice -d -p 81:80 nginx
    ```
    这条命令是指，用ｎｇｉｎｘ镜像(没有指定tag,默认是latest)运行一个容器，容器命名为ｗｅｂｓｅｒｖｉｃｅ，并且映射主机８1端口到容器的80端口，在浏览器输入 http://localhost 地址就可以访问到nginx服务器；
    
    `--name webservice`: 命名容器为webservice;
    
    `-d`: 后台运行;
    
    `-p 81:80`: 81是当前主机端口,80是镜像的端口,也就是把主机81端口映射到容器的80端口;
    
    **进入容器**
    
    上面启动的webservice容器我们是在后台运行的,现在想进去修改nginx的欢迎界面html;那么可以使用`docker exec`命令进入:
    ```
    $ docker exec -it webservice bash
    root@f649e877c035:/# echo '<h1>Hello, Docker</h1>' > /usr/share/nginx/html/index.html 
    root@f649e877c035:/# exit                 
    exit
    ```
    上面命令中,`docker exec`的参数`-it`是终端交互参数(因为我们要执行bash命令),webservice是容器名,bash是执行的命令;
    之后我们就进入到webservice容器中,执行了`echo`命令重定向输出到`/usr/share/nginx/html/index.html`文件中;
    现在打开浏览器 http://localhost/ 看到的内容就是`Hello, Docker`;
    
    我们也可以使用下面方式进入容器中:
    ```
    $ docker attach <container-name>
    ```
    例如,先启动一个后台运行的ubuntu:
    ```
    $ docker run -idt ubuntu:14.04
    ```
    然后,我们可以使用`docker ps`查看一下它的容器名:
    ```
    $ docker ps
    CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                         NAMES
    61bc61919df0        ubuntu:14.04        "/bin/bash"              5 seconds ago       Up 4 seconds                                      objective_raman
    960c831d71eb        nginx               "nginx -g 'daemon ..."   2 hours ago         Up 5 minutes        0.0.0.0:80->80/tcp, 443/tcp   webservice
    ```
    上面的`objective_raman`容器名就是刚刚创建的(你的可能跟我展示的不一样);然后在使用`docker attach`命令进入容器:
    ```
    $ docker attach objective_raman
    root@61bc61919df0:/#
    ```
    这样就进去容器了;
    
    **列出所有的容器**
    ```
    $ docker ps -a
    ```
    
    **列出正在运行的容器**
    ```
    $ docker ps
    ```

    **停止正在运行的容器**
    ```
    $ docker stop <container-name>
    ```
    例如,停止上面的webservice容器就是:
    ```
    $ docker stop webservice
    ```
    
    **启动已终止的容器**    
    ```
    $ docker start <container-name>
    ```
    例如,如果上面的webservice容器被停止了,那么浏览器就无法访问http://localhost地址,现在重启webservice容器:
    ```
    $ docker start webservice
    ```
    
    **删除容器**
    ```
    $ docker rm <container-name>
    ```
    这个命令并不会删除正在运行的容器,如果要删除正在运行的容器,那么需要使用`-f`参数;
    
    **清理所有处于终止状态的容器**
    ```
    $ docker rm $(docker ps -a -q)
    ```
    这个命令是利用`docker rm`不会删除正在运行的容器来删除所有处于终止状态的容器;


参考链接
----

* [docker git book](https://yeasy.gitbooks.io/docker_practice/content/)

