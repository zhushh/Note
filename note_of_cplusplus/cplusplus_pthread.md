## cplusplus pthread和信号量

Hello World
----
编译命令为：
```bash
$ gcc pth_hello.c -o pth_hello -lpthread
```
pth_hello.c文件如下：
```cpp
#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

long thread_count;

void* hello(void*);

int main(int argc, char** argv) {
    thread_count = strtol(argv[1], NULL, 10);
    long thread;
    pthread_t *thread_handlers;
    thread_handlers = (pthread_t*)malloc(thread_count*sizeof(pthread_t));

    for (thread = 0; thread < thread_count; thread++) {
        pthread_create(&thread_handlers[thread], NULL, hello, (void*)thread);
    }
    printf("Hello world from main.\n");

    for (thread = 0; thread < thread_count; thread++) {
        pthread_join(thread_handlers[thread], NULL);
    }

    free(thread_handlers);
    return 0;
}

void* hello(void* rank) {
    long my_rank = (long)rank;
    printf("Hello world from thread %ld.\n", my_rank);
    return NULL;
}
```

pthread函数
----
```cpp
pthread_t // 不透明的对象,存储的数据都是系统绑定,用户级无法直接访问里面数据
pthread_create(
    pthread_t*              thread_p,                   /* out */
    const pthread_attr_t*   attr_p,                     /* in */
    void*                   (*start_routine)(void*),    /* in */
    void*                   arg_p                       /* in */
);
pthread_join(
    pthread_t   thread,     /* in */
    void**      ret_val_p   /* out */
);

// use pthread_join(tid, &ret_val_p) to get the ret_val_ptr value
pthread_exit(
    void *ret_val_ptr  /* in */
);
```

概念词语
----
* 竞争条件(race condition)
```
当多个线程要访问共享变量或共享文件时，如果至少有一个访问是更新操作，那么这些访问就可能会导致某种错误，这种情况就叫竞争条件
```
* 临界区(critical section)
```
一段共享的代码段，每次只允许一个线程进入该代码段
```
* 忙等待
```
1. y = Compute(my_rank);
2. while (flag != my_rank);    // 此处一直检测flag值，处于忙等待状态
3. x = x+y;
4. flag++;
忙等待有可能在编译器开启编译优化的时候可能会失效，比如上面进行编译优化后可能为：
1. y = Compute(my_rank);
2. x = x + y
3. while (flag != my_rank);
4. flag ++
```

pthread计算矩阵乘法
----
```cpp
#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

long thread_count;
int m, n;
double *x;
double *y;
double **A;

void* Pth_mat_vect(void*);

int main(int argc, char** argv) {
    thread_count = strtol(argv[1], NULL, 10);
    long thread;
    pthread_t* thread_handlers;
    thread_handlers = (pthread_t*)malloc(thread_count*sizeof(pthread_t));
    scanf("%d %d", &m, &n);
    x = (double*)malloc(n*sizeof(double));
    y = (double*)malloc(m*sizeof(double));
    A = (double**)malloc(m*sizeof(double*));
    for (int i = 0; i < m; i++) {
        A[i] = (double*)malloc(n*sizeof(double));
        // 读取矩阵行元素
        for (int j = 0; j < n; j++) {
            scanf("%lf", &A[i][j]);
        }
    }
    // 读入向量x
    for (int i = 0; i < n; i++) {
        scanf("%lf", &x[i]);
    }

    for (thread = 0; thread < thread_count; thread++) {
        pthread_create(&thread_handlers[thread], NULL, Pth_mat_vect, (void*)thread);
    }

    for (thread = 0; thread < thread_count; thread++) {
        pthread_join(thread_handlers[thread], NULL);
    }

    printf("The result:\n");
    for (int i = 0; i < m; i++) {
        printf("%lf\n", y[i]);
    }
    free(thread_handlers);
    free(x);
    free(y);
    for (int i = 0; i < m; i++) {
        free(A[i]);
    }
    free(A);
    return 0;
}

void* Pth_mat_vect(void*rank) {
    long my_rank = (long)rank;
    int my_m = m / thread_count;
    int my_first_row = my_m * my_rank;
    int my_last_row = my_m + my_first_row;

    for (int i = my_first_row; i <= my_last_row && i < m; i++) {
        y[i] = 0.0;
        for (int j = 0; j < n; j++) {
            y[i] += A[i][j] * x[j];
        }
    }
    return NULL;
}
```

