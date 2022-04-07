---
name: webService_02_web_service框架CXF技术学习.md
date: Fri 13 Jan 2017 01:35:10 PM CST
update: Fri 13 Jan 2017 01:35:10 PM CST
keyword: CXF CXF+Spring
---

CXF介绍
----

CXF是Apache的一个开源的WS（web service）框架，本身是整合了[Celtix](http://celtix.ow2.org/)
和[XFire](https://www.oschina.net/p/xfire)两个框架，Celtix是ESB框架，而XFire是一款WS框架;

* wiki链接： [https://en.wikipedia.org/wiki/Apache_CXF](https://en.wikipedia.org/wiki/Apache_CXF)

* 官网链接： [http://cxf.apache.org/](http://cxf.apache.org/)

CXF内置Jetty发布WS
----
以下介绍的例子是用apache-cxf的一个基础例子，详细可下载[apache-cxf](http://cxf.apache.org/download.html),
在${apache-cxf-dir}/samples/jax_rs/basic目录下的例子查看源代码;

* 第一步： 创建maven项目

    使用下面命令创建maven的项目目录：
    ```
    $ mkdir -p basic/src/main/java/demo/jaxrs/server
    ```
    
* 第二步： 配置项目pom.xml文件

    在项目目录basic下新建pom.xml文件，并复制下面内容保存
    ```xml
    <?xml version="1.0"?>
    <project xmlns="http://maven.apache.org/POM/4.0.0" 
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
        xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/maven-v4_0_0.xsd">
        <modelVersion>4.0.0</modelVersion>
        <groupId>demo.jaxrs</groupId>
        <artifactId>jax_rs_basic</artifactId>
        <version>1.0-SNAPSHOT</version>
        <name>JAX-RS Basic Demo</name>
        <description>JAX-RS Basic Demo</description>
    
        <properties>
            <cxf.version>${project.version}</cxf.version>
            <httpclient.version>3.1</httpclient.version>
        </properties>
        <profiles>
            <profile>
                <id>server</id>
                <build>
                    <defaultGoal>test</defaultGoal>
                    <plugins>
                        <plugin>
                            <groupId>org.codehaus.mojo</groupId>
                            <artifactId>exec-maven-plugin</artifactId>
                            <executions>
                                <execution>
                                    <phase>test</phase>
                                    <goals>
                                        <goal>java</goal>
                                    </goals>
                                    <configuration>
                                        <mainClass>demo.jaxrs.server.Server</mainClass>
                                    </configuration>
                                </execution>
                            </executions>
                        </plugin>
                    </plugins>
                </build>
            </profile>
        </profiles>
        <dependencies>
            <!-- cxf -->
            <dependency>
                <groupId>org.apache.cxf</groupId>
                <artifactId>cxf-rt-frontend-jaxrs</artifactId>
                <version>3.1.9</version>
            </dependency>
            <!-- This dependency is needed if you're using the Jetty container -->
            <dependency>
                <groupId>org.apache.cxf</groupId>
                <artifactId>cxf-rt-transports-http-jetty</artifactId>
                <version>3.1.9</version>
            </dependency>
        </dependencies>
    </project>
    ```
    
* 第三步： 添加java源代码

    依次新建下面各个java类： Customer.java, Order.java, Product.java, CustomerService.java, Server.java
    
    basic/src/main/java/demo/jaxrs/server/Customer.java
    ```java
    package demo.jaxrs.server;
    
    import javax.xml.bind.annotation.XmlRootElement;
    
    @XmlRootElement(name = "Customer")
    public class Customer {
        private long id;
        private String name;
    
        public long getId() {
            return id;
        }
    
        public void setId(long id) {
            this.id = id;
        }
    
        public String getName() {
            return name;
        }
    
        public void setName(String name) {
            this.name = name;
        }
    }
    
    ```
    
    basic/src/main/java/demo/jaxrs/server/Order.java
    ```java
    package demo.jaxrs.server;
    
    import java.util.HashMap;
    import java.util.Map;
    import javax.ws.rs.GET;
    import javax.ws.rs.Path;
    import javax.ws.rs.PathParam;
    
    import javax.xml.bind.annotation.XmlRootElement;
    
    @XmlRootElement(name = "Order")
    public class Order {
        private long id;
        private String description;
        private Map<Long, Product> products = new HashMap<Long, Product>();
    
        public Order() {
            init();
        }
    
        public long getId() {
            return id;
        }
    
        public void setId(long id) {
            this.id = id;
        }
    
        public String getDescription() {
            return description;
        }
    
        public void setDescription(String d) {
            this.description = d;
        }
    
        @GET
        @Path("products/{productId}/")
        public Product getProduct(@PathParam("productId")int productId) {
            System.out.println("----invoking getProduct with id: " + productId);
            Product p = products.get(new Long(productId));
            return p;
        }
    
        final void init() {
            Product p = new Product();
            p.setId(323);
            p.setDescription("product 323");
            products.put(p.getId(), p);
        }
    }
    ```
    
    basic/src/main/java/demo/jaxrs/server/Product.java
    ```java
    package demo.jaxrs.server;

    import javax.xml.bind.annotation.XmlRootElement;

    @XmlRootElement(name = "Product")
    public class Product {
        private long id;
        private String description;

        public long getId() {
            return id;
        }

        public void setId(long id) {
            this.id = id;
        }

        public String getDescription() {
            return description;
        }

        public void setDescription(String d) {
            this.description = d;
        }
    }
    ```
    
    basic/src/main/java/demo/jaxrs/server/CustomerService.java
    ```java
    package demo.jaxrs.server;
    
    import java.util.HashMap;
    import java.util.Map;
    
    import javax.ws.rs.DELETE;
    import javax.ws.rs.GET;
    import javax.ws.rs.POST;
    import javax.ws.rs.PUT;
    import javax.ws.rs.Path;
    import javax.ws.rs.PathParam;
    import javax.ws.rs.Produces;
    import javax.ws.rs.core.Response;
    
    @Path("/customerservice/")
    //@Produces("application/json") 
    @Produces("text/xml")
    public class CustomerService {
        long currentId = 123;
        Map<Long, Customer> customers = new HashMap<Long, Customer>();
        Map<Long, Order> orders = new HashMap<Long, Order>();
    
        public CustomerService() {
            init();
        }
    
        @GET
        @Path("/customers/{id}/")
        public Customer getCustomer(@PathParam("id") String id) {
            System.out.println("----invoking getCustomer, Customer id is: " + id);
            long idNumber = Long.parseLong(id);
            Customer c = customers.get(idNumber);
            return c;
        }
    
        @PUT
        @Path("/customers/")
        public Response updateCustomer(Customer customer) {
            System.out.println("----invoking updateCustomer, Customer name is: " + customer.getName());
            Customer c = customers.get(customer.getId());
            Response r;
            if (c != null) {
                customers.put(customer.getId(), customer);
                r = Response.ok().build();
            } else {
                r = Response.notModified().build();
            }
    
            return r;
        }
    
        @POST
        @Path("/customers/")
        public Response addCustomer(Customer customer) {
            System.out.println("----invoking addCustomer, Customer name is: " + customer.getName());
            customer.setId(++currentId);
    
            customers.put(customer.getId(), customer);
    
            return Response.ok(customer).build();
        }
    
        @DELETE
        @Path("/customers/{id}/")
        public Response deleteCustomer(@PathParam("id") String id) {
            System.out.println("----invoking deleteCustomer, Customer id is: " + id);
            long idNumber = Long.parseLong(id);
            Customer c = customers.get(idNumber);
    
            Response r;
            if (c != null) {
                r = Response.ok().build();
                customers.remove(idNumber);
            } else {
                r = Response.notModified().build();
            }
    
            return r;
        }
    
        @Path("/orders/{orderId}/")
        public Order getOrder(@PathParam("orderId") String orderId) {
            System.out.println("----invoking getOrder, Order id is: " + orderId);
            long idNumber = Long.parseLong(orderId);
            Order c = orders.get(idNumber);
            return c;
        }
    
        final void init() {
            Customer c = new Customer();
            c.setName("John");
            c.setId(123);
            customers.put(c.getId(), c);
    
            Order o = new Order();
            o.setDescription("order 223");
            o.setId(223);
            orders.put(o.getId(), o);
        }
    
    }
    ```
    
    basic/src/main/java/demo/jaxrs/server/Server.java
    ```java
    package demo.jaxrs.server;

    import org.apache.cxf.jaxrs.JAXRSServerFactoryBean;
    import org.apache.cxf.jaxrs.lifecycle.SingletonResourceProvider;

    // import org.codehaus.jackson.jaxrs.JacksonJsonProvider; // for JacksonJsonProvider

    public class Server {

        protected Server() throws Exception {
            JAXRSServerFactoryBean sf = new JAXRSServerFactoryBean();

            // // set response content-type to json
            // JacksonJsonProvider jsonProvider = new JacksonJsonProvider();
            // sf.setProvider(jsonProvider);

            sf.setResourceClasses(CustomerService.class);
            sf.setResourceProvider(CustomerService.class, 
                new SingletonResourceProvider(new CustomerService()));
            sf.setAddress("http://localhost:9000/");

            sf.create();
        }

        public static void main(String args[]) throws Exception {
            new Server();
            System.out.println("Server ready...");

            Thread.sleep(5 * 6000 * 1000);
            System.out.println("Server exiting");
            System.exit(0);
        }
    }
    ```

* 第四步： 使用maven编译运行

    使用下面命令进行编译运行Server类
    ```
    $ mvn -Pserver
    ```
    然后打开浏览器，输入地址： http://localhost:9000/customerservice/customers/123 可以看到输出内容如下：
    ```
    <Customer>
      <id>123</id>
      <name>John</name>
    </Customer>
    ```
    终端可以用curl命令来查看
    ```
    $ curl -v http://localhost:9000/customerservice/customers/123
    ```
    
    到这里基本上完成了使用apache-cxf的内置jetty发布web service了，不过目前的输出格式是xml的，现在很多web需要json的格式;
    所以下面讲一下如何使我们刚刚发布的web service也支持json的格式;

* 第五步： Json支持

    首先，修改pom.xml,添加下面的Json依赖库
    ```xml
        <dependency>
          <groupId>org.codehaus.jackson</groupId>
          <artifactId>jackson-jaxrs</artifactId>
          <version>1.9.13</version>
        </dependency>
    ```

    然后，修改CustomerService.java，把
    ```
    @Produces("text/xml")
    ```
    修改成
    ```
    @Produces("application/json")
    ```

    最后，修改Server.java代码，为JAXRSServerFactoryBean添加Provider，修改后代码如下
    ```java
    package demo.jaxrs.server;

    import org.apache.cxf.jaxrs.JAXRSServerFactoryBean;
    import org.apache.cxf.jaxrs.lifecycle.SingletonResourceProvider;

    import org.codehaus.jackson.jaxrs.JacksonJsonProvider; // for JacksonJsonProvider

    public class Server {

        protected Server() throws Exception {
            JAXRSServerFactoryBean sf = new JAXRSServerFactoryBean();

            // set response content-type to json
            JacksonJsonProvider jsonProvider = new JacksonJsonProvider();
            sf.setProvider(jsonProvider);

            sf.setResourceClasses(CustomerService.class);
            sf.setResourceProvider(CustomerService.class, 
                new SingletonResourceProvider(new CustomerService()));
            sf.setAddress("http://localhost:9000/");

            sf.create();
        }

        public static void main(String args[]) throws Exception {
            new Server();
            System.out.println("Server ready...");

            Thread.sleep(5 * 6000 * 1000);
            System.out.println("Server exiting");
            System.exit(0);
        }
    }
    ```
    使用命令`$ mvn clean -Pserver`运行Server，
    打开浏览器输入地址 http://localhost:9000/customerservice/customers/123 ，下面是看到的内容
    ```
    {"id":123,"name":"John"}
    ```
    终端下可输入命令
    ```
    $ curl -vH "Accepted: application/json" http://localhost:9000/customerservice/customers/123
    ```
    可看到下面输出
    ```
    *   Trying 127.0.0.1...
    * Connected to localhost (127.0.0.1) port 9000 (#0)
    > GET /customerservice/customers/123 HTTP/1.1
    > Host: localhost:9000
    > User-Agent: curl/7.47.0
    > Accept: */*
    > Accepted: application/json
    > 
    < HTTP/1.1 200 OK
    < Date: Fri, 13 Jan 2017 10:05:20 GMT
    < Content-Type: application/json
    < Transfer-Encoding: chunked
    < Server: Jetty(9.2.15.v20160210)
    < 
    * Connection #0 to host localhost left intact
    {"id":123,"name":"John"}
    ```

* 项目目录参考

    源代码： [https://github.com/zhushh/CodeForDestributedComputingCourse/tree/master/webservice/basic](https://github.com/zhushh/CodeForDestributedComputingCourse/tree/master/webservice/basic)
    ```
    basic
    |
    |-- src
    |   `-- main
    |       `-- java
    |           `-- demo
    |               `-- jaxrs
    |                   `-- server
    |                       |-- Customer.java
    |                       |-- CustomerService.java
    |                       |-- Order.java
    |                       |-- Product.java
    |                       `-- Server.java
    `-- pom.xml
    ```
