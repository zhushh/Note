## C/C++

### 声明与定义

（1）变量定义：用于为变量分配存储空间，还可以指定初始值，程序中变量的定义有且仅有一个；除非有extern时，否则都为变量定义；

（2）变量声明：用于向程序表明变量的类型和名字；

（3）extern关键子：通过extern关键对变量进行声明而不定义它；如果extern变量带有初始化，那么认为是定义；

（4）定义也是声明：当变量定义时，我们声明了变量的类型和名字，定义是在内存中有确定的位置和大小；

举例：
```
extern int i;   // 声明
int i;  // 定义
extern int Pi=3.1415926;    // 定义，如果声明中带有初始化时是定义
extern int add(int a, int b);   // 函数声明不带{}，带大括号的为定义
```

### 字节
使用sizeof计算下面的值，在不同系统的结果：
（1）32位系统
```
sizeof(char) = 1
sizeof(char *) = 4
sizeof(short) = 2
sizeof(int) = 4
sizeof(long) = 4
sizeof(long long) = 8
sizeof(float) = 4
sizeof(double) = 8
```
（2）64位系统
```
sizeof(char) = 1
sizeof(char *) = 8
sizeof(short) = 2
sizeof(int) = 4
sizeof(long) = 8
sizeof(long long) = 8
sizeof(float) = 4
sizeof(double) = 8
```
32位和64位主要区别在于地址寻址宽度，32位寻址最大为2^32 = 4G,64位寻址最大为2^64;

类
----
### Why destructor should be declared as virtual in c++?

