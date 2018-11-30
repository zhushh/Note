### 创建项目

##### 项目创建

```
$ django-admin startproject mysite
```

生成的目录结构如下：

```
mysite/
	manage.py
	mysite/
		__init__.py
		settings.py
		urls.py
		wsgi.py
```

目录各文件介绍：

- `manage.py`：管理Django项目的命令行管理工具
- `mysite`：目录包含你的项目，它是一个纯python包
- `mysite/__init__.py`：空文件，让python认为这个目录是一个python包
- `mysite/settings.py`：Django项目的配置文件
- `mysite/urls.py`：Django项目的URL声明
- `mysite/wsgi.py`：项目运行在WSGI兼容的web服务器上的入口



##### 项目运行

```
$ python manage.py runserver
```

上面命令运行默认运行在8000端口，修改端口的运行方式是：

```
$ python manage.py runserver 8080
```

如果想要监听所有服务器的公开IP，使用：

```
$ python manage.py runserver 0:8080
```

`0`是`0.0.0.0`的简写。



### 创建应用

##### 应用创建

在Django中，每一个应用都是一个python包，并且遵从相同的约定。项目与应用的区别：

```
项目和应用有啥区别？应用是一个专门做某件事的网络应用程序，比如博客系统，或者公共记录的数据库，或者简单的投票程序。项目则是一个网站使用的配置和应用的集合。项目可以包含有很多应用，应用可以被很多个项目使用。
```

进入mysite项目，执行下面命令创建一个应用：

```
$ python manage.py startapp polls
```

创建`polls`目录，目录结构如下：

```
polls/
	__init__.py
	admin.py
	apps.py
	migrations/
		__init__.py
	models.py
	tests.py
	views.py
```

目录文件介绍：

- `admin.py`：
- `apps.py`：应用启动项目文件
- `migrations/`：
- `models.py`：编写模型的文件，可以映射到数据库及数据库表，使应用可以访问数据库操作
- `tests.py`：测试文件
- `views.py`：视图文件，视图是指一类具有相同功能和模板的网页集合

上面创建`polls`应用后，还需要添加`urls.py`文件，用于将一个URL映射到一个视图，然后再在mysite下面的`urls.py`包含这个路径的urls。



##### 创建视图及对应url

编辑`polls/views.py`：

```python
from django.http import HttpResponse

def index(request):
	return HttpResponse("Hello world. You are at the polls index.")
```

编辑`polls/urls.py`：

```python
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index')
]
```

这里django包的路径可能会根据django的版本有所改变，但是目的就是编写视图和创建url。

编辑`mysite/urls.py`：

```python
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('polls/', include('polls.urls')),
    path('admin/', admin.site.urls)
]
```

上面`path`中的`polls/`字符串，指定的是访问的url，比如浏览器输入：`127.0.0.1:8000/polls/`就会被路由到`pollls.urls`这个文件处理。

完成上面应用创建后，可以执行下面命令运行应用：

```
$ python manage.py runserver
```

再用浏览器打开：`http://localhost:8000/polls/`就可以看到`Hello world. You are at the polls index`，这是在`index`视图中定义的。

##### 更多的视图及模板

[https://docs.djangoproject.com/zh-hans/2.1/intro/tutorial03/](https://docs.djangoproject.com/zh-hans/2.1/intro/tutorial03/)

##### 数据库配置

[https://docs.djangoproject.com/zh-hans/2.1/intro/tutorial02/](https://docs.djangoproject.com/zh-hans/2.1/intro/tutorial02/)



### 参考链接

- [https://docs.djangoproject.com/zh-hans/2.1/intro/](https://docs.djangoproject.com/zh-hans/2.1/intro/)

























