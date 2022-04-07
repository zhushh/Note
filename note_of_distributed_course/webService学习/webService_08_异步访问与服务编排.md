---
name: webService_08_异步访问与服务编排.md
date: 2017-02-22
update: 2017-02-22
keywords: 
---


异步访问与实时交互客户端编程目录
----

* 异步访问
* 实时交互客户端(Reactive Client)扩展的目的
* 实时交互客户端API的用法
* 支持的Reactive库
* 实时交互客户端使用例子
* 参考链接


异步访问
----

JAX-RS的默认情况下是使用同步访问的方式,要使用异步访问,就需要调用`async`方法;
例如,下面是一段使用异步调用的例子:
```java
Client client = ClientBuilder.newClient();
WebTarget target = client.target("http://example.com/customers/{id}");
target.resolveTemplate("id", 123).request().async().get(
    new InvocationCallBack<Customer>() {
        @Override
        public void completed(Customer customer) {
            // Do something
        }
        @Override
        public void failed(Throwable throwable) {
            // Process error
        }
    });
```
在上面代码中,get调用之后会立刻返回,并不会阻塞线程的继续运行;
如果调用成功,那么completed的代码会被执行;
如果调用失败,那么failed方法将会被执行;

所有的异步调用返回的实例都是`Future<T>`类型,其中`T`是由InvocationCallBack指定;
返回的Future<T>实例可以用于监听或者取消异步调用,例如:
```java
Future<Customer> ff = target.resolveTemplate("id", 123).request().async()
    .get(new InvocationCallBack<Customer>() {
        @Override
        public void completed(Customer customer) {
            // Do something 
        }

        @Override
        public void failed(Throwable throwable) {
            // Process error
        }
    });

// After waiting for a while ...
if (!ff.isDone()) {
    ff.cancel(true);
}
```
虽然在执行异步调用的时候,建议是传进 InvocationCallBack 的实例,但是这并不是强制性的;
通过调用返回的Future<T>,我们可以使用`Future.get`方法去访问响应(response),
得到的返回值要么是T类型(表示调用成功),要么是null(表示调用失败);


实时交互客户端(Reactive Client)扩展的目的
----

实时交互编程可以更方便的开发异步编程;它是基于数据流和变化传播的;

而且使用实时交互的方法,也使得代码更容易去维护,编写和阅读;