互斥量
----
```
互斥锁的简称，是一个特殊的变量，可以通过某些特殊类型的函数，互斥量可以用来限制每次只有一个线程能进入临界区。

锁的粒度：指锁住的数据范围大小，比如锁住整个数组还是对每个数组的元素单独进行加锁；
锁粒度的大小需要合适，太大对并发性没有什么提升，太小又会消耗太多的锁资源，需要在复杂性和性能之间找到平衡；
```

* 函数操作
```cpp
pthread_mutexattr_t // 特殊的类型变量，用来做互斥量
int pthread_mutex_init(
    pthread_mutex_t*            mutex_p,    /* out */
    const pthread_mutexattr_t*  attr_p      /* in */
);
int pthread_mutex_destroy(pthread_mutex_t* mutex_p);
int pthread_mutex_lock(pthread_mutext_t* mutex_p);
int pthread_mutex_unlock(pthread_mutex_t* mutex_p);
```

计算Pi的值例子
----
```cpp
#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

long thread_count;
pthread_mutex_t mutex;
long long n;
double sum;

void* Thread_sum(void*);

int main(int argc, char** argv) {
    thread_count = strtol(argv[1], NULL, 10);
    n = strtol(argv[2], NULL, 10);
    long thread;
    pthread_t* thread_handlers;
    thread_handlers = (pthread_t*)malloc(thread_count*sizeof(pthread_t));
    pthread_mutex_init(&mutex);

    for (thread = 0; thread < thread_count; thread++) {
        pthread_create(&thread_handlers[thread], NULL, Thread_sum, (void*)thread);
    }

    for (thread = 0; thread < thread_count; thread++) {
        pthread_join(thread_handlers[thread], NULL);
    }

    printf("Pi = %lf\n", 4.0*sum);

    pthread_mutex_destroy(&mutex);
    free(thread_handlers);
    return 0;
}

void* Thread_sum(void* rank) {
    long my_rank = (long)rank;
    long long my_n = n / thread_count;
    long long my_first_i = my_n*my_rank;
    long long my_last_i = my_first_i + my_n;
    double factor;
    double local_sum = 0.0;
    if (my_first_i%2 == 0) {
        factor = 1.0;
    } else {
        factor = -1.0;
    }
    for (long long i = my_first_i; i < my_last_i; i++, factor = -factor) {
        local_sum += factor*(2*i+1);
    }
    pthread_mutex_lock(&mutex);
    sum += local_sum;
    pthread_mutex_unlock(&mutex);
    return NULL;
}
```

读写锁
----
```
与互斥量相似，但是允许更高的并发性。互斥锁要么是锁住状态，要么是不加锁状态，而且一次只有一个线程可以对其加锁。
读写锁有三种状态：读模式下的加锁状态，写模式下的加锁状态，不加锁状态；
一次只有一个线程可以占有写模式的读写锁，但是可以有多个线程同时占用读模式的读写锁；
```

* 操作函数
```c++
int pthread_rwlock_init(
    pthread_rwlock_t* rwlock,           /* out */
    const pthread_rwlockattr_t* attr    /* in */
);
int pthread_rwlock_destroy(
    pthread_rwlock_t* rwlock    /* in */
);

// 所有函数成功返回0，否则，返回错误编号
int pthread_rwlock_rdlock(pthread_rwlock_t* rwlock);
int pthread_rwlock_wrlock(pthread_rwlock_t* rwlock);
int pthread_rwlock_unlock(pthread_rwlock_t* rwlock);

int pthread_rwlock_tryrdlock(pthread_rwlock_t* rwlock);
int pthread_rwlock_trywrlock(pthread_rwlock_t* rwlock);
```

