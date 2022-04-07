#### Macaron教程

https://go-macaron.com/docs/intro/getting_started



#### 步骤

##### 配置

ubuntu环境



##### Go环境配置

略



##### Macaro安装

```
$ go get gopkg.in/macaron.v1
```

然后写简单的例子：

```go
package main

import "gopkg.in/macaron.v1"

func main() {
    m := macaron.Classic()
    m.Get("/", func() string {
        return "Hello world!"
    })
    m.Run()
}
```

保存main.go，然后`go run main.go`能正常运行OK



##### 代码目录架构

```
- mysite
	- src
		- public
			- html
				- index.html
		- assets
		- main.go
```

main.go代码：

```go
package main

import (
	"log"
	"net/http"
	"time"

	"gopkg.in/macaron.v1"
)

func main() {
	m := macaron.Classic()
	m.Use(macaron.Static("public",
		macaron.StaticOptions{
			// 请求静态资源时的 URL 前缀，默认没有前缀
			Prefix: "public",
			// 禁止记录静态资源路由日志，默认为不禁止记录
			SkipLogging: true,
			// 当请求目录时的默认索引文件，默认为 "index.html"
			IndexFile: "index.html",
			// 用于返回自定义过期响应头，默认为不设置
			// https://developers.google.com/speed/docs/insights/LeverageBrowserCaching
			Expires: func() string {
				return time.Now().Add(24 * 60 * time.Minute).UTC().Format("Mon, 02 Jan 2006 15:04:05 GMT")
			},
		}))

	m.Get("/", myHandler)

	log.Println("Server is running...")
	log.Println(http.ListenAndServe("0.0.0.0:80", m))
}

func myHandler(ctx *macaron.Context) string {
	return "the request path is: " + ctx.Req.RequestURI
}
```



index.html

```html
<!DOCTYPE html>
<html>
<head>
<title></title>
</head>
<body style="background-color: black">
<canvas id='cavs' style='position:fixed; z-index:-1;'></canvas>
</body>
</html>
<script type="text/javascript">
var canvas = document.getElementById("cavs");
const WIDTH = window.innerWidth;
const HEIGHT = window.innerHeight;
canvas.setAttribute("width", WIDTH);
canvas.setAttribute("height", HEIGHT);
var context = canvas.getContext("2d");
var start =
{
    loves: [],
    DURATION: 30,
    begin: function()
    {
        this.createLove();
    },
    createLove: function()
    {
        for (var i = 0; i < WIDTH / 59; i++)
        {
            var love = new Love();
            this.loves.push(love);
        }
        setInterval(this.drawLove.bind(this), this.DURATION);
    },
    drawLove: function()
    {
        context.clearRect(0, 0, WIDTH, HEIGHT);
        for (var key in this.loves)
        {
            this.loves[key].draw();
        }
    }
}
function Love()
{
    var me = this;
    function rand() 
    {
        me.maxScale = (Math.random() * 3.2 + 1.2) * WIDTH / 521;
        me.curScale = 1.2 * WIDTH / 521;
        me.x = Math.floor(Math.random() * WIDTH - 40);
        me.y = Math.floor(HEIGHT - Math.random() * 200);
        me.ColR = Math.floor(Math.random() * 255);
        me.ColG = Math.floor(Math.random() * 255);
        me.ColB = Math.floor(Math.random() * 255);
        me.alpha = Math.random() * 0.2 + 0.8;
        me.vector = Math.random() * 5 + 0.4;
    }
    (function(){rand();} ());
    me.draw = function()
    {
        if (me.alpha < 0.01) rand();
        if(me.curScale < me.maxScale) me.curScale += 0.3;
        x = me.x;
        y = me.y;
        scale = me.curScale;
        context.fillStyle = "rgba(" + me.ColR + "," + me.ColG + "," + me.ColB + "," + me.alpha + ")";
        context.shadowBlur = 10;
        context.shadowColor = "rgb(" + me.ColR + "," + me.ColG + "," + me.ColB + ")";
        context.beginPath();
        context.bezierCurveTo( x + 2.5*scale, y + 2.5*scale, x + 2.0*scale, y, x, y );
        context.bezierCurveTo( x - 3.0*scale, y, x - 3.0*scale, y + 3.5*scale,x - 3.0*scale,y + 3.5*scale );
        context.bezierCurveTo( x - 3.0*scale, y + 5.5*scale, x - 1.0*scale, y + 7.7*scale, x + 2.5*scale, y + 9.5*scale );
        context.bezierCurveTo( x + 6.0*scale, y + 7.7*scale, x + 8.0*scale, y + 5.5*scale, x + 8.0*scale, y + 3.5*scale );
        context.bezierCurveTo( x + 8.0*scale, y + 3.5*scale, x + 8.0*scale, y, x + 5.0*scale, y );
        context.bezierCurveTo( x + 3.5*scale, y, x + 2.5*scale, y + 2.5*scale, x + 2.5*scale, y + 2.5*scale );
        context.fill();
        context.closePath();
        me.y -= me.vector;
        me.alpha -= (me.vector / 2.9 * 3.5 / HEIGHT);
    }
}
window.onload = function()
{
    start.begin();
}
</script>
```



代码编译运行：

```
$ cd mysite/
$ go build
```





##### 云服务器申请

https://cloud.tencent.com/product/cvm

选择一款适合的云产品，然后进行购买配置



##### 域名申请并绑定云服务器

https://console.cloud.tencent.com/cns/detail/irick.com.cn/records

点击域名管理 -> 点击添加记录 -> 选择绑定到云服务器 -> 完成



