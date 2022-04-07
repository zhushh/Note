### __attribute__机制

`__attribute__`GNU C的一大特色，可以设置：

- 函数属性（Function Attribute）
- 变量属性（Variable Attribute）
- 类型属性（Type Attribute）

语法格式：

```c++
__attribute__(())
```



#### `format`

该属性可以使编译器检查函数声明和函数实际调用参数之间的格式化字符串是否匹配；

语法格式：

```c++
format ( archetype,  string-index,  first-to-check )
```

format属性告诉编译器，按照printf，scanf，strftime或strfmon的参数表格式规则对该函数的参数进行检查。

- archetype：指定是哪种风格；
- string-index：指定传入函数的第几个参数是格式化字符串；
- first-to-check：指定从函数的第几个参数开始按上述规则进行检查。

具体使用格式：

```
__attribute__( ( format( printf，m，n ) ) )
__attribute__( ( format( scanf，m，n ) ) )
```

其中参数m与n的含义为：

**m：**第几个参数为格式化字符串（format string）；

**n：**参数集合中的第一个，即参数“…”里的第一个参数在函数参数总数排在第几

注意，有时函数参数里还有“隐身”的呢，后面会提到；

在使用上，`__attribute__((format(printf,m,n)))`是常用的，而另一种却很少见到。

例子：

```c++
//m=1；n=2
extern void print(const char *format, ...) __attribute__((format(printf,1,2)));
//m=2；n=3
extern void print(int l,const char *format,...) __attribute__((format(printf,2,3)));
```

如果`print`是一个成员函数：

```c++
extern void print(int l,const char *format, ...) __attribute__((format(printf,3,4)));
```

其原因是因为，类成员函数的第一个参数实际上是**this**指针；



#### `noreturn`

该属性通知编译器函数从不返回值。

当遇到函数需要返回值却还没运行到返回值处就已退出来的情况，该属性可以避免出现错误信息。

C库函数中的abort（）和exit（）的声明格式就采用了这种格式：

```c++
extern void  exit(int)   __attribute__( ( noreturn ) );
extern void  abort(void)  __attribute__( ( noreturn ) ); 
```

例子：

```c
#include <stdio.h>
#include <stdlib.h>

void myexit() __attribute__((noreturn));

int test(int n) {
    if (n > 0) {
        myexit(n);

        // 不会走到的语句
        printf("match n > 0\n");
    } else {
        printf("match n <= 0\n");
        return 0;
    }
}

int main() {
    int n;
    scanf("%d", &n);
    test(n);
    return 0;
}

void myexit(int n) {
    printf("I am exit. n = %d\n", n);
    exit(n);
}
```



#### `constructor/destructor`

若函数被设定为constructor属性，则该函数会在main（）函数执行之前被自动的执行。类似的，若函数被设定为destructor属性，则该函数会在main（）函数执行之后或者exit（）被调用后被自动的执行。拥有此类属性的函数经常隐式的用在程序的初始化数据方面，这两个属性还没有在面向对象C中实现。例子：

```C
#include <stdio.h>
#include <stdlib.h>

void constructorTest() __attribute__((constructor));
void destructorTest() __attribute__((destructor));


int main() {
    printf("I am main function\n");
    return 0;
}

void constructorTest() {
    printf("I am constructor function\n");
}

void destructorTest() {
    printf("I am destructor function\n");
}
```

运行输出：

```
I am constructor function
I am main function
I am destructor function
```



#### `同时使用多个属性`

可以在同一个函数声明里使用多个`__attribute__`，并且实际应用中这种情况是十分常见的。使用方式上，你可以选择两个单独的`__attribute__`，或者把它们写在一起，可以参考下面的例子：

```c
extern void die(const char *format, ...) __attribute__((noreturn)) __attribute__((format(printf, 1, 2))); 
```

或者写成：

```c
extern void die(const char *format, ...) __attribute__((noreturn, format(printf, 1, 2))); 
```

如果带有该属性的自定义函数追加到库的头文件里，那么所以调用该函数的程序都要做相应的检查。



#### `和非GNU编译器的兼容性`

`__attribute__`设计的非常巧妙，很容易作到和其它编译器保持兼容。

例如：

```c
 /* 如果使用的是非GNU C, 那么就忽略__attribute__ */
#ifndef __GNUC__
      #define  __attribute__(x)     /* NOTHING * /
#endif 
```

`__attribute__`适用于函数的声明而不是函数的定义。所以，当需要使用该属性的函数时，必须在同一个文件里进行声明，例如：

```c
/* 函数声明 */
void  die( const char *format, ...) __attribute__((noreturn)) __attribute__((format(printf,1,2)));

void  die( const char *format, ...)
{   /* 函数定义 */  }
```





### 参考

https://cloud.tencent.com/developer/article/1392814

http://gcc.gnu.org/onlinedocs/gcc-4.0.0/gcc/Function-Attributes.html

