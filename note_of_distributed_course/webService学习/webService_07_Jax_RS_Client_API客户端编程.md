---
name: webService_05_Jax-Rs客户端编程.md
date: Fri 13 Jan 2017 04:47:21 PM CST
update: Fri 13 Jan 2017 04:47:21 PM CST
keyword: 
---


JAX-RS Client API客户端编程目录
----

* 统一接口限制
* 更容易地使用和重复使用JAX-RS artifacts
* Client API简介
* Java实例和类型表示
* Client传输连接
* 使用Client 请求和响应过滤
* 关闭链接
* 保护客户端
* 代码例子
* 参考链接

统一接口限制
----

统一接口限制是为了使 RESTful 架构的web service具有清晰的界限，这样一个客户端（例如浏览器）就可以使
用相同的接口和任何的服务进行交流；在软件工程中，这是一个非常重要的概念，因为它使得基于web的搜索引擎和服务
可以统一；它包括下面特征：

    (1) 简单，架构容易理解和维护
    (2) 解耦，随着时间的演变，客户端和服务可以保持向后兼容
另外需要更多的限制：

    (1) 每一个资源都具有一个URI
    (2) 客户端通过HTTP请求和响应，使用特定的HTTP方法获取资源
    (3) 通过指定媒体类型，可以返回一种或者多种格式的表示
    (4) 内容可以链接到其他的资源
    
在JAX-RS client API里，资源是一个封装有URI的`WebTarget`类；这个类可以调用一组基于`WebTarget`的特定
的HTTP方法；


更容易地使用和重复使用JAX-RS artifacts
----

带参数的POST请求例子：
```java
Client client = ClientBuilder.newClient();
WebTarget target = client.target("http://localhost:9998").path("resource");

Form form = new Form();
form.param("x", "foo");
form.param("y", "bar");

MyJAXBBean bean = 
target.request(MediaType.APPLICATION_JSON_TYPE)
    .post(Entity.entity(form,MediaType.APPLICATION_FROM_URLENCODED_TYPE),
        MyJAXBBean.class);
```
上面的例子中，首先使用Client实例创建一个WebTarget实例，


Client API简介
----

