#### 遍历目录

```go
func GetFileList(dirPath string) []string {
	fileList := []string{}
	PthSep := string(os.PathSeparator)
	dir, err := ioutil.ReadDir(dirPath)
	if err != nil {
		panic(err)
	}
	for _, fi := range dir {
		//fiPath := dirPath + PthSep + fi.Name()
		fiPath := fmt.Sprintf("%s%s%s", strings.TrimSuffix(dirPath, PthSep), PthSep, fi.Name())
		if fi.IsDir() {
			GetFileList(fiPath)
		} else {
			fileList = append(fileList, fiPath)
		}
	}

	return fileList
}
```



#### mysql

处理时间**timestamp**或**datetime**的结构定义方式：

```go
import (
	"database/sql"
    
    db "github.com/go-sql-driver/mysql"
)

// 用户信息
type UserInfo struct{
    Name 		sql.NullString `sql:"name"`
    Age 		sql.NullString `sql:"age"`
    CreateTime 	db.NullTime `sql:"create_time"`
}
```





#### interface 转 struct

```go
package main

import (
	"fmt"
	"reflect"
)

type People struct {
	Name string
	Age int
}

func Print(s interface{}) {
	p := reflect.New(reflect.TypeOf(s).Elem()).Interface()
    // 如果想要使用指针，按下面方式转换
    // personPtr := p.(*People)
	person := (*(p.(*People)))
	person.Name = "xxx"
	person.Age = 32
	fmt.Printf("person: %+v", person)
}

func main() {
	Print((*People)(nil))
}
```





#### for range的问题

下面这段代码会导致rsp的DiamondHistoryItems引用的都是同一个地址，因为都是引用for-range里声明的item地址，导致出现与自己预期的有些不一致。

```go
switch req.Type {
case purse.GetDiamondHistoryReq_DiamondSend:
    //err = handleGetDiamondSend(ctx, req, rsp)
    for _, item := range PurchaseBillRecordConf.PurchaseBillRecord {
        rsp.DiamondHistoryItems = append(rsp.DiamondHistoryItems, &item)
    }
case purse.GetDiamondHistoryReq_DiamondRecv:
    //err = handleGetDiamondRecv(ctx, req, rsp)
    for _, item := range PurchaseBillRecordRecvConf.PurchaseBillRecord {
        rsp.DiamondHistoryItems = append(rsp.DiamondHistoryItems, &item)
    }
default:
    err = qmf_errors.New("diamond history type invalid.", PurseDiamondHistoryTypeInvalid)
}
```

这种在for-range的使用中非常常见。。。



#### 加密使用

```go
package main

import (
    "crypto/sha256"
    "fmt"
    "strconv"
    "time"
)

func signature(data []byte) string {
    h := sha256.New()
    h.Write(data)
    hashInBytes := h.Sum(nil)
    return fmt.Sprintf("%x", hashInBytes)
}

func main() {
    now := time.Now().Unix()

    ts := strconv.FormatInt(now, 10)
    fmt.Println(signature([]byte(ts)))
}

```



#### GoMonkey打桩工具及原理

原理就是替换掉函数执行的跳转地址

https://github.com/bouk/monkey

https://blog.cyeam.com/golang/2018/08/07/monkey-patch



#### 输入输出

```go
package main

func main() {
    var number string
    fmt.Scan(&number)
    fmt.Printf("number: %s", number)
}
```





#### 获取本地Ip

```go
package main

import (
	"fmt"
	"net"
)

func getLocalIp() (string, error) {
	netInterfaces, err := net.Interfaces()
	if err != nil {
		fmt.Println("net.Interfaces failed, err:", err.Error())
		return "", err
	}

	for i := 0; i < len(netInterfaces); i++ {
		if (netInterfaces[i].Flags & net.FlagUp) != 0 {
			addrs, _ := netInterfaces[i].Addrs()

			for _, address := range addrs {
				if ipnet, ok := address.(*net.IPNet); ok && !ipnet.IP.IsLoopback() {
					if ipnet.IP.To4() != nil {
						fmt.Println(ipnet.IP.String())
						return ipnet.IP.String(), nil
					}
				}
			}
		}
	}

	return "", fmt.Errorf("ip no exists.")
}

func main() {
	getLocalIp()
}
```





#### 调用系统命令

