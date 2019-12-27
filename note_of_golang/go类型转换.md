### Go语言类型转换



Go语言包含：`类型转换`和`类型断言`，不同的类型之间必须做显示的类型转换

- 类型转换在编译期完成，包括**强制类型转换**和**隐式类型转换**
- 类型断言在运行时确定，包括**安全类型断言**和**非安全类型断言**



#### 转换

- 类型之间的转换

  ```go
  *Point(p)	// same as *(Point(p))
  (*Point)(p) //
  func()(x) 		// 转换x成func()类型
  func() int(x) // 转换x成func() int类型
  ```

  

- 接口之间的转换

  接口之间在编译期间可以确定的情况下可以使用隐式类型转换，当然也可以用强制类型转换（不常用），所有情况下都可以使用类型断言

  ```go
  type A interface {}
  type B interface {Foo()}
  // 编译时无法确定能不能转换，因此用断言
  var a A
  var b = a.(B)
  // 编译时，可以确定
  var c B
  var d = A(c)
  // or var d = c
  // or d = c.(A)
  ```

  

- 接口和类型直接的转换

  普通类型向接口转换，可以使用隐式类型转换

  ```go
  type A interface {}
  var s = "abc"
  var a A
  a = s
  ```

  接口向普通类型转换，只能使用类型断言，因为编译器无法确定

  ```go
  type A interface {}
  var s string
  var a A
  s = a.(string)
  ```

  



#### 断言

Go的接口值的动态类型是不确定的，一个类型断言检查一个接口对象x的动态类型是否和断言的类型T相匹配。

接口值的断言语法：`x.(T)`，这里`x`表示一个接口的类型，`T`表示一个类型（也可以为接口类型）。



- 非安全类型断言

  非安全类型断言，如果系统检测到不匹配，则会在运行期间调用内置的panic，抛出异常

  ```go
  s := "adb"
  i := s.(int)
  ```

  

- 安全类型断言

  安全的类型转换，会有一个ok的bool值，表征类型转换是否成功

  ```go
  type Err struct {
  	S string
  }
  
  func (e *Err) Error() string {
  	return e.S
  }
  
  func GetErr() error {
  	return &Err{S: "abs"}
  }
  
  func GetError() error {
  	return fmt.Errorf("nick")
  }
  
  func main() {
  	e := GetError()
  	i, ok := e.(*Err)
  	if ok {
  		fmt.Printf("ok, i = %+v", i)
  	} else {
  		fmt.Printf("fail")
  	}
  }
  // 打印fail
  ```


- 参考: https://studygolang.com/articles/11419

