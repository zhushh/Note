---
name: webService_03_使用Spring和Cxf发布WS.md
date: 2017-01-13
update: 2017-01-13
keywords: spring cxf web service
---


Spring+Cxf发布restful web service
----

* 第一步： 新建Maven项目，并配置pom.xml

    使用maven命令创建webapp项目（不熟悉maven的可以看下 [maven简单命令](https://github.com/zhushh/Note/blob/master/maven%E6%8A%80%E6%9C%AF%E5%AD%A6%E4%B9%A0.md#maven-%E5%B8%B8%E7%94%A8%E5%91%BD%E4%BB%A4) ）
    ```
    $ mvn -B archetype:generate -DarchetypeGroupId=org.apahce.maven.archetypes \
    -DarchetypeArtifactId=maven-archetype-webapp \
    -DgroupId=demo.ws \
    -DartifactId=Spring_Cxf_example
    ```
    
    然后把下面的项目配置信息覆盖掉pom.xml中原来的内容
    ```xml
    <project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/maven-v4_0_0.xsd">
        <modelVersion>4.0.0</modelVersion>
        <groupId>demo.ws</groupId>
        <artifactId>rest_spring_cxf</artifactId>
        <packaging>war</packaging>
        <version>1.0-SNAPSHOT</version>
    
        <!-- 申明常用软件的版本 -->
        <properties>
                <jettyVersion>9.3.7.v20160115</jettyVersion>
                <cxf.version>3.1.6</cxf.version>
                <jackson.version>2.4.1</jackson.version>
        </properties>
        
        <dependencies>
            <!-- CXF jaxrs 依赖 -->
            <dependency>
                <groupId>org.apache.cxf</groupId>
                <artifactId>cxf-rt-transports-http</artifactId>
                <version>${cxf.version}</version>
            </dependency>
            <dependency>
                <groupId>org.apache.cxf</groupId>
                <artifactId>cxf-rt-frontend-jaxrs</artifactId>
                <version>${cxf.version}</version>
            </dependency>
    
            <!-- CXF jaxrs description 依赖 -->
            <dependency>
                <groupId>org.apache.cxf</groupId>
                <artifactId>cxf-rt-rs-service-description</artifactId>
                <version>${cxf.version}</version>
            </dependency>
    
            <!-- spring 依赖 -->
            <dependency>
                <groupId>org.springframework</groupId>
                <artifactId>spring-web</artifactId>
                <version>3.2.8.RELEASE</version>
            </dependency>
    
            <!-- Jackson -->
            <dependency>
                <groupId>com.fasterxml.jackson.jaxrs</groupId>
                <artifactId>jackson-jaxrs-json-provider</artifactId>
                <version>${jackson.version}</version>
            </dependency>
    
        </dependencies>
        <build>
            <finalName>cxf-rs-spring</finalName>
            <!-- jetty:run 插件 -->
            <plugins>
                <plugin>
                    <groupId>org.eclipse.jetty</groupId>
                    <artifactId>jetty-maven-plugin</artifactId>
                    <version>${jettyVersion}</version>
                </plugin>
            </plugins>
        </build>
    </project>
    ```
    
* 第二步： 配置web.xml

    编辑web.xml文件，用下面内容替代
    ```xml
    <?xml version="1.0" encoding="UTF-8"?>
    <web-app xmlns="http://java.sun.com/xml/ns/javaee"
             xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
             xsi:schemaLocation="http://java.sun.com/xml/ns/javaee
             http://java.sun.com/xml/ns/javaee/web-app_3_0.xsd"
             version="3.0">
    
        <!-- Spring -->
        <context-param>
            <param-name>contextConfigLocation</param-name>
            <param-value>classpath:spring.xml</param-value>
        </context-param>
        <listener>
            <listener-class>org.springframework.web.context.ContextLoaderListener</listener-class>
        </listener>
    
        <!-- CXF -->
        <servlet>
            <servlet-name>cxf</servlet-name>
            <servlet-class>org.apache.cxf.transport.servlet.CXFServlet</servlet-class>
        </servlet>
        <servlet-mapping>
            <servlet-name>cxf</servlet-name>
            <url-pattern>/ws/*</url-pattern>
        </servlet-mapping>
    
    </web-app>  
    ```
    这里配置的信息是，使用Spring中的contextConfigLocation去加载Spring的配置文件spring.xml;
    使用CXF提供的CXFServlet去处理/ws/的REST请求;
    
* 第三步： 添加java源代码

    先创建java源代码目录,在Sprng_Cxf_example目录下执行
    ```
    $ mkdir -p src/main/java/demo/ws/rest_spring_cxf
    ```
    然后依次新建这些java源代码： 
    
        src/main/java/demo/ws/rest_spring_cxf/Product.java 
        src/main/java/demo/ws/rest_spring_cxf/ProductService.java 
        src/main/java/demo/ws/rest_spring_cxf/ProductServiceImpl.java
    
    具体代码，在这里省略，后面会给出项目源代码;
    ```java
    package demo.ws.rest_spring_cxf;

    import java.lang.reflect.Field;
    import java.util.ArrayList;
    import java.util.Collections;
    import java.util.Comparator;
    import java.util.Date;
    import java.util.Iterator;
    import java.util.List;
    import java.util.Map;
    import org.springframework.stereotype.Component;

    @Component
    public class ProductServiceImpl implements ProductService {
        ...
    }
    ```
    上面这里使用Spring的@Component注解，把ProductServiceImpl这个类发布为Spring Bean;
    
* 第四步： 配置spring

    这里是 src/main/resources/spring.xml 的配置
    ```xml
    <?xml version="1.0" encoding="UTF-8"?>
    <beans xmlns="http://www.springframework.org/schema/beans"
           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
           xmlns:context="http://www.springframework.org/schema/context"
           xsi:schemaLocation="http://www.springframework.org/schema/beans
           http://www.springframework.org/schema/beans/spring-beans-4.0.xsd
           http://www.springframework.org/schema/context
           http://www.springframework.org/schema/context/spring-context-4.0.xsd">

        <context:component-scan base-package="demo.ws"/>

        <import resource="spring-cxf.xml"/>

    </beans>
    ```
    配置描述的是，通过扫描demo.ws这个包，Spring可以访问这个包里面的所有Spring Bean，比如上一步使用@Component注解发布的ProductServiceImpl;
    另外，`<import>`这个配置加载了spring-cxf.xml的内容;下面是 src/main/resources/spring-cxf.xml 的配置
    ```xml
    <!-- spring-cxf.xml -->
    <?xml version="1.0" encoding="UTF-8"?>
    <beans xmlns="http://www.springframework.org/schema/beans"
           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
           xmlns:jaxrs="http://cxf.apache.org/jaxrs"
           xsi:schemaLocation="http://www.springframework.org/schema/beans
           http://www.springframework.org/schema/beans/spring-beans-4.0.xsd
           http://cxf.apache.org/jaxrs
           http://cxf.apache.org/schemas/jaxrs.xsd">

        <jaxrs:server address="/rest">
            <jaxrs:serviceBeans>
                <ref bean="productServiceImpl"/>
            </jaxrs:serviceBeans>
            <jaxrs:providers>
                <bean class="com.fasterxml.jackson.jaxrs.json.JacksonJsonProvider"/>
            </jaxrs:providers>
        </jaxrs:server>

        <bean id="productServiceImpl" class="demo.ws.rest_spring_cxf.ProductServiceImpl"></bean>
    </beans>
    ```
    使用CXF提供的Spring命名空间来配置Service Bean和Provider;其中server的address属性为`/rest`表示REST请求的相对路径，
    与web.xml里面的`/ws/*`配置结合起来，就是最终的REST的请求的根路径`/ws/rest`; 而在ProductService类里面使用的@Path注解
    所配置的只是一个相对路径;
    
* 第五步： 调用REST服务

    编写一个简单的html页面代码 src/main/webapp/product.html 来调用REST
    ```html
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Demo</title>
        <link href="http://cdn.bootcss.com/bootstrap/3.1.1/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body>

    <div class="container">
        <div class="page-header">
            <h1>Product</h1>
        </div>
        <div class="panel panel-default">
            <div class="panel-heading">Product List</div>
            <div class="panel-body">
                <div id="product"></div>
            </div>
        </div>
    </div>

    <script src="http://cdn.bootcss.com/jquery/2.1.1/jquery.min.js"></script>
    <script src="http://cdn.bootcss.com/bootstrap/3.1.1/js/bootstrap.min.js"></script>
    <script src="http://cdn.bootcss.com/handlebars.js/1.3.0/handlebars.min.js"></script>

    <script type="text/x-handlebars-template" id="product_table_template">
        {{#if data}}
            <table class="table table-hover" id="product_table">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Product Name</th>
                        <th>Price</th>
                    </tr>
                </thead>
                <tbody>
                    {{#data}}
                        <tr data-id="{{id}}" data-name="{{name}}">
                            <td>{{id}}</td>
                            <td>{{name}}</td>
                            <td>{{price}}</td>
                        </tr>
                    {{/data}}
                </tbody>
            </table>
        {{else}}
            <div class="alert alert-warning">Can not find any data!</div>
        {{/if}}
    </script>

    <script>
        $(function() {
            $.ajax({
                type: 'get',
                url: 'http://localhost:8080/ws/rest/products',
                dataType: 'json',
                success: function(data) {
                    var template = $("#product_table_template").html();
                    var render = Handlebars.compile(template);
                    var html = render({
                        data: data
                    });
                    $('#product').html(html);
                }
            });
        });
    </script>

    </body>
    </html>
    ```
    这里是前端的页面，使用ajax来发送请求调用后台的REST服务;
    使用JQuery、Boostrap、Handlebars.js等技术，不懂也没关系（有兴趣可以了解一下）;
    
* 第六步： 编译运行项目

    使用下面命令进行编译运行REST服务
    ```
    $ mvn compile
    $ mvn jetty:run
    ```
    打开浏览器输入 http://localhost:8080/product.html 即可看到页面;

* 项目目录参考及源代码

    项目源代码： [https://github.com/zhushh/CodeForDestributedComputingCourse/tree/master/webservice/Spring_Cxf_example](https://github.com/zhushh/CodeForDestributedComputingCourse/tree/master/webservice/Spring_Cxf_example)
    ```
    Spring_Cxf_example
    |-- src
    |   `-- main
    |       |-- java
    |       |   `-- demo
    |       |       `-- ws
    |       |           `-- rest_spring_cxf
    |       |               |-- Product.java
    |       |               |-- ProductService.java
    |       |               `-- ProductServiceImpl.java
    |       |-- resources
    |       |   |-- spring-cxf.xml
    |       |   `-- spring.xml
    |       `-- webapp
    |           |-- product.html
    |           `-- WEB-INF
    |               `-- web.xml
    `-- pom.xml
    ```

* 参考链接

    [https://my.oschina.net/huangyong/blog/294324?](https://my.oschina.net/huangyong/blog/294324?)