参看例子: [Reactive Jersey Client, Part 1 – Motivation](https://blog.dejavu.sk/2015/01/07/reactive-jersey-client-part-1-motivation/)


实时交互客户端API的用法
----

交互式客户端API提供了跟JAX-RS的客户端API相似的API接口,它是基于现有的JAX-APIs的一些扩展;

HTTP请求的同步调用如下:
```java
Response response = ClientBuilder.newClient()
                    .target("http://example.com/resource")
                    .request()
                    .get();
```
异步调用如下:
```java
Future<Response> response = ClientBuilder.newClient()
        .target("http://example.com/resource")
        .request()
        .async()
        .get();
```
上面我们就可以看到,异步调用仅仅只是在同步调用的基础上添加了一个`async`方法;
所以,为了方便使用,交互式客户端也是跟异步调用用法类似,只是我们把`async`方法替换成`rx`方法;
例如:
```java
Obervable<Response> response = Rx.newClient(RxObservable.class)
        .target("http://example.com/resource")
        .request()
        .rx()
        .get();
```

使用此扩展需要添加的maven依赖:
```
<dependency>
    <groupId>org.glassfish.jersey.ext.rx</groupId>
    <artifactId>jersey-rx-client</artifactId>
    <version>2.25.1</version>
</dependency>
```


支持的Reactive库
----

* RxJava - Observable

    这个扩展是由Netflix贡献的,算是目前Java里面最高级的交互式库(Reactive library);

    项目的maven依赖:
    ```
    <dependency>
        <groupId>org.glassfish.jersey.ext.rx</groupId>
        <artifactId>jersey-rx-client-rxjava</artifactId>
        <version>2.25.1</version>
    </dependency>
    ```

    创建Rx Java 客户端和WebTarget
    ```java
    // New Client
    RxClient<RxObservableInvoker> newRxClient = Rx.newClient(RxObservableInvoker.class);

    // From exiting Client
    RxClient<RxObservableInvoker> rxClient = Rx.from(client, RxObservableInvoker.class);

    // From existing WebTarget
    RxTarget<RxObservableInvoker> rxWebTarget = Rx.from(target, RxObservableInvoker.class);
    ```

    如果你是想使用RxObservable入口点时,你可以跳过Invoker的类型:
    ```java
    // New Client
    RxClient<RxObservableInvoker> newRxClient = RxObservable.newClient();

    // From existing Client
    RxClient<RxObservableInvoker> rxClient = RxObservable.from(client);

    // From existing WebTarget
    RxTarget<RxObservableInvoker> rxWebTarget = RxObservable.from(target);
    ```

    获取Observable的调用方法:
    ```java
    Observable<Response> observable = RxObservable.newClient()
            .target("http://example.com/resource")
            .request()
            .rx()
            .get();
    ```


* Java 8 - CompletionStage and CompletableFuture

    Java 8原生就是支持基于事件驱动或异步编程,主要有两个类型接口: CompletionStage 和 CompletionFuture;
    这些类型可以被绑定到Stream中,就可以实现和RxJava一样的功能;

    项目的maven依赖:
    ```
    <dependency>
        <groupId>org.glassfish.jersey.ext.rx</groupId>
        <artifactId>jersey-rx-client-java8</artifactId>
        <version>2.25.1</version>
    </dependency>
    ```
    

    使用Java 8创建客户端和WebTarget:
    ```java
    // New Client
    RxClient<RxCompletionStageInvoker> newRxClient = Rx.newClient(RxCompletionStageInvoker.class);

    // From existing Client
    RxClient<RxCompletionStageInvoker> rxClient = Rx.from(client, RxCompletionStageInvoker.class);

    // From existing WebTarget
    RxTarget<RxCompletionStageInvoker> rxWebTarget = Rx.from(target, RxCompletionStageInvoker.class);
    ```

    使用 RxCompletionStageInvoker入口点跳过指定invoker类型来创建客户端和WebTarget:
    ```java
    // New Client
    RxClient<RxCompletionStageInvoker> newRxClient = RxCompletionStage.newClient();
     
    // From existing Client
    RxClient<RxCompletionStageInvoker> rxClient = RxCompletionStage.from(client);
     
    // From existing WebTarget
    RxTarget<RxCompletionStageInvoker> rxWebTarget = RxCompletionStage.from(target);
    ```

    获取CompletionStage的调用方法:
    ```java
    CompletionStage<Response> stage = RxCompletionStage.newClient()
                .target("http://example.com/resource")
                .request()
                .rx()
                .get();
    ```

* Guava - ListenableFuture and Futures

    由Google支持贡献的Reactive库;

    maven项目依赖:
    ```
    <dependency>
        <groupId>org.glassfish.jersey.ext.rx</groupId>
        <artifactId>jersey-rx-client-guava</artifactId>
        <version>2.25.1</version>
    </dependency>
    ```

    使用Guava创建客户端和WebTarget:
    ```java
    // New Client
    RxClient<RxListenableFutureInvoker> newRxClient = Rx.newClient(RxListenableFutureInvoker.class);

    // From existing Client
    RxClient<RxListenableFutureInvoker> rxClient = Rx.from(client, RxListenableFutureInvoker.class);

    // From existing WebTarget
    RxTarget<RxListenableFutureInvoker> rxWebTarget = Rx.from(target, RxListenableFutureInvoker.class);
    ```

    不指定invoker类型:
    ```java
    // New Client
    RxClient<RxListenableFutureInvoker> newRxClient = RxListenableFuture.newClient();
     
    // From existing Client
    RxClient<RxListenableFutureInvoker> rxClient = RxListenableFuture.from(client);
     
    // From existing WebTarget
    RxTarget<RxListenableFutureInvoker> rxWebTarget = RxListenableFuture.from(target);
    ```

    获取ListenableFuture的调用方式:
    ```java
    ListenableFuture<Response> stage = RxListenableFuture.newClient()
            .target("http://example.com/resource")
            .request()
            .rx()
            .get();
    ```

* JSR-166e - CompletableFuture

    如果Java 8不够理想,但是又需要使用CompletionStage和CompletionFuture时,就可以使用JSP 166库;

    项目maven依赖:
    ```
    <dependency>
        <groupId>org.glassfish.jersey.ext.rx</groupId>
        <artifactId>jersey-rx-client-jsr166e</artifactId>
        <version>2.25.1</version>
    </dependency>
    ```

    创建客户端和WebTarget:
    ```java
    // New Client
    RxClient<RxCompletableFutureInvoker> newRxClient = Rx.newClient(RxCompletableFutureInvoker.class);

    // From existing Client
    RxClient<RxCompletableFutureInvoker> rxClient = Rx.from(client, RxCompletableFutureInvoker.class);

    // From existing WebTarget
    RxTarget<RxCompletableFutureInvoker> rxWebTarget = Rx.from(target, RxCompletableFutureInvoker.class);
    ```

    不指定invoker的方式:
    ```java
    // New Client
    RxClient<RxCompletableFutureInvoker> newRxClient = RxCompletableFuture.newClient();
     
    // From existing Client
    RxClient<RxCompletableFutureInvoker> rxClient = RxCompletableFuture.from(client);
     
    // From existing WebTarget
    RxTarget<RxCompletableFutureInvoker> rxWebTarget = RxCompletableFuture.from(target);
    ```

    调用方式:
    ```java
    CompletableFuture<Response> stage = RxCompletableFuture.newClient()
            .target("http://example.com/resource")
            .request()
            .rx()
            .get();
    ```


实时交互客户端使用例子
----

* [Travel Agency (Orchestration Layer) Example using Reactive Jersey Client API](https://github.com/jersey/jersey/tree/2.25.1/examples/rx-client-webapp)

* [Travel Agency (Orchestration Layer) Example using Reactive Jersey Client API (Java 8)](https://github.com/jersey/jersey/tree/2.25.1/examples/rx-client-java8-webapp)


参考链接
----

* [JAX-RS文档](http://download.oracle.com/otn-pub/jcp/jaxrs-2_0_rev_A-mrel-eval-spec/jsr339-jaxrs-2.0-final-spec.pdf
?AuthParam=1487667458_ddc56bd853cf1725c656dc14387496b8)

* [Jersey Reactive Client API](https://jersey.java.net/documentation/latest/rx-client.html)
