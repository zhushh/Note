#### 安装

- 下载Go发行版

  Go的官方网址是: [https://golang.org/dl/](https://golang.org/dl/)

  ```
  wget https://dl.google.com/go/go1.10.4.linux-amd64.tar.gz
  ```

  

- 提取压缩包

  提取压缩包到合适的目录：

  ```
  sudo tar -xzf go1.10.4.linux-amd64.tar.gz -C /usr/local
  ```

  

- 建立软连接

  ```
  sudo ln -s /usr/local/go/bin/* /usr/bin
  ```

  然后执行`go version`查看是否安装成功。



#### 配置环境变量

修改`~/.bashrc`文件，进行下面配置：

```
export GOROOT=/usr/local/go  #设置为go安装的路径，有些安装包会自动设置默认的goroot
export GOPATH=$HOME/go-workspace   #默认安装包的路径
export PATH=$PATH:$GOROOT/bin:$GOPATH/bin
```

然后，运行`go env`查看go环境变量



#### 卸载

- 删除go目录

  ```
  sudo rm -rf /usr/local/go
  ```

  

- 删除软链接

  ```
  sudo rm -rf /usr/bin/go
  ```

  



#### 升级

升级Go版本其实就是：

1.卸载之前安装的旧版本

2.再安装重新下载的Go版本