[When to use virtual destructors?](http://stackoverflow.com/questions/461203/when-to-use-virtual-destructors)

### Why do we not have a virtual constructor in c++?
```
A virtual call is a mechanism to get work done given partial information. In particular, "virtual" allows us to
call a function knowing only any interfaces and not the exact type of the object. To create an object you need 
complete information. In particular, you need to know the exact type of what you want to create. Consequently, a 
"call to a constructor" cannot be virtual.
```

### Why does the copy constructor function must use a reference for the paramater
```c++
#include <iostream>
using namespace std;

class A {
public:
    A(int a) { var = a;}
    A(const A& a) { var = a.var;}
    // using A(A a) {var = a.var; } will cause compiler error
    ~A() {}
    int get() const {return var;}
private:
    int var;
};

int main(int argc, char const *argv[])
{
    A a(3);
    A b = a;    // call copy constructor function
    cout << b.get() << endl;
    return 0;
}
```


### 虚类的构造函数和析构函数执行顺序
```c++

class Test {
public:
    Test() {cout << "Test Constructed" << endl;}
    ~Test() {cout << "Test Destructed" << endl;}
};
class Base {
public:
    Base() {cout << "Base Constructed" << endl;}
    virtual ~Base() {cout << "Base Destructed" << endl;}
};
class Derived: public Base
{
public:
    Derived() {cout << "Derived Constructed" << endl;}
    virtual ~Derived() {cout << "Derived Destructed" << endl;}
private:
    Test t;
};

int main(int argc, char const *argv[])
{
    Base *bptr = new Derived();
    delete bptr;
    return 0;
}

输出结果：
Base Constructed
Test Constructed
Derived Constructed
Derived Destructed
Test Destructed
Base Destructed

原因：
delete指向派生类的基类指针构造函数和析构函数的执行顺序如下：
基类构造函数->成员变量的构造函数->自身构造函数
自身析构函数->成员变量析构函数->基类析构函数
```

### 虚函数表的修改
```c++
class animal
{
protected:
    int age;
public:
    virtual void print_age(void) = 0;
};

class dog : public animal
{
public:
       dog() {this -> age = 2;}
       ~dog() { }
       virtual void print_age(void)
       {
           cout<<"Wang, my age = "<<this -> age<<endl;
       }
};

class cat: public animal
{
public:
    cat() {this -> age = 1;};
    ~cat() { }
    virtual void print_age(void)
    {
        cout<<"Miao, my age = "<<this -> age<<endl;
    }
};

int main(void)
{
    cat kitty;
    dog jd;
    animal * pa;
    int * p = (int *)(&kitty);
    int * q = (int *)(&jd);
    p[0] = q[0];
    pa = &kitty;
    pa -> print_age();
    return 0;
}

输出结果：
Wang, my age = 1

原因：
理解虚函数表以及类的存储结构
int * p = (int *)(&kitty)   // p指向kitty
int * q = (int *)(&jd)      // q指向jd
p[0] = q[0]   // 把kitty的指向cat::print_age的指针值，修改成指向了dog::print_age
pa = &kitty   // pa指向kitty
pa->print_age()  // 调用的是刚刚被修改过的函数指针，也就是dog::print_age函数，但是
// 在this->age的这个语句的this是kitty,age也就自然是kitty的1
```

### 类的大小测试
```c++
class A {
public:
    virtual void f() {}
};
// 为了使不同的类具有不一样的地址，编译器回自动给空类加上一个字节
class B {};
class C : public B {
public:
    void f() {}
};
class D: public C, public A {};
class E {
private:
    static int f;
};

class F {
private:
    int a;
};

class G {
public:
    G(){}
    ~G(){}
    void ff() {}
};

int main(int argc, char const *argv[])
{
    cout << "sizeof int*: " << sizeof(int*) << endl;
    cout << "sizeof int: " << sizeof(int) << endl;
    cout << "sizeof A: " << sizeof(A) << endl;
    cout << "sizeof B: " << sizeof(B) << endl;
    cout << "sizeof C: " << sizeof(C) << endl;
    cout << "sizeof D: " << sizeof(D) << endl;
    cout << "sizeof E: " << sizeof(E) << endl;
    cout << "sizeof F: " << sizeof(F) << endl;
    cout << "sizeof G: " << sizeof(G) << endl;
    return 0;
}

输出结果（64位系统）：
sizeof int*: 8
sizeof int: 4
sizeof A: 8
sizeof B: 1
sizeof C: 1
sizeof D: 8
sizeof E: 1
sizeof F: 4
sizeof G: 1
结论：
/*
类的大小：
１．为类的非静态成员数据的类型大小之和．
２．有编译器额外加入的成员变量的大小，用来支持语言的某些特性（如：指向虚函数的指针）．
３．为了优化存取效率，进行的边缘调整．
４　与类中的构造函数，析构函数以及其他的成员函数无关．
*/
```


类的建立方式
----
### 静态建立
静态建立一个对象是由编译器为对象在栈空间中分配内存，是通过直接移动栈顶指针，挪出适当的空间，然后在这片内存空间上调用构造函数形成一个栈对象；使用这种方法，直接调用类的构造函数。例如下面例子：
```c++
class A {
public:
    A() {...}
};

A a;
```

### 动态建立

动态建立类的对象，是使用new运算符将对象建立在堆空间中，这个过程分两步，第一步是执行operator new()函数，在堆空间中搜索合适的内存并进行分配；第二步是调用构造函数构造对象，初始化这片内存空间；这种方法，间接调用类的构造函数。
```c++
class A {
public:
    A() {...}
};

A *ptr = new A();
```

### 建立只能在栈上面创建的类
只有使用new运算符的对象才会建立在堆上面，因此，只需要禁用new运算符就可以实现类对象只能建立在栈上。将operator new()设置为私有方法即可。
```c++
class A {
public:
    A() {...}
    ~A() {...}
private:
    void* operator new(size_t t) {}     // 注意函数的第一个参数和返回值都是固定
    void operator delete(void *p) {}    // 重载new就需要重载delete
};
```

### 建立只能在堆上面创建的类
当对象建立在栈上面时，是由编译器分配内存空间的，调用构造函数来构造栈对象。当对象使用完后，编译器会调用析构函数来释放栈对象所占的空间。编译器管理了对象的整个生命周期。如果编译器无法调用类的析构函数，情况会是怎样的呢？比如，类的析构函数是私有的，编译器无法调用析构函数来释放内存。所以，编译器在为类对象分配栈空间时，会先检查类的析构函数的访问性，其实不光是析构函数，只要是非静态的函数，编译器都会进行检查。如果类的析构函数是私有的，则编译器不会在栈空间上为类对象分配内存。
```c++
class A {
public:
    A() {...}
    void destroy() { delete this; } // 使用完类后必须调用这个方法释放资源
private:
    ~A() {...}
};

// 下面是个继承版本
class A {
public:
    static A* create() { return new A(); }
    void destroy() { delete this; }
protected:
    A() {...}
    virtual ~A() {...}
};
```

指针
----
### 数组+1时移动距离
```C++
int main(int argc, char const *argv[])
{
    int a[4] = {1, 2, 3, 4};
    int *ptr = (int*)(&a+1);
    printf("%d\n", *(ptr-1));
    return 0;
}

输出结果：
4

原因：
取标识符a它的地址加1会移动它本身元素个数的长度，
也就是说&a + 1 会向后移动四个位置,如下：
[1][2][3][4][null]
 |            |
 a           &a+1
```

### 指针移动
```c++
#include <iostream>
#include <cstdio>
using namespace std;

int main(int argc, char const *argv[])
{
    char *p[] = {"A", "B", "C"};
    char **pp[] = {p+2, p+1, p};
    char ***ppp = pp;
    printf("%s\n", **++ppp);
    printf("%s\n", *++*++ppp);
    return 0;
}

输出结果：
B
B

原因：
'++'和取值'*'运算的优先级是一样的，所以靠近的先执行；
'**++ppp'的执行顺序是先把ppp向后移动一位，在两次取值，所以输出"B";
'*++*++ppp'的执行顺序是先把ppp向后移动一位，再取值，得到的值是p，
然后对p进行'++'操作得到的是p+1的地址也就是指向字符串"B"

图示如下：
(1):                          (2)++ppp执行之后:     
["A"]["B"]["C"]               ["A"]["B"]["C"]      
  |    |    |                   |    |    |        
 [p0] [p1] [p2]                [p0] [p1] [p2]      
  |                             |                  
  p                             p                  
    [p2][p1][p0]                  [p2][p1][p0]     
     | \                          |     \          
     pp ppp                       pp    ppp        

(3)继续执行++ppp:              (4)最后++ppp执行之后:  
["A"]["B"]["C"]               ["A"]["B"]["C"]      
  |    |    |                   |    |    |        
 [p0] [p1] [p2]                [p0] [p1] [p2]      
  |                             |                  
  p                             p                  
    [p2][p1][p0]                  [p2][p1][p0]     
     |        \                    |        \      
     pp       ppp                  pp       ppp    

```

const关键字
----
### const修饰指针
[Clockwise/Spiral Rule](http://c-faq.com/decl/spiral.anderson.html)

[stackoverflow上的详解](http://stackoverflow.com/questions/1143262/what-is-the-difference-between-const-int-const-int-const-and-int-const)

![](https://raw.githubusercontent.com/zhushh/Note/master/img/const2.png)

### const修饰类的成员变量及成员函数
* 1.类的成员变量被const修饰时，需要在构造函数初始化列表初始化
```c++
class A {
public:
    A(int a) : age(a) {}
private:
    const int age;
}
```
* 2.类的成员函数被const修饰的时候，不能对类的成员变量进行修改且在函数体中不能调用非const函数
```c++
class A {
public:
    A() {}
    void printAge() { cout << age << endl; }
    int getAge() const {
        age++;    // Error
        printAge();   // Error
        return age;
    }
private:
    int age;
}
```

函数
----
### 函数参数入栈顺序
```c++
#include <stdio.h>
int ff(int a, int b, int c) {
    return 0;
}
int main(int argc, char const *argv[])
{
    return ff(printf("A"), printf("B"), printf("C"));
}

输出结果：
CBA

原因：
函数参数入栈顺序是从右向左，所以先执行打印C，在打印B，最后打印A
```

typename关键字
----
[参考链接](https://zh.wikipedia.org/wiki/Typename)
### class关键字的同义词
在c++编程语言的泛型编程中，typename关键字用于引入一个模板参数，例如：
```c++
template <typename T>
const T& max(const T& x, const T& y) {
    if (y < x) {
        return x;
    }
    return y;
}
```
这种情况下，typename可用class这个关键字代替，如下代码所示：
```c++
template <class T>
const T& max(const T& x, const T& y) {
    if (y < x) {
        return x;
    }
    return y;
}
```
以上两段代码没有功能上的区别。

### 类型名指示符
先看下面错误的代码：
```c++
template <typename T>
void foo(const T& t) {
    // 声明一个指针指向某个类型为T::bar的对象的指针
    T::bar *p;
}

struct StructWithBarAsType {
    typedef int bar;
};

int main() {
    StructWithBarAsType x;
    foo(x);
}
```
这段代码是不能通过编译的，因为编译器不知道T::bar究竟是一个类型的名字还是一个某个变量的名字；
c++标准规定：
>A name used in a template declaration or definition and that is dependent on a template-parameter is assumed not to name a type unless the applicable name lookup finds a type name or the name is qualified by the keyword typename.

意即出现上述歧义时，编译器将自动默认bar是一个变量名，而不是类名；所以上面中的T::bar * p会被
解释成为乘法，而不是p为指向T::bar类型的对象的指针。
要解决上面的问题，就是显示地告诉编译器，T::bar是一个类型名，就必须用关键字typename,例如：
```c++
template <typename T>
void foo(const T& t) {
    // 声明一个指向某个类型为T::bar的对象的指针
    typename T::bar *p;
}
```
这样编译器就确定T::bar是一个类型名，p自然就被解释为指向T::bar类型的对象的指针了。


static_cast,reinterpret_cast,const_cast和dynamic_cast
----
### const_cast
用于移除变量的const
```cpp
#include <iostream>
using namespace std;

class A {
public:
    A(int i): val(i) {}
    void constFunc(int i) const {
        // this->val = i;   // compile error: this is a pointer to const
        const_cast<A*>(this)->val = i;  // OK as long as the type object isn't const
    }
    int getVal() const {
        return val;
    }
private:
    int val;
};

int main(int argc, char const *argv[])
{
    A a(2);
    cout << a.getVal() << endl;
    a.constFunc(4);
    cout << a.getVal() << endl;
    return 0;
}

//上面的输出结果为：
//2
//4
```

### dynamic_cast
可安全地把基类指针转换成派生类指针，如果不能转换那么会赋值出错
```cpp
#include <iostream>
using namespace std;

class B {
public:
    virtual ~B() {}
};

class D : public B {
public:
    virtual void name() {}
};

int main(int argc, char const *argv[])
{
    B *b1 = new B;
    if (D *d = dynamic_cast<D*>(b1)) {
        std::cout << "downcast from b1 to d successful\n";
        d->name();  // safe to call
    }
    B *b2 = new D;
    if (D *d = dynamic_cast<D*>(b2)) {
        std::cout << "downcast from b2 to d successful\n";
        d->name();  // safe to call
    }
    return 0;
}

//输出结果为：
//downcast from b2 to d successful
```

### static_cast
完成相关类型之间的转换
```cpp
#include <vector>
#include <iostream>
 
struct B {
    int m = 0;
    void hello() const {
        std::cout << "Hello world, this is B!\n";
    }
};
struct D : B {
    void hello() const {
        std::cout << "Hello world, this is D!\n";
    }
};
 
enum class E { ONE = 1, TWO, THREE };
enum EU { ONE = 1, TWO, THREE };
 
int main()
{
    // 1: initializing conversion
    int n = static_cast<int>(3.14); 
    std::cout << "n = " << n << '\n';
    std::vector<int> v = static_cast<std::vector<int>>(10);
    std::cout << "v.size() = " << v.size() << '\n';
 
    // 2: static downcast
    D d;
    B& br = d; // upcast via implicit conversion
    br.hello();
    D& another_d = static_cast<D&>(br); // downcast
    another_d.hello();
 
    // 3: lvalue to xvalue
    std::vector<int> v2 = static_cast<std::vector<int>&&>(v);
    std::cout << "after move, v.size() = " << v.size() << '\n';
 
    // 4: discarded-value expression
    static_cast<void>(v2.size());
 
    // 5. inverse of implicit conversion
    void* nv = &n;
    int* ni = static_cast<int*>(nv);
    std::cout << "*ni = " << *ni << '\n';
 
    // 6. array-to-pointer followed by upcast
    D a[10];
    B* dp = static_cast<B*>(a);
 
    // 7. scoped enum to int or float
    E e = E::ONE;
    int one = static_cast<int>(e);
    std::cout << one << '\n';
 
    // 8. int to enum, enum to another enum
    E e2 = static_cast<E>(one);
    EU eu = static_cast<EU>(e2);
 
    // 9. pointer to member upcast
    int D::*pm = &D::m;
    std::cout << br.*static_cast<int B::*>(pm) << '\n';
 
    // 10. void* to any type
    void* voidp = &e;
    std::vector<int>* p = static_cast<std::vector<int>*>(voidp);
}

// output:
// n = 3
// v.size() = 10
// Hello world, this is B!
// Hello world, this is D!
// after move, v.size() = 0
// *ni = 3
// 1
// 0
```


### reinterpret_cast
完成不相关类型直接的转换
```cpp
#include <cstdint>
#include <cassert>
#include <iostream>
int f() { return 42; }
int main()
{
    int i = 7;
 
    // pointer to integer and back
    uintptr_t v1 = reinterpret_cast<uintptr_t>(&i); // static_cast is an error
    std::cout << "The value of &i is 0x" << std::hex << v1 << '\n';
    int* p1 = reinterpret_cast<int*>(v1);
    assert(p1 == &i);
 
    // pointer to function to another and back
    void(*fp1)() = reinterpret_cast<void(*)()>(f);
    // fp1(); undefined behavior
    int(*fp2)() = reinterpret_cast<int(*)()>(fp1);
    std::cout << std::dec << fp2() << '\n'; // safe
 
    // type aliasing through pointer
    char* p2 = reinterpret_cast<char*>(&i);
    if(p2[0] == '\x7')
        std::cout << "This system is little-endian\n";
    else
        std::cout << "This system is big-endian\n";
 
    // type aliasing through reference
    reinterpret_cast<unsigned int&>(i) = 42;
    std::cout << i << '\n';
}

// output:
// The value of &i is 0x7ffeb2c3a99c
// 42
// This system is little-endian
// 42
```

左值引用和右值引用
----
### 左值引用和右值引用
[http://en.cppreference.com/w/cpp/language/reference](http://en.cppreference.com/w/cpp/language/reference)
```

```

### 移动构造函数和赋值运算符
[https://msdn.microsoft.com/zh-cn/library/dd293665.aspx](https://msdn.microsoft.com/zh-cn/library/dd293665.aspx)


字节序与struct结构体
----
### 字节序
是指占内存多于一个字节类型的数据在内存中的存放顺序，通常有小端、大端两种字节顺序。
小端字节序是指,**低字节**数据存放在低地址处，**高字节**数据存放在内存高地址处；
大端字节序是指,**高字节**数据存放在低地址处，**低字节**数据存放在内存高地址处。

基于X86平台的PC机是小端字节序的，而有的嵌入式平台则是大端字节序的。所有网络协议也都是采用big endian的方式来传输数据的。所以有时我们也会把big endian方式称之为网络字节序。

比如数字0x12345678在两种不同字节序CPU中的存储顺序如下所示：
```
Big Endian
低地址                                            高地址
---------------------------------------------------->
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|     12     |      34    |     56      |     78    |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

Little Endian
低地址                                            高地址
---------------------------------------------------->
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|     78     |      56    |     34      |     12    |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```
从上面两图可以看出，采用Big Endian方式存储数据是符合我们人类的思维习惯的。

联合体union的存放顺序是所有成员都从低地址开始存放，利用该特性，就能判断CPU对内存采用Little-endian还是Big-endian模式读写。

### 字节对齐
理论上任何类型的变量都可以从任何地址开始访问，但实际情况是在访问特定变量的时候，经常在特定的内存地址访问，这就需要各种数据按照一定的规则在空间上排列，而不是顺序一个接一个的排放；
* 为什么需要字节对齐？

    1.某些平台只能在特定的地址访问特定的类型数据

    2.为了提高提取存取数据的速度，进行字节对齐
* 字节对齐的原则

    1.数据成员对齐原则：
    ```
    结构体的数据成员，第一个数据成员放在offset为0的地址，以后每个数据成员存储的起始位置要从该
    成员的大小或成员的子成员大小（比如说数组或结构体）的整数倍开始（比如int为4字节，所以要从4
    的整数倍地址开始存储）
    ```

    2.结构体作为成员对齐原则：
    ```
    如果一个结构里有某些结构体成员，则结构体成员要从其内部最大元素大小的整数倍地址开始存储。（
    struct a里面存有struct b，b里面有char，int，double等元素，那b应该从8的整数倍开始存
    储）
    ```

    3.收尾工作：
    ```
    结构体的总大小，也就是sizeof的结果，必须是其内部最大成员的整数倍，不足的要补齐。
    ```

### 结构体字节对齐
```c++
struct T {
    short a;
    int b;
    char c;
};
```
上面的结构体大小为12bytes，但是换成下面的顺序，大小就是8bytes，原因是因为结构体内部成员的字节对齐
```c++
struct T {
    short a;
    char c;
    int b;
};
```
### 匿名结构体/联合体
 编译运行下面代码
```c++
#include <stdio.h>
#include <stdlib.h>

struct T {
    int type;
    int size;

    /* 匿名联合体，`ch`和`value`就相当于是`struct T`的成员变量 */
    union {
        char ch;
        int value;
    };

    /* 类似于匿名联合体， `struct T`可以直接省略结构体的名称使用`one`和`two` */
    struct {
        struct T* one;
        struct T* two;
    };
};

int main(int argc, char const *argv[])
{
    struct T a = {1, 3, 12};
    struct T b = {2, 2, 'a'};
    struct T c = {3, 1, 4, &a, &b};

    printf("%3d %3d %4d\n", a.type, a.size, a.value);
    printf("%3d %3d %4c\n", b.type, b.size, b.ch);
    printf("%3d %3d %4d %4d\n", c.type, c.size, (c.one)->type, (c.two)->type);
    return 0;
}
```
输出如下
```
  1   3   12
  2   2    a
  3   1    1    2
```

### Extern C in C++的作用
在C++代码中，经常可以看到如下代码：
```c++
#ifdef __cplusplus
extern C {
#endif

#ifdef __cplusplus
}
#endif
```
上面这个用法的原因是，为了使C能够调用C++中的函数；为什么C不能直接调用呢？原因还得从编译链接说起，c++使用的编译器是C++编译器，C++中存在
函数重载，所以c++代码编译的时候，识别一个函数需要根据函数名+参数来区分不同的函数，但是在C语言中，是用函数名就可以进行区分的，这就导致C linker
链接一个C++库函数时，需要兼容性，所以c++为了使函数能够被C回调使用，就在头文件的地方使用extern C来进行编译，表示支持给C回调使用；

[https://stackoverflow.com/questions/1041866/what-is-the-effect-of-extern-c-in-c](https://stackoverflow.com/questions/1041866/what-is-the-effect-of-extern-c-in-c)
