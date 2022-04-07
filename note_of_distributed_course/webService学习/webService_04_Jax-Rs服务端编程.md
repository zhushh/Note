---
name: webService_04_Jax-Rs服务端编程.md
date: Fri 13 Jan 2017 01:38:22 PM CST
update: Fri 13 Jan 2017 01:38:22 PM CST
keyword: cxf jax-rs
---

JAX-RS服务端编程目录
----
* 根资源类

    * @Path
    * @GET,@PUT,@POST,@DELETE,...(HTTP Methods)
    * @Produces
    * @Consumes

* 参数注解(@*Param)
* 子资源
* 根资源的生命周期
* @Context
* 注入规则
* 参考链接


根资源类(Root Resources Classes)
----

根资源类，至少带有一个@Path的POJOs(Plain Old Java Objects)；
比如下面就是简单的hello world根资源类：
```java
package org.glassfish.jersey.examples.helloworld;

import javax.ws.rs.GET;
import javax.ws.rs.Path;
import javax.ws.rs.Produces;

@Path("helloworld")
public class HelloWorldResource {
    public static final String CLICHED_MESSAGE = "Hello, World!";

    @GET
    @Produces("text/html")
    public String getHello() {
        return CLICHED_MESSAGE;
    }
}
```

* @Path

    * 最简单的使用
        
        比如上面使用的`@Path("helloworld")`,直接把HelloWorldResource这个类映射到相对URI路径/helloworld

    * URI路径模板

        URI路径模板就是在URI中带有变量，下面大括号里面的`username`就是变量
        ```
        @Path("/users/{username}")
        ```
        如果想要在代码中使用`username`变量，可以像下面使用参数注解把`username`当做参数传进去
        ```java
        @Path("/users/{username}")
        public class UserResource {

            @GET
            @Produces("text/html")
            public String getUser(@PathParam("username") String userName) {
                ...
            }
        }
        ```
    
    * URI正则表达式

        有时候你可能需要对变量进行过滤，这时候就可以使用正则表达式，如下：
        ```
        @Path("/users/{username: [a-zA-Z][a-zA-Z_0-9]*}")
        ```

* HTTP Methods(@GET, @PUT, @POST, @DELETE, ...)

    @GET, @PUT, @POST, @DELETE, @HEAD等通常对应http协议的get, put, post, delete, head等方法；
    比如上面的HelloWorldResource类例子中，`@GET`就是用来处理http的get请求；
    又如，像下面这个例子就是使用@PUT注解来处理http的put请求：
    ```java
    @PUT
    public Response putContainer() {
        System.out.println("PUT CONTAINER " + container);

        URI uri = uriInfo.getAbsolutePath();
        Container c = new Container(container, uri.toString());

        Response r;
        if (!MemoryStore.MS.hasContainer(c)) {
            r = Response.create(uri).build();
        } else {
            r = Response.noContent().build();
        }

        MemoryStore.MS.createContainer(c);
        return r;
    }
    ```
    另外，JAX-RS在运行的时候通常默认会支持HEAD和OPTIONS方法；

* @Produces

    这个注解是用来说明返回给客户端的MIME类型的，例如使用`@Produces("text/plain")`就是返回"text/plain"的格式给客户端；`@Produces`这个注解可以用在类，也可以用在方法上面；比如下面例子：
    ```
    @Path("/myResource")
    @Produces("text/plain")
    public class SomeResource {
        @GET
        public String doGetAsPlainText() {
            ...
        }

        @GET
        @Produces("text/html")
        public String doGetAsHtml() {
            ...
        }
    }
    ```
    @Produces还可以声明多个类型返回，例如：
    ```
    @GET
    @Produces({"application/xml", "application/json"})
    public String doGetAsXmlOrJson() {
        ...
    }
    ```
    此时，如果"application/xml"和"application/json"都支持，那么前面的那种格式会被优先返回；
    如果get请求只接受"application/xml"或"application/json"的一种，那么被接受的那种格式就会被返回；

* @Consumes

    指定处理输入媒体的类型，例如"Content-Type: application/json".如果你的服务中函数带一个自由的参数，规定合适的输入provider，那么使用body中的内容，实例化这个参数。例如：
    ```
    @Post
    @Consumes("text/plain")
    public String sayHello(@PathParam("username") String userName, String letter) {
        return "hello " + userName + ":" + letter;
    }
    ```


参数注解(@*Param)
----