```go
package main

import (
	"fmt"
	"io/ioutil"
	"os/exec"
)

func main() {
	cmd := exec.Command("ls", "-a", "-l")
	stdout, err := cmd.StdoutPipe()
	if err != nil {
		fmt.Errorf("err:%+v", err)
		return
	}
	defer stdout.Close()

	// Start 和 Run的区别是，Run会阻塞等待命令执行完成后返回，而Start不会
	if err := cmd.Start(); err != nil {
		fmt.Errorf("err:%+v", err)
		return
	}

	opbytes, err := ioutil.ReadAll(stdout)
	if err != nil {
		fmt.Errorf("err:%+v", err)
		return
	}

	fmt.Printf(string(opbytes))
}
```





#### 文件读写

```go
import (
    "encoding/json"
    "fmt"
	"io/ioutil"
)

type Person struct {
    Name string
    Age int
}

func ReadJsonFile(filename string) (*Person, error) {
    p := new(Person)
    plan, _ := ioutil.ReadFile(filename)
    err := json.Unmarshal(plan, p)
    if err != nil {
        return nil, err
    }
    return p, nil
}
```



#### Testing

默认会执行当前目录下以`*_test.go`格式命名的文件，并生成可执行文件。

执行test

```
$ go test -v ./...
```

清楚test缓存

```
$ go clean -testcache
```



#### string

##### string转bytes

```go
str := "nice"
strByte := []byte(str)
```





#### time

- RFC3339 time解析

```go
import (
	"fmt"
    "time"
)

func test() {
    now := time.Now()
    loc, _ := time.LoadLocation("Local")
    rfc3339_t := now.Format(time.RFC3339)
    
    fmt.Printf("now: %s\n", now)
    fmt.Printf("rfc3339: %s\n", rfc3339_t)
    
    t, _ := time.ParseInLocation(time.RFC3339, rfc3339_t, loc)
    fmt.Printf("cur: %s\n", t)
}
```



- 时戳转换日期：

```go
package main

import (
	"fmt"
	"time"
)

func getDateByTimeStamp(timeStamp int64) string {
	//loc, _ := time.LoadLocation("Local")
	timeNow := time.Unix(timeStamp, 0)
	timeString := timeNow.Format("2006-01-02 15:04:05")
	return timeString
}

func main() {
	var (
		d1 int64 = 1560416308
		d2 int64 = 1560416261
		d3 int64 = 1560416238
		d4 int64 = 1560416236
	)
	fmt.Printf("timestamp=%d, date=%s\n", d1, getDateByTimeStamp(d1))
	fmt.Printf("timestamp=%d, date=%s\n", d2, getDateByTimeStamp(d2))
	fmt.Printf("timestamp=%d, date=%s\n", d3, getDateByTimeStamp(d3))
	fmt.Printf("timestamp=%d, date=%s\n", d4, getDateByTimeStamp(d4))
}
```

- 获取格式化的当前时间日期：

```go
package main

import (
	"fmt"
	"time"
)

func main() {
	date := time.Now().Format("2006-01-02")
	fmt.Println(date)
	fmt.Println(date[0:4] + date[5:7] + date[8:])
    d := time.Now().Format("2006-01-02 15:04:05")
    fmt.Println(d)
}
```

- 字符串转时间：

```go
package main

import (
	"fmt"
	"time"
)

func main() {
	str := "2019-06-27 18:38:08"
	t, err := time.ParseInLocation("2006-01-02 15:04:05", str, time.Local)
	if err != nil {
		fmt.Printf("time.ParseInLocation err:%+v", err)
		return
	}

	fmt.Printf("t = %v", t)
}
```

- 时间增加

```go
package main

import (
"fmt"
"time"
)

func main() {
	start := time.Date(2019, 12, 5, 0, 0, 0, 0, time.Local)

	fmt.Printf("start = %+v\n", start)

	end := start.AddDate(0, 0, 36500)

	fmt.Printf("end = %+v\n", end)
}
// 输入如下:
// start = 2019-12-05 00:00:00 +0800 CST
// end = 2119-11-11 00:00:00 +0800 CST
```





#### slice

##### slice排序(sort.Slice接口)