* 开始使用Client API
    
    首先需要添加依赖，[详细链接](https://jersey.java.net/documentation/latest/modules-and-dependencies.html#dependencies);

* 创建和配置客户端(Client)实例

    最简单的创建方式如下：
    ```java
    Client client = ClientBuilder.newClient();
    ```

    ClientBuilder是JAX-RS的一个API，可以用于创建Client实例；它还可以配置 客户端（例如SSL传输设置）；
    另外一种配置客户端的方式是,在创建客户端的时候，通过传进一个`ClientConfig`类来进行配置；
    `ClientConfig`是`Configurable`的一种实现，`Configurable`提供了注册providers和设置properties的方法；

    下面代码展示如何注册providers：

    ```java
    ClientConfig clientConfig = new ClientConfig();
    clientConfig.register(MyClientResponseFilter.class);
    clientConfig.register(new AnotherClientFilter());
    Client client = ClientBuilder.newClient(clientConfig);
    ```
    上面的`MyClientResponseFilter`和`AnotherClientFilter`都是实现了`ClientRequestFilter`的自定义Filter；
    详细请参看 [JAX-RS文档](http://download.oracle.com/otn-pub/jcp/jaxrs-2_0_rev_A-mrel-eval-spec/jsr339-jaxrs-2.0-final-spec.pdf?AuthParam=1487667458_ddc56bd853cf1725c656dc14387496b8) 的
    第六章——Filters and Interceptors；

    Jersey支持函数式编程，所以我们可以这样子写上面的代码：
    
    ```java
    Client client = ClientBuilder.newClient(new ClientConfig()
        .register(MyClientResponseFilter.class)
        .register(new AnotherClientFilter()));
    ```

    properties也可以通过函数链来进行配置：
    ```java
    client.register(FilterA.class)
        .register(new FilterB())
        .property("my-property", true);
    ```

    如果想要获取当前客户端的配置信息，那么可以使用`getConfiguration()`方法获取：
    ```java
    ClientConfig clientConfig = new ClientConfig();
    clientConfig.register(MyClientResponseFilter.class);
    clientConfig.register(new AnotherClientFilter());
    Client client = ClientBuilder.newClient(clientConfig);
    client.register(ThirdClientFilter.class);
    Configuration newConfiguration = client.getConfiguration();
    ```

* 定位web resource

    有了客户端实例，我们就可以用它创建`WebTarget`：
    ```java
    WebTarget webTarget = client.target("http://example.com/rest");
    ```
    客户端包含有多种方式去创建一个 `WebTarget`；
    `WebTarget`也是实现了`Configurable`接口，所以我们可以为WebTarget注册providers：
    ```java
    WebTarget webTarget = client.target("http://example.com/rest");
    webTarget.register(FilterForExampleCom.class);
    ```

* 在WebTarget上识别资源

    WebTarget可以通过`path`方法派生出其他的 WebTarget 资源：
    ```java
    WebTarget resourceWebTarget = webTarget.path("resource");
    ```
    此时，resourceWebTarget 就指向新的web target，它的URI是"http://example.com/rest/resource";
    需要注意，WebTarget 的path方法会创建新的WebTarget实例，所以需要使用新的变量
    `resourceWebTarget`，假如我们现在想要访问resource资源下的helloWorld，那么就可以再创建
    新的WebTarget：
    ```java
    WebTarget helloWorldWebTarget = resourceWebTarget.path("helloWorld");
    ```
    有些URI中会有参数，我们可以使用`queryParam`方法设置参数：
    ```java
    WebTarget helloWorldWebTargetWithQueryParam = 
        helloWorldWebTarget.queryParam("greeting", "Hi World!");
    ```

* 调用Http请求

    客户端(Client)API里面提供了Invocation，这是一个接口，可以用来创建调用，然后再提交调用进行执行；
    也就是说请求调用这个过程分成了两步： 创建一个Invocation和提交Invocation；Invocation可以通过
    Invocation Builder进行创建：
    ```java
    Invocation.Builder invocationBuilder = 
        helloWorldWebTargetWithQueryParam.request(MediaType.TEXT_PLAIN_TYPE);
    invocationBuilder.header("some-header", "true");
    ```

    Invocation Builder 是用于配置请求的参数信息的，比如上面的some-header可以修改成cookie参数；
    创建好 Invocation Builder后，我们就可以发送请求：
    ```java
    Response response = invocationBuilder.get();
    ```

    我们可以打印出来看一下response：
    ```java
    System.out.println(response.getStatus());
    System.out.println(response.readEntity(String.class));
    ```

    另外，我们还可以使用post请求：
    ```java
    Response postResponse =
        helloWorldWebTarget.request(MediaType.TEXT_PLAIN_TYPE)
            .post(Entity.entity("A string entity to be POSTed", MediaType.TEXT_PLAIN_TYPE));
    ```

* 例子总结

    把上面例子的所有代码总结起来就是下面这样：
    ```java
    ClientConfig clientConfig = new ClientConfig();
    clientConfig.register(MyClientResponseFilter.class);
    clientConfig.register(new AnotherClientFilter());
     
    Client client = ClientBuilder.newClient(clientConfig);
    client.register(ThirdClientFilter.class);
     
    WebTarget webTarget = client.target("http://example.com/rest");
    webTarget.register(FilterForExampleCom.class);
    WebTarget resourceWebTarget = webTarget.path("resource");
    WebTarget helloworldWebTarget = resourceWebTarget.path("helloworld");
    WebTarget helloworldWebTargetWithQueryParam =
            helloworldWebTarget.queryParam("greeting", "Hi World!");
     
    Invocation.Builder invocationBuilder =
            helloworldWebTargetWithQueryParam.request(MediaType.TEXT_PLAIN_TYPE);
    invocationBuilder.header("some-header", "true");
     
    Response response = invocationBuilder.get();
    System.out.println(response.getStatus());
    System.out.println(response.readEntity(String.class));
    ```

    使用链式调用简化代码：
    ```java
    Client client = ClientBuilder.newClient(new ClientConfig()
        .register(MyClientResponseFilter.class)
        .register(new AnotherClientFilter()));

    String entity = client.target("http://example.com/rest")
                .register(FilterForExampleCom.class)
                .path("resource/helloworld")
                .queryParam("greeting", "Hi World!")
                .request(MediaType.TEXT_PLAIN_TYPE)
                .header("some-header", "true")
                .get(String.class);
    ```
    如果不需要设置参数和header，就使用下面这样编写：
    ```java
    String responseEntity = ClientBuilder.newClient()
                .target("http://example.com/rest").path("resource/helloworld")
                    .request().get(String.class);
    ```


Java实例和类型表示
----

服务器和客户端都支持Java的所有类型和表示；例如，你可以把响应当做字节流处理：
```java
InputStream in = response.readEntity(InputStream.class);
...  // Read from the stream
in.close();
```

下面演示使用File实例来提交一个文件：
```java
File f = ...
...
webTarget.request().post(Entity.entity(f, MediaType.TEXT_PLAIN_TYPE));
```


对客户端请求和响应进行过滤
----

在客户端的底层对请求和响应进行过滤，这样做，你可以在应用层上面专注其他方面的内容；
Filter不仅可以读取请求的URI、headers和entity，还可以读取响应的状态、headers和entity；

Jersey提供下面几种Filter可以使用：
```
CsrfProtectionFilter: 跨站请求(Cross-site)伪造保护过滤
EncodingFeature: 使用ContentEncode去编码和解码通信信息
HttpAuthenticationFeature: HTTP 认证
```


关闭链接
----

每个链接都会在请求(request)的时候打开，然后再收到响应(response)并进行处理后关闭掉；例如：
```java
final WebTarget target = ... // some web taregt
Response response = target.path("resource").request().get();
System.out.println("Connection is still open.");
System.out.println("string response: " + response.readEntity(String.class));
System.out.println("Now the connection is closed.");
```
如果你没有读取entity，那么就需要手动关闭链接`response.close()`；另外，如果entity是通过
InputStream读取，那么这个链接会一直保持链接直到完成InputStream的读取；



保护客户端
----

客户端(client)可以使用SSL进行加密；通过`ClientBuilder`我们就可以配置SSL，它提供了三
个方法： `KeyStore`, `TrustStore`和`SslContext`，看下面例子：
```java
SSLContext ssl = ... your configured SSL context;
Client client = ClientBuilder.newBuilder().sslContext(ssl).build();
Response response = client.target("https://example.com/resource").request().get();
```

使用`SslConfigurator`创建自定义的SSL:
```java
SslConfigurator sslConfig = SslConfigurator.newInstance()
    .trustStoreFile("./truststore_client")
    .trustStorePassword("secret-password-for-truststore")
    .keyStoreFile("./keystore_client")
    .keyPassword("secret-password-for-keystore");

SSLContext sslContext = sslConfig.createSSLContext();
Client client = ClientBuilder.newBuilder().sslContext(sslContext).build();
```


代码例子
----

[项目地址](https://github.com/zhushh/CodeForDestributedComputingCourse/tree/master/course_07/02)

查看src/main/java/demo/jaxrs/client/MyClient.java里面的代码即可;


参考链接
----

* [JAX-RS文档](http://download.oracle.com/otn-pub/jcp/jaxrs-2_0_rev_A-mrel-eval-spec/jsr339-jaxrs-2.0-final-spec.pdf?AuthParam=1487667458_ddc56bd853cf1725c656dc14387496b8)

* [JAX-RS所有的类](https://jersey.java.net/apidocs-javax.jax-rs/2.0.1/allclasses-noframe.html)

* [Jersey客户端的 Client API](https://jersey.java.net/documentation/latest/client.html)

