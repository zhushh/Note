Makefile教程
============================

1.1 概述
----
makefile由许多规则构成，每条规则格式如下：
    
```
<Target> : <prequisites>
<Tab> <Command>
```
<Target>是必需的，<prequisites>和<Command>是可选的，但是最少要有其中一个；

1.2 目标文件(Target)
----
一个目标文件就构成一条规则，一般是文件名，指makefile我呢见所要构建的对象，比如a.txt。
目标文件可以是一个文件，也可以是多个文件名，之间用空格分隔。

除了文件名，目标文件还可以是操作名字，这称为“伪目标”(phony target).
```
clean:
	rm *.o
```
上面的clean不是文件名，而是一个操作名字，属于“伪目标”，作用是删除对象文件。

但是，当当前目录中，正好有一个文件叫做clean，那么这个命令不会执行。
因为make发现clean文件已经存在，就认为没有必要重新构建，所以不会执行指定的rm命令。

为了避免这种情况，可以确定生命clean是“伪目标”，写法如下：
```
.PHONY: clean
clean:
	rm *.o temp
```

如果make命令没有指定目标，默认会执行makefile文件的第一个目标。
```shell
$ make
```
上面命令执行makefile文件第一个目标。

1.3 前置条件（prequisites）
----
前置条件一般是一组文件名，之间用空格分隔。它指定了“目标”是否重新构建的判断标准：只要有一个前置文件不存在，或者有过更新（前置文件的last-modification时间戳比目标的时间戳新），“目标”就需要重新构建。
```
result.txt: source.txt
	cp source.txt result.txt
```
上面代码中，构建result.txt的前置条件就是source.txt，如果当前目录中的source.txt已经存在，那么make result.txt可以正常运行，
否则必须再写一条规则，来生成source.txt。
```
source.txt:
	echo "this is source.txt"  > source.txt
```
上面makefile文件的source.txt目标没有前置条件，只要这个文件还存在，每次make source.txt都会生成。
```
$ make result.txt
$ make result.txt
```
连续执行两次，第一次执行会先新建source.txt，然后新建result.txt。第二次执行，make发现source.txt没有变动，所以不会执行任何操作。

1.4 命令(command)
----
命令表示如何更新目标文件，由一行或多行shell命令组成。是构建目标文件的具体指令，它的运行结果通常就是生成目标文件。

<em>每行命令之前必须有一个tab键</em>。

需要注意的是，每行命令在一个单独的shell中执行，这些shell之间没有继承关系。比如：
```
var-host:
	export foo=bar
	echo "$foo=[$$foo]"
```
上面运行make之后，取不到foo的值，因为这两个命令在两个不同的进程执行；一个解决办法是将两个命令行写在一行，中间用分号分隔。
```
var-kept:
	export foo=bar; echo "foo=[$$foo]"
```
另一种解决办法是，在换行前加上反斜杠转义：
```
var-kept:
	export foo=bar; \
	echo "foo=[$$foo]"
```
最后一个方法是加上`.ONESHELL:`命令：
```
.ONESHELL:
var-kept:
	export foo=bar
	echo "foo=[$$foo]"
```






