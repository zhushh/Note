#### 测试例子

```go
package main

import (
	"fmt"
	"sync"
)

func main() {
	var wait sync.WaitGroup
	wait.Add(1)
	go func() {
		defer wait.Done()
		fmt.Println("Hello 1")
	}()

	wait.Add(1)
	go func() {
		defer wait.Done()
		fmt.Println("Hello 2")
	}()

	wait.Add(1)
	go func() {
		defer wait.Done()
		fmt.Println("Hello 3")
	}()

	wait.Wait()
	fmt.Println("Hello 4")
}
```

输出结果：其中，1，2，3的顺序可能会不一样

```
Hello 3
Hello 1
Hello 2
Hello 4
```





#### 错误例子

```go
package main

import (
	"fmt"
	"sync"
)

func main() {
	var wait sync.WaitGroup

	go func() {
		defer wait.Done()
		wait.Add(1)
		fmt.Println("Hello 1")
	}()

	go func() {
		defer wait.Done()
		wait.Add(1)
		fmt.Println("Hello 2")
	}()

	go func() {
		defer wait.Done()
		wait.Add(1)
		fmt.Println("Hello 3")
	}()

	wait.Wait()
	fmt.Println("Hello 4")
}
```

结果输出：

```
Hello 4
```

或者

```
Hello 2
Hello 1
Hello 4
```

各种情况都可能出现，导致这个的原因是因为`goroutin`的调度，可能还没有`add`就执行了`wait`，这时候就会导致go func启动的没有被执行。

