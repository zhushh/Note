---
name: maven
date: 2016-12-29
update: 2016-12-30
keyword: maven
---


Maven是什么？
----

* Maven介绍

    maven是一个项目构建和管理的自动化工具，maven通过项目对象模型（POM，下面会介绍）来管理项目的构建;
    
    wiki链接[https://en.wikipedia.org/wiki/Apache_Maven](https://en.wikipedia.org/wiki/Apache_Maven)

* Maven项目的目录结构特征

    |              目录             |           用处            |
    | ----------------------------- | -------------------------|
    |          ${basedir}           | 存放pom.xml和所有的子目录   |
    |    ${basedir}/src/main/java   | 项目的java源代码目录        |
    | ${basedir}/src/main/resources | 项目的资源，比如property文件 |
    |    ${basedir}/src/test/java   | 项目测试类，比如JUnit代码    |
    | ${basedir}/src/test/resources | 测试使用的资源              |


Maven 环境安装与配置
----

* 安装前提：

    Java环境的配置，并设置有JAVA_HOME环境变量;

* 下载解压安装：

    前往[https://maven.apache.org/download.cgi](https://maven.apache.org/download.cgi)，
    下载  apache-maven-3.3.9-bin.tar.gz安装包;运行下面命令进行解压：
    ```
    $ tar -zxvf apache-maven-3.3.9-bin.tar.gz
    ```
    移到/usr/local目录，并创建链接apache-maven：

    ```
    $ sudo mv apache-maven-3.3.9 /usr/local/
    $ sudo ln -s /usr/local/apache-maven-3.3.9 /usr/local/apache-maven
    ```

* 添加命令到环境变量：

    编辑/etc/profile文件，添加/修改下面环境变量内容:
    ```
    export M2_HOME=/usr/local/apache-maven
    export MAVEN_OPTS="-Xms256m -Xmx512m"
    export MAVEN_HOME=/usr/local/apache-maven
    export PATH=/usr/local/apache-maven/bin:$PATH
    ```

* 检验安装成功：

    输入下面命令：
    ```
    $ mvn --version
    ```
    看到类似下面的输出则说明安装配置成功：
    ```
    Apache Maven 3.3.9 (bb52d8502b132ec0a5a3f4c09453c07478323dc5; 2015-11-11T00:41:47+08:00)
    Maven home: /usr/local/apache-maven
    Java version: 1.8.0_51, vendor: Oracle Corporation
    Java home: /opt/jdk1.8.0_51/jre
    Default locale: en_US, platform encoding: UTF-8
    OS name: "linux", version: "4.4.0-57-generic", arch: "amd64", family: "unix"
    ```

Maven 入门例子
----

先通过运行一个简单的入门例子，待会后面会再解释一下命令;

* 创建项目

    使用下面命令创建项目
    ```
    $ mvn archetype:generate -DgroupId=com.mycompany.app \
    -DartifactId=my-app \
    -DarchetypeArtifactId=maven-archetype-quickstart \
    -DinteractiveMode=false
    ```
    第一次运行需要等一会，因为maven会下载项目所需要的所有插件和依赖，
    然后你会看到在当前目录下会创建一个my-app的项目目录;`cd my-app`进入项目目录,目录结构如下：
    ```
    my-app
    |-- pom.xml
    `-- src
        |-- main
        |   `-- java
        |       `-- com
        |           `-- mycompany
        |               `-- app
        |                   `-- App.java
        `-- test
            `-- java
                `-- com
                    `-- mycompany
                        `-- app
                            `-- AppTest.java
    ```
    详细说明

        src/main/java目录包含的是项目源代码
        src/test/java目录包含的是项目的测试代码
        pom.xml文件是Project Object Model（POM）

* 工程对象模型（POM）介绍

    工程对象模型（POM），是指文件pom.xml，这个文件是maven项目配置的核心。包含了关于工程和各种配置细节的信息，Maven 使用这些信息构建工程。
    所有的项目都只有一个POM文件，文件需要包含groupId， artifactId， version三个信息;其中，

        groupId：描述的是项目名称
        artifactId:描述的是包的名称
        version:描述包的版本号

    详细信息参考[https://maven.apache.org/guides/introduction/introduction-to-the-pom.html](https://maven.apache.org/guides/introduction/introduction-to-the-pom.html)和[https://maven.apache.org/pom.html](https://maven.apache.org/pom.html)


* 编译打包项目

    在目录my-app下运行下面命令
    ```
    $ mvn package
    ```
    会看到项目的编译过程，最后输出会有下面信息：
    ```
    ...
    [INFO] 
    [INFO] --- maven-jar-plugin:2.4:jar (default-jar) @ my-app ---
    [INFO] Building jar: /home/zhushh/Rick/mavenRepository/my-app/target/my-app-1.0-SNAPSHOT.jar
    [INFO] ------------------------------------------------------------------------
    [INFO] BUILD SUCCESS
    [INFO] ------------------------------------------------------------------------
    [INFO] Total time: 4.613 s
    [INFO] Finished at: 2016-12-29T16:16:55+08:00
    [INFO] Final Memory: 21M/331M
    [INFO] ------------------------------------------------------------------------
    ```

* 检验是否成功生成目标包
    ```
    $ java -cp target/my-app-1.0-SNAPSHOT.jar com.mycompany.app.App 
    ```
    看到输出`Hello World`， 就说明成功运行第一个maven例子;

* 参考教程

    [https://maven.apache.org/guides/getting-started/index.html#What_is_Maven](https://maven.apache.org/guides/getting-started/index.html#What_is_Maven)


Maven 常用命令
----

* 创建项目

    ```
    mvn -B archetype:generate \ 
        -DarchetypeGroupId=org.apache.maven.archetypes \
        -DarchetypeArtifactId=maven.archetype.webapp \
        -DgroupId=com.mycompany.app \
        -DartifactId=my-app
    ```

    **-B**：

        这个参数是指进行创建过程不需要交互（也就是不需要手动输入groupId、artifactId这些，而是使用指定）;

    **-DgroupId**：
        
        这个参数是由两个构成，其中-D表示定义的意思;
        所以上面命令中：
        -DarchetypeGroupId 表示定义archetypeGroupId
        -DarchetypeArtifactId 表示定义archetypeArtifactId
        -DgroupId 表示定义groupId
        -DartifactId 表示定义artifactId

    使用maven可以创建很多种应用，包括webapp、j2ee、maven插件、maven项目等，这些都可以通过定义archetypeGroupId和archetypeArtifactId来创建;
    详细参考链接[https://maven.apache.org/guides/introduction/introduction-to-archetypes.html](https://maven.apache.org/guides/introduction/introduction-to-archetypes.html)

* 编译项目

    ```
    mvn compile
    ```
    运行这个命令可以编译项目，编译过程按照pom.xml文件定义好的进行;
    提醒一下，这里只是进行编译，而要运行maven项目的java代码，需要使用插件;而且不同的项目运行需要使用不同的插件;
    
* 运行项目

    如果只是运行java的代码，那么使用 [maven-exec-plugin](http://www.mojohaus.org/exec-maven-plugin/usage.html) ;
    
    先配置pom.xml，添加下面的插件内容
    ```xml
    <build>
      <plugins>
        <plugin>
          <groupId>org.codehaus.mojo</groupId>
          <artifactId>exec-maven-plugin</artifactId>
          <version>1.2.1</version>
          <executions>
            <execution>
              <goals>
                <goal>java</goal>
              </goals>
            </execution>
          </executions>
          <configuration>
            <mainClass>com.mycompany.app.App</mainClass>
            <arguments>
              <argument>foo</argument>
              <argument>bar</argument>
            </arguments>
          </configuration>
        </plugin>
      </plugins>
    </build>
    ```
    主要需要配置的是`<mainClass>`和`<arguments>`，这两个分别表示运行的类和传进去的参数;其他的是插件信息;
    
    然后在命令行输入下面命令
    ```
    $ mvn exec:java -Dexec.mainClass="com.mycompany.app.App"
    ```
    就可以运行com/mycompany/app/App.java这个类了;
    还有其他比较复杂的配置运行，这个有需要的自己去查看例子或别的教程即可;
    总的来说，这个pom.xml的配置信息其实挺容易看懂的;所以要看懂别人的例子也不难;
    
* 运行测试代码

    ```
    mvn test
    ```
    运行项目目录test里面的测试，一般也需要在pom.xml文件里面先进行配置;

* 打包项目

    ```
    mvn package
    ```
    直接把编译好后的各个类等文件进行打包，打包的格式和资源也是在pom.xml里面定义;
    所以你知道pom.xml文件的配置有多强大了吧;

* 安装项目

    ```
    mvn install
    ```
    安装到本地，具体暂时不了解，有兴趣的可以去查看一下文档;

* 其他命令参数

    ```
    mvn site
    mvn clean
    mvn idea:idea
    mvn eclipse:eclipse
    ```

Maven创建标准Servlet程序过程
----
* 使用maven创建项目

    ```
    mvn -B archetype:generate -DarchetypeGroupId=org.apache.maven.archetypes \
        -DarchetypeArtifactId=maven-archetype-webapp \
        -DgroupId=com.mycompany.app \
        -DartifactId=my-app
    ```
    之后就会创建出项目my-app，目录结构如下：
    ```
    my-app
    |-- pom.xml
    `-- src
        |-- main
            |-- resources
            `-- webapp
                |-- index.jsp
                `-- WEB-INF
                    `-- web.xml
    ```

* 创建源代码目录及文件

    我们手动创建src/main/java/org/example源代码目录，并添加文件HelloServlet.java文件，文件输入下面内容：
    ```java
    package org.example;

    import java.io.IOException;
    import javax.servlet.ServletException;
    import javax.servlet.http.HttpServlet;
    import javax.servlet.http.HttpServletRequest;
    import javax.servlet.http.HttpServletResponse;

    public class HelloServlet extends HttpServlet
    {
            protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException
            {
                    response.setContentType("text/html");
                    response.setStatus(HttpServletResponse.SC_OK);
                    response.getWriter().println("<h1>Hello Servlet</h1>");
                    response.getWriter().println("session=" + request.getSession(true).getId());
            }
    }
    ```

* 编辑webapp信息

    编辑src/main/webapp/WEB-INF/web.xml文件，把下面内容覆盖掉原来的就可以：
    ```xml
    <!DOCTYPE web-app PUBLIC
     "-//Sun Microsystems, Inc.//DTD Web Application 2.3//EN"
     "http://java.sun.com/dtd/web-app_2_3.dtd" >

    <web-app
       xmlns="http://xmlns.jcp.org/xml/ns/javaee"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xsi:schemaLocation="http://xmlns.jcp.org/xml/ns/javaee http://xmlns.jcp.org/xml/ns/javaee/web-app_3_1.xsd"
       metadata-complete="false"
       version="3.1">

      <servlet>
            <servlet-name>Hello</servlet-name>
            <servlet-class>org.example.HelloServlet</servlet-class>
      </servlet>
      <servlet-mapping>
            <servlet-name>Hello</servlet-name>
            <url-pattern>/hello/*</url-pattern>
      </servlet-mapping>

    </web-app>
    ```
    
* 编辑项目依赖等信息
    
    编辑pom.xml文件，可以用下面内容覆盖掉原来的：
    ```xml
    <project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
      xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/maven-v4_0_0.xsd">
      <modelVersion>4.0.0</modelVersion>
      <groupId>com.mycompany.app</groupId>
      <artifactId>JettyMavenHelloWarApp</artifactId>
      <packaging>war</packaging>
      <version>1.0-SNAPSHOT</version>
      <name>JettyMavenHelloWarApp Maven Webapp</name>

      <properties>
              <jettyVersion>9.3.7.v20160115</jettyVersion>
      </properties>

      <dependencies>
            <dependency>
              <groupId>javax.servlet</groupId>
              <artifactId>javax.servlet-api</artifactId>
              <version>3.1.0</version>
              <scope>provided</scope>
            </dependency>
      </dependencies>

      <build>
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

* 编译运行项目
    
    使用下面命令进行编译运行，可能需要等一会，因为需要下载安装jetty
    ```
    mvn jetty:run package
    ```
    成功运行后应该会在最后看到类似如下输出：
    ```
    ...
    [INFO] Started ServerConnector@7afb1741{HTTP/1.1,[http/1.1]}{0.0.0.0:8080}
    [INFO] Started @4816ms
    [INFO] Started Jetty Server
    ```
    然后访问浏览器，输入[http://localhost:8080/hello](http://localhost:8080/hello) 可以看到类似下面输出：
    ```
    Hello Servlet
    session=58tpdbbynuze769l01r97pjx 
    ```

* 备注
 
    可以参考另一个教程来创建servlet程序,链接是 [http://www.eclipse.org/jetty/documentation/current/maven-and-jetty.html](http://www.eclipse.org/jetty/documentation/current/maven-and-jetty.html)