```go
package main

import (
	"fmt"
	"sort"
)

type Person struct {
	Name string
	Age  int
}

func (p Person) String() string {
	return fmt.Sprintf("%s: %d", p.Name, p.Age)
}

// ByAge implements sort.Interface for []Person based on
// the Age field.
type ByAge []Person

func (a ByAge) Len() int           { return len(a) }
func (a ByAge) Swap(i, j int)      { a[i], a[j] = a[j], a[i] }
func (a ByAge) Less(i, j int) bool { return a[i].Age < a[j].Age }

func main() {
	people := []Person{
		{"Bob", 31},
		{"John", 42},
		{"Michael", 17},
		{"Jenny", 26},
	}

	fmt.Println(people)
	// There are two ways to sort a slice. First, one can define
	// a set of methods for the slice type, as with ByAge, and
	// call sort.Sort. In this first example we use that technique.
	sort.Sort(ByAge(people))
	fmt.Println(people)

	// The other way is to use sort.Slice with a custom Less
	// function, which can be provided as a closure. In this
	// case no methods are needed. (And if they exist, they
	// are ignored.) Here we re-sort in reverse order: compare
	// the closure with ByAge.Less.
	sort.Slice(people, func(i, j int) bool {
		return people[i].Age > people[j].Age
	})
	fmt.Println(people)

}
```

参考：https://golang.org/pkg/sort/



##### slice的append解析

```go
z = append(x, y)
```

slice的底层是引用了一个数组，这个数组有一定的空间，每次append数据的时候，如果x的底层数据空间足够，则会直接在底层数组后面加入y元素，这种时候z和x是引用同一个底层数组；如果x的底层数组空间已经用完，那么会分配一块足够大的新的空间，然后把x拷贝到新的空间，在插入y元素，最后返回，这种情况下z和x底层引用的不是同一个底层数组；

验证例子：

```go
package main

import (
        "fmt"
)

func main() {
        x := make([]int, 3, 4)
        for i := 0; i < 3; i++ {
                x[i] = i
        }
        z := append(x, 6)
        fmt.Println(x)	// [0 1 2]
        fmt.Println(z)	// [0 1 2 6]

    	// 这里证明x和z是引用了相同的内存
        x = append(x, 4)
        fmt.Println(x)	// [0 1 2 4]
        fmt.Println(z)	// [0 1 2 4]
    
    	// 这里证明，如果空间不足的时候，会创建新的内存区域，拷贝x再后面插入新元素
    	z = append(x, 8)
        z[0] = 7
        fmt.Println(x)	// [0 1 2 4]
        fmt.Println(z)	// [7 1 2 4 8]
}
```





#### map

##### map的key类型，要求必须是可比较的

##### map的元素不是变量，无法取地址

```
ages["bob"] = 1
_ = &ages["bob"]	// 这里是错误的，无法对map的成员进行取地址，原因是map可能随元素数量的增长二重新分配更大的内存空间，从而可能导致之前的地址无效
```

##### map的迭代顺序是不确定的，而且每次都是随机的

```go
package main

import (
        "fmt"
)

func main() {
        m := make(map[string]int)
        m["nice"] = 1
        m["to"] = 2
        m["meet"] = 3
        m["you"] = 4

        for w, v := range m {
                fmt.Printf("%s\t%d\n", w, v)
        }
        for w, v := range m {
                fmt.Printf("%s\t%d\n", w, v)
        }
}
```

这里输出的顺序不一定是`1 2 3 4`，也可能是`3 4 2 1`这种。如果想要显示地对key进行排序，需要使用`sort`包的`Strings`函数对字符串进行排序。

##### map的key的非空判断

```go
age, ok := ages["bob"]
if !ok {
    // "bob" is not a key in this map; age = 0
}
```



#### 结构体

##### 结构体面值

结构体值可以用结构体面值表示，结构体面值可以指定每个成员的值

```go
type Point struct{X, Y int}
p := Point{1, 2}
```

结构体面值有两种语法，第一种就是上面那样，要求以结构体成员定义的顺序为咩咯结构体成员指定一个面值，这种写法只能在定义结构体的包内部使用，或者较小的结构体中使用；另一种写法，以成员名字和相应的面值来初始化，可以包含全部或部分成员：

```go
anim := gif.GIF{LoopCount: nframe}
```

这种写法如果成员被忽略的话，将默认值用0值。

##### 结构体比较

如果结构体的全部成员都是可以比较的，那么结构体也是可以比较的，这时可以使用==或!=运算符号进行比较。

##### 匿名访问成员

```go
type Point struct {
    X, Y int
}

type Circle struct {
    Point
    Radius int
}

type Wheel struct {
    Circle
    Spokes int
}

w = Wheel{Circle{Point{8, 8}, 5}, 20}

w = Wheel{
    Circle: Circle{
        Point: Point{X: 8, Y: 8},
        Radius: 5,
    },
    Spokes: 20,	// 这里的逗号是必须的
}
```

匿名成员也是可以导出的，如果是小写的point，那么因为point是无法导出的，所以匿名成员也无法导出。