读写锁实现的作业队列
----
```cpp
#include <iostream>
#include <queue>
using namespace std;

#include <cstdio>
#include <cstdlib>
#include <pthread.h>

struct Job {
    struct Job *j_next;
    struct Job *j_prev;
    pthread_t j_id;
};

class JobQueue {
public:
    JobQueue() {
        q_head = NULL;
        q_tail = NULL;
        int err;
        if ((err = pthread_rwlock_init(&q_lock)) != 0) {
            exit(err);
        }
    }
    ~JobQueue() {
        struct Job* ptr = q_head;
        while (q_head != NULL) {
            q_head = q_head->next;
            delete ptr;
            ptr = q_head;
        }
        pthread_rwlock_destroy(q_lock);
    }

    void insert(const struct Job* job) {
        pthread_rwlock_wrlock(q_lock);
        job->j_next = q_head;
        job->j_prev = NULL;
        if (q_head == NULL) {
            q_tail = jp;
        } else {
            q_head->j_prev = job;
        }
        q_head = job;
        pthread_rwlock_unlock(q_lock);
    }

    void append(const struct Job* job) {
        pthread_rwlock_wrlock(q_lock);
        job->j_prev = q_tail;
        job->j_next = NULL;
        if (q_tail == NULL) {
            q_head = job;
        } else {
            q_tail->j_next = job;
        }
        q_tail = job;
        pthread_rwlock_unlock(q_lock);
    }

    void remove(const struct Job* job) {
        pthread_rwlock_wrlock(q_lock);
        if (job == q_head) {
            q_head = job->j_next;
            if (q_tail == job) {
                q_tail = NULL;
            } else {
                job->j_next->j_prev = job->j_prev;
            }
        } else if (job == q_tail) {
            q_tail = job->j_prev;
            job->j_prev->j_next = job->j_next;
        } else {
            job->j_prev->j_next = job->j_next;
            job->j_next->j_prev = job->j_prev;
        }
        pthread_rwlock_unlock(q_lock);
    }

    struct Job* find(pthread_t id) {
        struct Job *jp;

        if (pthread_rwlock_rdlock(q_lock) != 0)
            return NULL;

        for (jp = q_head; jp != NULL; jp = jp->next) {
            if (pthreda_equal(jp->j_id, id))
                break;
        }
        pthread_rwlock_unlock(q_lock);
        return jp;
    }

private:
    struct Job* q_head;
    struct Job* q_tail;
    pthread_rwlock_t q_lock;
};
```

信号量(semaphore)
----
```
一种特殊类型的unsigned int无符号整型变量，可以赋值为0,1,2,...
它与互斥量最大的区别在于信号量没有个体拥有权，主线程把所有信号量初始化为0，即“加锁”，其他线程都能调用sem_post和sem_wait函数。

信号量比互斥量功能更强的原因：
1.它们能初始化为任何非负值；
2.信号量没有“归属权”，任何线程都能够对锁上的信号量进行解锁；
```

* 操作函数
```cpp
头文件: #include <semaphore.h>
sem_t // 信号量类型
int sem_init(
    sem_t*      semaphore_p,    /* out */
    int         shared,         /* in */
    unsigned    initial_val     /* in */
);
int sem_destroy(sem_t* semaphore_p  /* in/out */);
int sem_post(sem_t* semaphore_p     /* in/out */);
int sem_wait(sem_t* semaphore_p     /* in/out */);
```

信号量实现线程间发送消息
----
```cpp
#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <semaphore.h>

void* Send_msg(void*);

const int MSG_MAX = 1024;
long thread_count;
char **message;
sem_t *semaphores;

int main(int argc, char const *argv[])
{
    if (argc != 2) {
        printf("Usage: ./a.out thread_number\n");
        exit(0);
    }
    long thread;
    thread_count = strtol(argv[1], NULL, 10);
    pthread_t* thread_handlers;
    thread_handlers = (pthread_t*)malloc(thread_count*sizeof(pthread_t));
    message = (char**)malloc(thread_count*sizeof(char*));
    semaphores = (sem_t*)malloc(thread_count*sizeof(sem_t));

    // initialize message to NULL and semaphore to 0(locked)
    for (thread = 0; thread < thread_count; thread++) {
        message[thread] = NULL;
        sem_init(&semaphores[thread], 0, 0);
    }

    // create thread
    for (thread = 0; thread < thread_count; thread++) {
        pthread_create(&thread_handlers[thread], NULL, Send_msg, (void*)thread);
    }

    // join thread
    for (thread = 0; thread < thread_count; thread++) {
        pthread_join(thread_handlers[thread], NULL);
    }

    // destroy semaphore
    for (thread = 0; thread < thread_count; thread++) {
        sem_destroy(&semaphores[thread]);
    }

    // free memory
    free(semaphores);
    for (thread = 0; thread < thread_count; thread++) {
        free(message[thread]);
    }
    free(message);
    free(thread_handlers);
    return 0;
}

void* Send_msg(void* rank) {
    long my_rank = (long)rank;
    long dest = (my_rank+1) % thread_count;
    char *my_msg = (char*)malloc(MSG_MAX*sizeof(char));

    sprintf(my_msg, "Hello to %ld from %ld", dest, my_rank);
    message[dest] = my_msg;
    sem_post(&semaphores[dest]);    // unlock semaphores of dest
    sem_wait(&semaphores[my_rank]); // wait for semaphores to be unlocked
    printf("Thread %ld > %s\n", my_rank, message[my_rank]);
    return NULL;
}
```

生产者与消费者同步
----
一个“消费者”线程在继续运行前需要等待一些条件或数据被“生产者”线程创建。

