### 检查文件编码程序

```c++
#include <iostream>
#include <fstream>
using namespace std;

int main()
{
  ifstream fin("./test_file.csv", ios::binary);
  unsigned char s2;
  fin.read((char *)&s2, sizeof(s2)); //读取第一个字节，然后左移8位
  int p = s2 << 8;
  fin.read((char *)&s2, sizeof(s2)); //读取第二个字节
  p += s2;

  string code;

  switch (p) //判断文本前两个字节
  {
  case 0xfffe: //65534
    code = "Unicode";
    break;
  case 0xfeff: //65279
    code = "Unicode big endian";
    break;
  case 0xe6a2: //59042
    code = "UTF-8";
    break;
  default:
    code = "ANSI";
  }
  fin.close();

  cout << code << endl;
  return 0;
}
```