##### tag的使用

```go
type Movie struct {
    Title string	`json:"title"`
    Year  int 		`json:"released"`
}
```

结构体成员tag可以是任意字符串面值，但是通常由一系列的空格分隔的`key:"value"`键值对序列；因为值中含义双引号字符，因此成员tag一般用原生字符串面值的形式书写。`json`开头键名对应的值用于控制`encoding/json`包编码和解码的行为，并且`encoding/..`下面其他的包也遵循这个约定。

多tag例子：

```go
type User struct {
	ID        UserID `sql:"id" json:"ID"`
	FirstName string `sql:"first_name" json:"FirstName"`
	LastName  string `sql:"last_name" json:"LastName"`
	Email     string `sql:"email" json:"Email"`
	Active    bool   `sql:"active" json:"Active,omitempty"
}
```





#### 函数

函数可以像其他值一样，拥有类型，可以被赋值给其他变量，传递给函数，从函数返回。

```go
func Square(n int) int {return n*n }

var f func(int) int

f = Square
fmt.Println(f(3))	// 9
```

函数值可以与nil比较，但是不可以当作map的key。



##### 函数的声明

```
func 函数名 形参数列表 返回值列表（可省略） 函数体
```

函数的类型被称为 **函数标识符**，如果两个函数的 **形式参数列表**和 **返回值列表**中的变量类型一一对应，那么这两个函数被认为由相同的类型和标识符。比如：

```go
func add(x, y int) int {}
func sub(a, b int) int {}
```

另外，没有函数体的函数声明，表示该函数不是以Go实现的，这样的声明定义了标识符：

```go
package main

func Sin(x float64) float
```



##### 形参，有名返回值，return和defer

Go语言没有默认参数值，所有的参数提供实参。函数的**形参**和**有名返回值**作为函数最外层的局部变量，被存储在相同的词法块中，如果函数的返回值都显示了变量名，那么return语句可以省略操作数，称之为bare return。

```go
package main
import "fmt"

func sum(a, b int) (r int) {
        defer func(){
                r += 1
        }()
        r = a+b
        return r	// 此处的r变量可以不写
}

func sum2(a, b int) int {
        var r int
        defer func() {
                r += 1
        }()
        r = a+b
        return r
}

func main() {
        a := 3
        b := 4
        fmt.Println(sum(a, b))		// 打印 8
        fmt.Println(sum2(a, b))		// 打印 7
}
```

上面程序输出分别为：`8`和`7`，原因是因为`return`不是一个原子的操作。执行顺序是：

1. 先给返回值赋值
2. 调用defer表达式（可以对**有名返回值**进行修改更新）
3. 最后返回到函数中



##### 引用类型的实参

指针，slice，map，function，channel等，这些实参可能由于函数的引用被修改，导致函数外部使用的时候也被修改。



##### 匿名函数

```go
strings.Map(func (r rune) rune {return r+1}, "HAL-9000")

func Square() func() int {
    var x int
    return func() int {
        x++
        return x * x
    }
}