路障和条件变量
----
* 路障
```
通过保证所有线程程序中处于同一位置来同步线程，这个同步点称为路障（barrier）,只有所有线程都到达此
路障，线程才能继续运行下去，否则，会阻塞在路障。路障一个非常重要的应用就是调试程序，因为并行程序发
生错误时，很难确定具体在哪个位置出现错误。
```

* 忙等待和互斥量实现的路障
```cpp
int counter;
int thread_count;
pthread_mutex_t barrier_mutex;
...
void* Thread_work(...) {
    ...
    pthread_mutex_lock(&barrier_mutex);
    counter++;
    pthread_mutex_unlock(&barrier_mutex);
    while (counter < thread_count);
    ...
}
```
此实现方式的缺点：
```
1.线程处于忙等待循环浪费很多cpu周期
2.程序中的线程数多过于核数时，程序的性能会直线下降
3.按此方式实现路障，有多少个路障就需要设置多少个不同的共享counter变量来进行计数
```

* 信号量实现路障
```cpp
int counter;
int thread_count;
sem_t counter_semaphore;
sem_t barrier_semaphore;
...
void* Thread_work(...) {
    ...
    sem_wait(&counter_semphore);    // 线程请求counter_semaphore
    if (counter == thread_count - 1) {  // 判断是否为最后一个线程
        counter = 0;    // 重置counter计数
        sem_post(&counter_semaphore);   // 释放counter_semaphore
        for (int i = 0; i < thread_count - 1; i++) {
            sem_post(&barrier_semaphore);   // 逐一释放barrier_semaphore，使其他线程可以继续前行
        }
    } else {
        counter++;
        sem_post(&counter_semaphore);   // 线程释放counter_semaphore
        sem_wait(&barrier_semaphore);   // 线程进入阻塞
    }
    ...
}
```
此方式实现路障的优缺点
```
优：
1.线程被sem_wait阻塞时，不会消耗cpu周期，性能更加
2.counter被重置为0后可以重用
缺：
1.barrier_semaphore会导致竞争条件，不可重用
```

* 条件变量
```
条件变量是一个数据结构，允许线程在某个特定条件或事件发生前都处于挂起状态。当事件或条件发生时，
另一个线程可以通过信号来唤醒挂起的线程。一个条件变量总是和一个互斥量相关联。
```

相关函数
```cpp
pthread_cond_t // 条件变量的类型
int pthread_cond_init(
    pthread_cond_t*             cond_p,     /* out */
    const pthread_condattr_t*   cond_attr_p /* in */
);
int pthread_cond_destroy(pthread_cond_t* cond_p     /* in/out */);
int pthread_cond_signal(pthread_cond_t* cond_var_p  /* in/out */);
int pthread_cond_broadcast(pthread_cond_t* cond_var_p   /* in/out */);
int pthread_cond_wait(
    pthread_cond_t* cond_var_p,     /* in/out */
    pthread_mutex_t* mutex_p        /* in/out */
);
```

* 条件变量实现路障
```cpp
int counter;
pthread_mutex_t mutex;
pthread_cond_t cond_var;
...
void* Thread_work(...) {
    ...
    pthread_mutex_lock(&mutex);
    counter++;
    if (counter == thread_count) {
        counter = 0;
        pthread_cond_broadcast(&cond_var);
    } else {
        while (pthread_cond_wait(&cond_var, &mutex) != 0);
    }
    pthread_mutex_unlock(&mutex);
    ...
}
```
注意：上面else语句使用while循环的原因是因为有其他事件将挂起的线程解锁。


pthread自带的屏障
----
```cpp
int pthread_barrier_init(
    pthread_barrier_t* barrier,         /* out */
    const pthread_barrierattr_t* attr,  /* in */
    unsigned int count  /* in */
);
int pthread_barrier_destroy(
    pthread_barrier_t* barrier
);

int pthread_barrier_wait(
    pthread_barrier_t* barrier
);
```
pthread_barrier_wait函数给其中一个线程返回`PTHREAD_BARRIER_SERIAL_THREAD`,其他线程得到的返回值是0；
这使得一个线程可以作为主线程，它可以工作在其他所有线程已完成的工作结果上；

