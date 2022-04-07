---
name: 随机数Random.md
date: 2017-03-22
update: 2017-03-22
keywords: c++ 随机数 random
---

Random随机数生成
----
下面代码演示使用c++11的random库进行随机数的生成
```c++
#include <iostream>
#include <random>
using namespace std;

int main()
{
    std::mt19937 rng;
    rng.seed(std::random_device()());
    std::uniform_int_distribution<std::mt19937::result_type> dist6(1, 6);
    std::cout << dist6(rng) << std::endl;
    
    std::uniform_real_distribution<double> distribution(-1, 1);
    std::cout << distribution(rng) << std::endl;
    return 0;
}
```

初始化随机种子
```c++
std::mt19937 rng;
rng.seed(std::random_device()());
```

创建一个均匀分布，这个均匀分布可以等概率（随机）生成[1, 6]区间的整形数字；
```c++
std::uniform_int_distribution<std::mt19937::result_type> dist6(1, 6);
```
也可以直接写成
```c++
std::uniform_int_distribution<int> dist6(1, 6);
```

创建一个均匀分布，随机（等概率）生成在（-1， 1）之间的小数；
```c++
std::uniform_real_distribution<double> distribution(-1, 1);
```

更多信息看参考链接

参考链接
----
[cplusplus random](http://www.cplusplus.com/reference/random/?kw=random)
