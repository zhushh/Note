---
name: webService学习.md
date: Tue 10 Jan 2017 03:06:32 PM CST
update: Tue 10 Jan 2017 03:06:32 PM CST
keyword: web service 
---


使用JDK发布WebSerivce
----

* 第一步： 创建项目

    使用下面命令创建HelloService项目
    ```
    $ mkdir -p HelloService/src/main/java/org/example
    ```

* 第二步：编写接口服务

    编写HelloService.java接口服务，保存文件到HelloService/src/main/java/org/example/HelloService.java
    ```java
    package org.example;

    import javax.jws.WebService;

    @WebService
    public interface HelloService {
        String say(String name);
    }
    ```

* 第三步：实现接口

    实现服务接口，保存下面代码到HelloService/src/main/java/org/example/HelloServiceImpl.java
    ```java
    package org.example;

    import javax.jws.WebService;

    @WebService(
        serviceName = "HelloService",
        portName = "HelloServicePort",
        endpointInterface = "org.example.HelloService"
    )
    public class HelloServiceImpl implements HelloService {
        public String say(String name) {
            return "Hello, " + name;
        }
    }
    ```

* 第四步：编写发布WebService的Server类

    为发布web service，我们实现下面的Server类，保存代码到HelloService/src/main/java/org/example/Server.java
    ```java
    package org.example;

    import javax.xml.ws.Endpoint;

    public class Server {
        public static void main(String[] args) {
            String address = "http://localhost:8080/ws/soap/hello";
            HelloService helloService = new HelloServiceImpl();

            Endpoint.publish(address, helloService);
            System.out.println("ws is published.");
        }
    }
    ```

* 第五步：编译运行

    在目录HelloService/src/main/java下，使用下面命令进行编译运行
    ```
    $ javac org/example/Server.java
    $ java org.example.Server
    ```
    此时终端会输出`ws is published.`，然后打开浏览器输入网址
    [http://localhost:8080/ws/soap/hello?wsdl](http://localhost:8080/ws/soap/hello?wsdl)，
    就可以看到输出的xml文件内容；


生成web service客户端，并在客户端调用WS
----

* 第一步： 生成web service客户端代码

    java安装好后自带wsimport工具，可以使用这个命令来生成客户端代码；
    先使用JDK发布web service，然后在信的窗口使用下面命令，生成WS客户端代码
    ```
    $ wsimport http://localhost:8080/ws/soap/hello?wsdl
    ```
    此时当前目录下就会生成一个org/example的目录，里面会有生成的class文件，通过下面命令进行jar包打包
    ```
    $ jar -cf client.jar org/
    ```
    这样就成功生成client.jar文件，这个文件在客户端会需要使用；

* 第二步：创建项目HelloServiceClient

    使用下面命令创建项目目录
    ```
    $ mkdir -p HelloServiceClient/src/main/java/org/example
    ```
    把第一步中的client.jar拷贝到 HelloServiceClient/src/main/java 目录下;后面编译运行会使用;

* 第三步： 添加客户端Client类

    编写Client客户端类，保存代码到 HelloServiceClient/src/main/java/org/example/Client.java
    ```java
    package org.example;

    public class Client {

        public static void main(String[] args) {
            HelloService_Service service = new HelloService_Service();

            HelloService helloService = service.getHelloServicePort();
            String result = helloService.say("world");
            System.out.println(result);
        }
    }
    ```

* 第四步： 编译运行Client类

    在目录HelloServiceClient/src/main/java下，使用下面命令进行编译Client类
    ```
    $ javac -classpath client.jar org/example/Client.java 
    ```
    编译成功后，使用下面命令运行Client类
    ```
    $ java -classpath .:client.jar org.example.Client 
    ```
    对于java萌新来说，上面的.:client.jar的`.`千万不能省略，不然会找不到Client类运行(ZZ)，运行成功可以看到下面输出
    ```
    Hello， World
    ```
    

通过动态代理类调用web service
----

* 第一步： 创建项目HelloServiceDynamicClient

    类似上面的创建项目命令，使用下面命令创建项目目录
    ```
    $ mkdir -p HelloServiceDynamicClient/src/main/java/org/example
    ```

* 第二步： 编写动态代理DynamicClient类

    保存下面代码到HelloServiceDynamicClient/src/main/java/org/example/DynamicClient.java
    ```java
    package org.example;

    import java.net.URL;
    import javax.xml.namespace.QName;
    import javax.xml.ws.Service;

    public class DynamicClient {

        public static void main(String[] args) {
            try {
                URL wsdl = new URL("http://localhost:8080/ws/soap/hello?wsdl");
                QName serviceName = new QName("http://example.org/", "HelloService");
                QName portName = new QName("http://example.org/", "HelloServicePort");
                Service service = Service.create(wsdl, serviceName);

                HelloService helloService = service.getPort(portName, HelloService.class);
                String result = helloService.say("world");
                System.out.println(result);
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
    }
    ```
    这个动态代理类需要本地提供HelloService.java这个接口，直接拷贝HelloService项目里的HelloService.java到
    HelloServiceDynamicClient/src/main/java/org/example/HelloService.java就可以；

* 第三步： 编译运行DynamicClient类

    先使用JDK发布web service，然后在 HelloServiceDynamicClient/src/main/java/目录下执行下面命令编译运行
    ```
    $ javac org.example.DynamicClient.java
    $ java org.example.DynamicClient
    ```
    可以看到下面的输出内容
    ```
    Hello, World
    ```


项目目录结构参考
----

```
webservice
|-- HelloService
|   `-- src
|       `-- main
|           `-- java
|               `-- org
|                   `-- example
|                       |-- HelloService.java
|                       |-- HelloServiceImpl.java
|                       `-- Server.java
|
|-- HelloServiceClient
|   `-- src
|       `-- main
|           `-- java
|               |-- client.jar
|               `-- org
|                   `-- example
|                       `-- Client.java
|
|-- HelloServiceDynamicClient
    `-- src
        `-- main
            `-- java
                `-- org
                    `-- example
                        |-- DynamicClient.java
                        `-- HelloService.java
```

参考阅读链接
----

[https://my.oschina.net/huangyong/blog/286155](https://my.oschina.net/huangyong/blog/286155)