* example
```cpp
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <limits.h>
#include <sys/time.h>

#include <pthread.h>

#define NTHREAD 8
#define NUMBERS 10000000
#define NSIZE  NUMBERS / NTHREAD

long nums[NUMBERS];     // the array to be sorted
long snums[NUMBERS];    // the sorted array
long numscopy[NUMBERS]; // test single thread time

pthread_barrier_t b;

int compare(const void* a, const void* b) {
    long _a = *((long*)a);
    long _b = *((long*)b);
    return _a - _b;
}

void* thread_fn(void* args) {
    long idx = (long)args;
    qsort(&nums[idx], NSIZE, sizeof(long), compare);
    pthread_barrier_wait(&b);
    return NULL;
}

void merge() {
    long idx[NTHREAD];
    long i;
    for (i = 0; i < NTHREAD; i++)
        idx[i] = i*NSIZE;
    long index;
    long cur;
    long num;
    for (index = 0; index < NUMBERS; index++) {
        cur = 0;
        num = LONG_MAX;
        for (i = 0; i < NTHREAD; i++) 
            if (idx[i] < (i+1)*NSIZE && nums[idx[i]] < num) {
                num = nums[idx[i]];
                cur = i;
            }
        snums[index] = nums[idx[cur]];
        idx[cur]++;
    }
}

int main(int argc, char const *argv[])
{
    srand(time(NULL));
    struct timeval start, end;
    long long startusec, endusec;
    pthread_t tid;
    long i;
    for (i = 0; i < NUMBERS; i++) {
        nums[i] = (rand() % 99999);
        numscopy[i] = nums[i];
    }

    pthread_barrier_init(&b, NULL, NTHREAD+1);

    gettimeofday(&start, NULL);
    for (i = 0; i < NTHREAD; i++) {
        pthread_create(&tid, NULL, thread_fn, (void*)(i*NSIZE));
    }
    pthread_barrier_wait(&b);
    merge();
    gettimeofday(&end, NULL);

    // for (i = 0; i < NUMBERS; i++) {
    //     printf("%ld\n", snums[i]);
    // }
    startusec = start.tv_sec * 1000000 + start.tv_usec;
    endusec = end.tv_sec * 1000000 + end.tv_usec;
    printf("%d threads sorted took %.4f seconds\n", NTHREAD, (endusec - startusec) / 1000000.0);

    gettimeofday(&start, NULL);
    qsort(numscopy, NUMBERS, sizeof(long), compare);
    gettimeofday(&end, NULL);
    startusec = start.tv_sec * 1000000 + start.tv_usec;
    endusec = end.tv_sec * 1000000 + end.tv_usec;
    printf("single thread sorted took %.4f seconds\n", (endusec - startusec) / 1000000.0);
    return 0;
}
```

缓存、缓存一致性和为共享
----
* 缓存(Cache)
```
处理器的执行速度比访问主存中数据的速度快得多，如果处理器每次操作都从主存中读取数据，那么它将花费大量的
时间等待数据从内存中取出后再到达处理器。为解决这个问题，处理器增加相对快速的内存，称为缓存。
```

* 时间和空间局部性原理
```
如果处理器在时间t访问了内存位置x，那么很可能它在一个接近t的时间访问接近x的内存位置。
```

* 缓存行或缓存块
```
如果一个处理器需要访问主存位置x，那么就不只是将x的内容传入（出）主存，而是将一块包含x的内存传入（出）主存。
这一块内存称为缓存行或缓存块；
```

* 缓存一致性问题
```
在多核系统中，各个核的Cache存储相同的变量的副本，当一个处理器更新Cache中变量的副本时，其他处理器应该
知道该变量已更新，即其他处理器中Cache的副本也应该更新。
```

* 缓存一致性的解决
```
1.写直达（write-through）Cache中，当cpu向Cache写数据的时，高速缓存会立即写回主存中；
2.写回（write-back）Cache中，数据不是立即更新到主存中，而是将发生数据更新的高速缓存标记为脏(dirty)，
当发生缓存行替换时，标记为脏的高速缓存行被写入到主存中；
```

* 伪共享(false sharing)
```
因为缓存一致的基本单位是缓存行或缓存块，它通常比一个存储字大，所以这可能会带来负效应：两个线程可能正在访问
不同的内存单元，当两个单元属于同一缓存行时，缓存一致性硬件会看成这两个线程正在访问同一个内存单元。这样，如果
一个线程更新了它的内存单元，之后其他的线程试图读它想访问的内存单元（与前面更新的内存单元同在一个缓存行），就
不得不从主存中获取值。就是说，缓存一致性硬件强迫多个线程看起来好像是共享同一个内存单元。这称为伪共享，它会严
重降低共享内存程序的性能。
```

线程安全性
----
```
某些C语言函数通过声明static变量，从而在两次调用之间存储数据。当多个线程调用该函数时，可能引起错误，
因为线程之间共享静态存储，所以一个线程能够覆盖另一个线程的数据。这样的函数不是线程安全的。
```