资源方法的参数可以使用参数注解从请求里面提取；
比如像上面使用`@PathParam`提取在`@Path`定义的`username`变量；
又如@QueryParam，这种是从QueryString或者Form中提取变量信息；
另外，还可以使用@DefaultValue 为变量制定默认值，比如下面代码：
```
@GET
@Path("girlfriend")
@Produces("text/html")
public String girlFriend(@PathParam("username") String userName, 
        @DefaultValue("Mary") @QueryParam("name") String name,
        @DefaultValue("123") @QueryParam("id") String id) {
    return "hello " + userName + ": your's gf is " + name;
}
```
参数注解还有很多种，比如从HTTP headers里面提取信息的@HeaderParam；
从cookies里面提取的信息的@CookieParam等；

* @FormParam
    
    从POST表单里面获取参数；比如下面代码：
    ```
    @POST
    @Path("/girlfriend")
    @Produces("text/html")
    public String girlFriendPost(@PathParam("username") String userName,
                    @FormParam("") Customer user ) {
            return "hello " + userName + ": your's gf is " + user.getName();
    }
    ```
    上面代码中会把表单定义成类，让系统自动实例化并填充；

* @BeanParam
    
    这个参数注解可以让我们自己定义类来获取参数信息；比如先定义下面的类：
    ```java
    public class MyBeanParam {
        @PathParam("p")
        private String pathParam;
     
        @MatrixParam("m")
        @Encoded
        @DefaultValue("default")
        private String matrixParam;
     
        @HeaderParam("header")
        private String headerParam;
     
        private String queryParam;
     
        public MyBeanParam(@QueryParam("q") String queryParam) {
            this.queryParam = queryParam;
        }
     
        public String getPathParam() {
            return pathParam;
        }
        ...
    }
    ```
    然后就可以使用下面的代码进行参数获取：
    ```
    @POST
    public void post(@BeanParam MyBeanParam beanParam, String entity) {
        final String pathParam = beanParam.getPathParam(); // contains injected path parameter "p"
        ...
    }
    ```
    在上面的例子中，我们把@PathParam, @QueryParam @MatrixParam 和 @HeaderParam 都集合进一个类里面，
    使用起来会比较灵活，但是不怎么简洁；


子资源(Sub-resources)
----

* 子资源方法

    `@Path`注解可以作用在类上面，同时还可以用在方法上，这时候这个方法就是子资源方法；我们可以看下面这个例子：
    ```java
    @Singleton
    @Path("/printers")
    public class PrintersResource {
     
        @GET
        @Produces({"application/json", "application/xml"})
        public WebResourceList getMyResources() { ... }
     
        @GET @Path("/list")
        @Produces({"application/json", "application/xml"})
        public WebResourceList getListOfPrinters() { ... }
     
        @GET @Path("/jMakiTable")
        @Produces("application/json")
        public PrinterTableModel getTable() { ... }
     
        @GET @Path("/jMakiTree")
        @Produces("application/json")
        public TreeModel getTree() { ... }
     
        @GET @Path("/ids/{printerid}")
        @Produces({"application/json", "application/xml"})
        public Printer getPrinter(@PathParam("printerid") String printerId) { ... }
     
        @PUT @Path("/ids/{printerid}")
        @Consumes({"application/json", "application/xml"})
        public void putPrinter(@PathParam("printerid") String printerId, Printer printer) { ... }
     
        @DELETE @Path("/ids/{printerid}")
        public void deletePrinter(@PathParam("printerid") String printerId) { ... }
    }
    ```

* 子资源定位器

    如果`@Path`是被用在没有被`@GET`或`@POST`等注解上的方法的资源方法，那么这个方法就是子资源定位器，看下面例子：
    ```java
    @Path("/item")
    public class ItemResource {
        @Context UriInfo uriInfo;
     
        @Path("content")
        public ItemContentResource getItemContentResource() {
            return new ItemContentResource();
        }
     
        @GET
        @Produces("application/xml")
            public Item get() { ... }
        }
    }
     
    public class ItemContentResource {
     
        @GET
        public Response get() { ... }
     
        @PUT
        @Path("{version}")
        public void put(@PathParam("version") int version,
                        @Context HttpHeaders headers,
                        byte[] in) {
            ...
        }
    }
    ```
    ItemResource类包含有子资源定位器方法`getItemContentResource`,用来返回一个新的资源类；


根资源的生命周期(Life-cycle of Root Resources Classes)
----

根资源的生命周期分为三种： Request scope，Per-lookup scope， Singleton；

|     Scope        | Annotation     | Description |
|------------------|----------------|-------------|
| Request scope    | @RequestScoped | 默认的生命周期，每个请求都会创建新的用来处理请求，在同一个请求中可重复使用 |
| Per-lookup scope | @PerLookup     | 每当需要使用这个类时就会创建一个实例，即使在同一个请求中也是 |
| Singleton        | @Singleton     | 在jar-rs应用中，这个类的实例只会被创建一次 |


@Context
----

