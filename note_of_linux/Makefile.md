Makefile教程
============================

1.1 概述
----
makefile由许多规则构成，每条规则格式如下：
    
```
<Target> : <Requirements>
<Tab> <Command>
```
<Target>是必需的，<Requirements>和<Command>是可选的，但是最少要有其中一个；

1.2 目标文件<Target>
----
一个目标文件就构成一条规则，一般是文件名，指makefile我呢见所要构建的对象，比如a.txt。
目标文件可以是一个文件，也可以是多个文件名，之间用空格分隔。

除了文件名，目标文件还可以是操作名字，这称为“伪目标”(phony target).
```
clean:
	rm *.o
```

