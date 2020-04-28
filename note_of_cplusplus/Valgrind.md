#### valgrind

c++内存泄漏检查工具



#### 安装使用

ubuntu:

```
$ sudo apt install valgrind
```

centos:

```
# yum install valgrind
```



#### 例子

问题现象：程序正常执行完成，然后在析构函数出现coredump

gdb进行调试：显示是内存库`/lib64/libc.so.6` 执行free操作的时候异常

直接执行内存检查工具：`valgrind --tool=memcheck [program] [args...]`

```
$ valgrind --tool=memcheck ./target 1
```



#### 输出结果分析

valgrind输出结果会报告5种内存泄露，这五种内存泄露分析如下：

- "definitely lost"：确认丢失。程序中存在内存泄露，应尽快修复。当程序结束时如果一块动态分配的内存没有被释放且通过程序内的指针变量均无法访问这块内存则会报这个错误。 

- "indirectly lost"：间接丢失。当使用了含有指针成员的类或结构时可能会报这个错误。这类错误无需直接修复，他们总是与"definitely lost"一起出现，只要修复"definitely lost"即可。例子可参考我的例程。

- "possibly lost"：可能丢失。大多数情况下应视为与"definitely lost"一样需要尽快修复，除非你的程序让一个指针指向一块动态分配的内存（但不是这块内存起始地址），然后通过运算得到这块内存起始地址，再释放它。例子可参考我的例程。当程序结束时如果一块动态分配的内存没有被释放且通过程序内的指针变量均无法访问这块内存的起始地址，但可以访问其中的某一部分数据，则会报这个错误。

- "still reachable"：可以访问，未丢失但也未释放。如果程序是正常结束的，那么它可能不会造成程序崩溃，但长时间运行有可能耗尽系统资源，因此笔者建议修复它。如果程序是崩溃（如访问非法的地址而崩溃）而非正常结束的，则应当暂时忽略它，先修复导致程序崩溃的错误，然后重新检测。

- "suppressed"：已被解决。出现了内存泄露但系统自动处理了。可以无视这类错误。这类错误我没能用例程触发，看官方的解释也不太清楚是操作系统处理的还是valgrind，也没有遇到过。所以无视他吧~

例子：

```
/home/sshuangzhu $ valgrind --tool=memcheck ./TARGET 
==4828== 
==4828== HEAP SUMMARY:
==4828==     in use at exit: 40,920 bytes in 5 blocks
==4828==   total heap usage: 150 allocs, 145 frees, 45,734 bytes allocated
==4828== 
==4828== LEAK SUMMARY:
==4828==    definitely lost: 40,920 bytes in 5 blocks
==4828==    indirectly lost: 0 bytes in 0 blocks
==4828==      possibly lost: 0 bytes in 0 blocks
==4828==    still reachable: 0 bytes in 0 blocks
==4828==         suppressed: 0 bytes in 0 blocks
==4828== Rerun with --leak-check=full to see details of leaked memory
==4828== 
==4828== For counts of detected and suppressed errors, rerun with: -v
==4828== ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0)
```



#### 相关阅读

valgrind使用简介：https://blog.csdn.net/gatieme/article/details/51959654

linux配置开启core文件：https://blog.csdn.net/star_xiong/article/details/43529637

c++内存释放出现coredump问题：

https://www.cnblogs.com/hokyhu/archive/2012/09/14/2685437.html