`@Context`是注入上下文信息的注解，可以用来获取：Application，UriInfo，Request, HttpHeaders, SecurityContext, Providers等信息；
详细请阅读文档： [JAX-RS文档说明](http://download.oracle.com/otn-pub/jcp/jaxrs-2_0_rev_A-mrel-eval-spec/jsr339-jaxrs-2.0-final-spec.pdf?AuthParam=1487667458_ddc56bd853cf1725c656dc14387496b8)


注入规则(Rules of Injection)
----

* 注入规则的通常用法

    注入可以被作用于类成员变量、构造函数参数、资源类/子资源类/子资源定位器方法参数和bean的setter方法；看下面例子：
    ```java
    @Path("{id:\\d+}")
    public class InjectedResource {
        // Injection onto field
        @DefaultValue("q") @QueryParam("p")
        private String p;
     
        // Injection onto constructor parameter
        public InjectedResource(@PathParam("id") int id) { ... }
     
        // Injection onto resource method parameter
        @GET
        public String get(@Context UriInfo ui) { ... }
     
        // Injection onto sub-resource resource method parameter
        @Path("sub-id")
        @GET
        public String get(@PathParam("sub-id") String id) { ... }
     
        // Injection onto sub-resource locator method parameter
        @Path("sub-id")
        public SubResource getSubResource(@PathParam("sub-id") String id) { ... }
     
        // Injection using bean setter method
        @HeaderParam("X-header")
        public void setHeader(String header) { ... }
    }
    ```

* 注入规则在Singleton类型的限制

    对于Singleton类型的资源类，类的作用域内的变量和构造函数参数不能被注入；例如：
    ```java
    @Path("resource")
    @Singleton
    public static class MySingletonResource {
     
        @QueryParam("query")
        String param; // WRONG: initialization of application will fail as you cannot
                      // inject request specific parameters into a singleton resource.
     
        @GET
        public String get() {
            return "query param: " + param;
        }
    }
    ```
    上面的代码是不被允许的，不过我们可以使用`@Context`来进行注入；例如：
    ```java
    @Path("resource")
    @Singleton
    public static class MySingletonResource {
        @Context
        Request request; // this is ok: the proxy of Request will be injected into this singleton
     
        public MySingletonResource(@Context SecurityContext securityContext) {
            // this is ok too: the proxy of SecurityContext will be injected
        }
     
        @GET
        public String get() {
            return "query param: " + param;
        }
    }
    ```

* 注入规则的汇总

    | Java construct         | Description  |
    |------------------------|--------------|
    | Class field            | 直接注入到变量中，变量类型可以是private，但不能是final；注意Singleton类型 |
    | Constructor parameters | 调用构造函数，最大匹配的被调用， 注意Singleton类型 |
    | Resource methods       | 当方法被调用的时候可以注入变量，可以用在任何类型 |
    | Sub resources locators | 当子资源定位器被调用的时候，可以注入变量，可以用在任何类型 |
    | Setter methods         | 通过setter方法来注入变量值，只能被使用在@Context注解上 |

    下面是一个注入的例子，包含所有可以被注入的情况：
    ```java
    @Path("resource")
    public static class SummaryOfInjectionsResource {
        @QueryParam("query")
        String param; // injection into a class field
     
     
        @GET
        public String get(@QueryParam("query") String methodQueryParam) {
            // injection into a resource method parameter
            return "query param: " + param;
        }
     
        @Path("sub-resource-locator")
        public Class<SubResource> subResourceLocator(@QueryParam("query") String subResourceQueryParam) {
            // injection into a sub resource locator parameter
            return SubResource.class;
        }
     
        public SummaryOfInjectionsResource(@QueryParam("query") String constructorQueryParam) {
            // injection into a constructor parameter
        }
     
     
        @Context
        public void setRequest(Request request) {
            // injection into a setter method
            System.out.println(request != null);
        }
    }
     
    public static class SubResource {
        @GET
        public String get() {
            return "sub resource";
        }
    }
    ```


参考链接
----

* [JAX-RS文档](http://download.oracle.com/otn-pub/jcp/jaxrs-2_0_rev_A-mrel-eval-spec/jsr339-jaxrs-2.0-final-spec.pdf?AuthParam=1487667458_ddc56bd853cf1725c656dc14387496b8)（如果想要学习深一点，建议直接阅读这个文档）

* [https://jersey.java.net/documentation/latest/jaxrs-resources.html](https://jersey.java.net/documentation/latest/jaxrs-resources.html)

* [http://ss.sysu.edu.cn/~pml/webservices/5-jax-rs-std.html](http://ss.sysu.edu.cn/~pml/webservices/5-jax-rs-std.html)

* [http://docs.jboss.org/resteasy/docs/3.0.6.Final/userguide/html_single/index.html#_Context](http://docs.jboss.org/resteasy/docs/3.0.6.Final/userguide/html_single/index.html#_Context)