func main() {
    f := Square()
    fmt.Println(f())	// 1
    fmt.Println(f())	// 4
    fmt.Println(f())	// 9
}
```

Go使用闭包技术实现函数值，Go程序员把函数值叫做闭包。变量的声明周期是由引用计数决定，而不是作用于决定。



##### 可变参数

声明可变参数，需要在函数列表的最后一个参数类型之前加上省略符号“...”，表示会接收任意数量该类型参数：

```go
func sum(vals ...int) int {
    total := 0
    for _, val := range vals {
        total += val
    }
    return total
}
```

**切片如何传给可变参数**

切片类型的参数，传给可变长参数，只需要在切片变量的后面使用省略符号就可以“...”

```go
values := []int{2,4,6,8}
fmt.Println(sum(values...))
```

**更常用的可变参数使用**

```go
func errorf(linenum int, format string, args ...interface{}) {
    fmt.Fprintf(os.Stderr, "Line %d:", linenum)
    fmt.Fprintf(os.Stderr, format, args...)
    fmt.Fprintln(os.Stderr)
}
linenum, name := 23, "nick"
errorf(linenum, "undefined: %s", name)
```



##### Panic与Recover函数

panic允许传递一个参数给它，panic打印这个字符串，处理完当前goroutine已经defer挂上去的任务，以及触发panic的调用栈，停掉当前正在执行的程序。总结就是三点：

- 遇到处理不了的错误，panic
- 退出前会执行本goroutine的defer，方式是原路返回
- 不是本goroutine的defer，不执行

如果不希望因为无法处理的错误panic而导致整个进程挂掉，可以在当前goroutine的defer中，使用recover来捕获panic。**recover只在defer的函数中有效，如果不在defer上下文中，recover会返回nil**。

[Golang：深入理解panic and recover](https://ieevee.com/tech/2017/11/23/go-panic.html)



#### 错误处理

##### 错误传播

```go
doc, err := html.Parse(resp.Body)
resp.Body.Close()
if err != nil {
    return nil, fmt.Errorf("parsing %s as HTML: %v", url, err)
}
```

当HTML解析错误的时候，但是此时是已经获取得到resp数据的了，所以可以把错误封装更详细，向上传播处理，后面定位错误的时候，可以快速的知道错误原因。



##### 固定间隔重试

```go
func WaitForServer(url string) error {
    const timeour = 1 * time.Minute
    deadline := time.Now().Add(timeout)
    for tries := 0; time.Now().Before(deadline); tries++ {
        _, err := http.Head(url)
        if err == nil {
            return nil
        }
        log.Printf("server not response (%s); retrying...", err)
        time.Sleep(time.Second << uint(tries))
    }
    return fmt.Errorf("server %s failed to response after %s", url, timeout)
}
```



##### 输出错误信息并结束程序

```go
if err := WaitForServer(url); err != nil {
    fmt.Fprintf(os.Stderr, "Site is down: %v\n", err)
    os.Exit(1)
}
```

使用`log`方式更简洁：

```go
if err := WaitForServer(url); err != nil {
    log.Fatalf("Site is down: %v", err)
}
```



##### 只输出错误信息 or 直接忽略错误

```go
if err := Ping(); err != nil {
    log.Printf("ping failed: networking disabled", err)
}

os.RemoveAll(dir)
```



#### 方法

##### 方法值和方法表达式

```go
import (
    "fmt"
	"math"
)

type Point struct {
    X, Y int
}

func (p Point)Distance(q Point) float64 {
    return math.Hypot(p.X-q.X, p.Y - q.Y)
}

p := Point{1, 2}
q := Point{4, 6}

distanceFromP := p.Distance	// 方法值
distance := Point.Distance	// 方法表达式

fmt.Println(distanceFromP(q))
fmt.Println(distance(p, q))
```

##### 封装

- 一个struct类型的字段，对同一个package的所有代码都是可见性，无论是在函数内还是方法里
- 封装的最小单位是package





#### 时间比较

这里的时间比较，如果没有获取时区，可能会导致UTC时间和CST时间相比较错误。

```go
func CheckActivityTime(startTime string, endTime string) bool {
	format := "2006-01-02 15:04:05"
	loc, _ := time.LoadLocation("Local") //重要：获取时区
	now := time.Now()
	a, _ := time.ParseInLocation(format, startTime, loc)
	b, _ := time.ParseInLocation(format, endTime, loc)
	if now.After(a) && now.Before(b) {
		return true
	}
	return false
}
```



##### switch的巧用

利用switch进行多个字符串判断，保持代码简洁

```go
func ListenTCP(network string, laddr *TCPAddr) (*TCPListener, error) {
    switch network {
    case "tcp", "tcp4", "tcp6":
    default:
        return nil, OpError{Op: "listen", Net: network, Source: nil, Addr: laddr.opAddr(), Err: UnknownNetworkError(network)}
    }
    if laddr == nil {
        laddr = &TCPAddr()
    }
    ln, err := listenTCP(context.Backgroud(), network, laddr)
    if err != nil {
        return nil, OpError{Op: "listen", Net: network, Source: nil, Addr: laddr.opAddr(), Err: err}
    }
    return ln, nil
}
```

`fallthrough`关键字使用：只能用于switch最后一个语句，表示当前case被执行时，后面一个case的语句也会被执行；

```go
package main

import "fmt"

func test(val int) {
    switch val {
    case 4:
        fmt.Println("4")
    case 5:
        fmt.Println("5")
        fallthrough
    case 6:
        fmt.Println("6")
    case 7:
        fmt.Println("7")
    }
}

func main() {
    val := 5
    test(val)
}
```

上面程序会输出：

```
5
6
```





##### 简单的cache

```go
var cache = struct {
    sync.Mutex
    mapping map[string]string
} {
    mapping: make(map[string]string)
}

func Lookup(key string) string {
    cache.Lock()
    v := cache.mapping[key]
    cache.Unlock()
    return v
}
```

























