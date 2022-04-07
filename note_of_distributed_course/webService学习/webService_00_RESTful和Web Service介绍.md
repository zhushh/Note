---
name: webService_00_WebService介绍.md
date: Tue 10 Jan 2017 04:04:38 PM CST
update: 13 Jan 2017
keyword: REST RESTful web service
---


REST介绍
----

* 什么是REST

    REST（representational state transfer）,首次出现是2000年Roy Thomas Fielding的博文中，它是指一组架构约束条件和原则;
    满足这些条件和约束的就属于RESTful;

* 如何理解REST

    1.资源（Resource）
    ```
    任何可以被命名的信息都是资源，它可以是一个文本、图片、临时的服务、一组资源的集合、实体的对象等;
    每个资源都可以通过URI来定位;
    ```
    2.表现层（Representation）
    ```
    指的是资源的表现，一个资源可以有多种表示形式，比如可以是txt文本，也可以是http消息体，或者其他形式的表示;
    ```
    3.状态转移（State Transfer）
    ```
    这里的状态转移与状态机（state transition）里的可不相同，在客户端与服务端之间的转移代表资源的表述;
    通过状态转移和操作资源的表述，来间接的实现操作资源的目的;
    ```

* REST风格的架构的六个特征

    1.面向资源（Resource Oriented）: REST是以资源抽象为核心展开
    
    2.可寻址（Addressability）： 每一个资源在web上都有自己的地址
    
    3.连通性（Connectedness）： 避免设计孤立的资源，设计的时候除了设计资源本身，还应通过超链接将资源关联起来
    
    4.无状态（Statelessness）： 通信的会话状态（Session state）应该全由客户端负责维护
    
    5.统一接口（Uniform Interface）： 必须通过统一的接口来对资源执行各种操作，对于每个资源只能执行一组有限的操作
    
    6.超文本驱动（Hypertext Driven）： 又名“将超媒体作为应用状态的引擎”，将Web应用看作是一个由很多状态（应用状态）组成的有限状态机。资源之间通过超链接相互关联，超链接既代表资源之间的关系，也代表可执行的状态迁移。在超媒体之中不仅仅包含数据，还包含了状态迁移的语义。以超媒体作为引擎，驱动Web应用的状态迁移。通过超媒体暴露出服务器所提供的资源，服务器提供了哪些资源是在运行时通过解析超媒体发现的，而不是事先定义的。从面向服务的角度看，超媒体定义了服务器所提供服务的协议。客户端应该依赖的是超媒体的状态迁移语义，而不应该对于是否存在某个URI或URI的某种特殊构造方式作出假设。一切都有可能变化，只有超媒体的状态迁移语义能够长期保持稳定。

* 参考链接

    Infoq： [http://www.infoq.com/cn/articles/understanding-restful-style](http://www.infoq.com/cn/articles/understanding-restful-style)
    
    stackoverflow: [http://stackoverflow.com/questions/671118/what-exactly-is-restful-programming](http://stackoverflow.com/questions/671118/what-exactly-is-restful-programming)


Web Service介绍
----

* 什么是web service
    
    web服务，简写WS，基于web的服务；

* web service标准

    传统上web service标准主要由三个部分构成，分别是：

        1.简单对象访问协议（SOAP）
        一个基于XML的可扩展消息信封格式，需同时绑定一个网络传输协议。这个协议通常是HTTP或HTTPS，但也可能是SMTP或XMPP。

        2.web服务描述性语言（WSDL）
        一个XML格式文档，用以描述服务端口访问方式和使用协议的细节。通常用来辅助生成服务器和客户端代码及配置信息。

        3.统一描述、发现和集成（UDDI）
        一个用来发布和搜索WEB服务的协议，应用程序可藉由此协议在设计或运行时找到目标WEB服务。

* 参考阅读链接

    wiki： [https://en.wikipedia.org/wiki/Web_service](https://en.wikipedia.org/wiki/Web_service)

    博客: [https://my.oschina.net/lilw/blog/170518](https://my.oschina.net/lilw/blog/170518)

    java web service： [http://docs.oracle.com/javaee/6/tutorial/doc/gijti.html](http://docs.oracle.com/javaee/6/tutorial/doc/gijti.html)

    阮一峰博客： [http://www.ruanyifeng.com/blog/2009/08/what_is_web_service.html](http://www.ruanyifeng.com/blog/2009/08/what_is_web_service.html)


Restful Web Service 
----

* 什么是RESTful web service

    基于REST的web service就属于RESTful web service，restful web service相对于传统的web service来说更加轻量级;
    
* 参考链接

    wiki: [https://en.wikipedia.org/wiki/Representational_state_transfer](https://en.wikipedia.org/wiki/Representational_state_transfer)
    
    oracle: [http://docs.oracle.com/javaee/6/tutorial/doc/gijqy.html](http://docs.oracle.com/javaee/6/tutorial/doc/gijqy.html)
