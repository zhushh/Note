#### 问题说明

线上程序出现cpu高负载，需要进行定位原因处理。



### 分析

##### 相关命令

- perf：程序性能分析
- top：进程内存/cpu数据
- netstat：网络相关



##### 分析步骤

1.perf stat：查看程序运行时整体情况，包括以下数据信息：

```
Task-clock-msecs：CPU 利用率，该值高，说明程序的多数时间花费在 CPU 计算上而非 IO。

Context-switches：进程切换次数，记录了程序运行过程中发生了多少次进程切换，频繁的进程切换是应该避免的。

Cache-misses：程序运行过程中总体的 cache 利用情况，如果该值过高，说明程序的 cache 利用不好

CPU-migrations：表示进程 t1 运行过程中发生了多少次 CPU 迁移，即被调度器从一个 CPU 转移到另外一个 CPU 上运行。

Cycles：处理器时钟，一条机器指令可能需要多个 cycles，

Instructions: 机器指令数目。

IPC：是 Instructions/Cycles 的比值，该值越大越好，说明程序充分利用了处理器的特性。

Cache-references: cache 命中的次数

Cache-misses: cache 失效的次数。
```



2.perf top: 查询耗时cpu较前的程序及函数

```
  59.32%  reader_qmf_pay                [.] runtime.memmove
  1.78%  [kernel]                      [k] _raw_spin_unlock_irqrestore
  1.58%  [kernel]                      [k] finish_task_switch
  1.29%  [vdso]                        [.] 0x0000000000000c68
  1.18%  reader_qmf_pay                [.] runtime.memclrNoHeapPointers
  1.07%  reader_qmf_pay                [.] fmt.(*pp).doPrintf
  0.93%  reader_qmf_pay                [.] runtime.findObject
  0.89%  [kernel]                      [k] iowrite16
  0.86%  reader_qmf_pay                [.] runtime.mallocgc
  0.76%  libc-2.17.so                  [.] vfprintf
  0.73%  reader_qmf_pay                [.] runtime.procyield
  0.62%  reader_qmf_pay                [.] fmt.(*fmt).fmtInteger
  0.53%  [kernel]                      [k] __do_softirq
  0.53%  reader_qmf_pay                [.] runtime.(*itabTableType).find
  0.49%  reader_qmf_pay                [.] runtime.gcWriteBarrier
  0.49%  reader_qmf_pay                [.] runtime.scanobject
  0.47%  reader_qmf_pay                [.] fmt.(*fmt).pad
  0.42%  reader_qmf_pay                [.] math/rand.(*rngSource).Seed
```



3.perf record + report：记录程序执行数据，并生成报表进行分析

```
$ perf record -e cycles -o cycles.perf -g -p 5330
$ perf report -i cycles.perf > result.txt
$ vim result.txt
```





#### 参考

https://www.ibm.com/developerworks/cn/linux/l-cn-perf1/index.html



