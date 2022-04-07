# -*- coding: UTF-8 -*-
import chardet
str = b"\323\340\266\356\262\273\327\343\243\254\307\353\263\344\326\265\272\363\274\314\320\370\262\331\327\367"
#判断当前字符串的格式（编码类型）
fencoding = chardet.detect(str)  

print(fencoding)
#编码类型为打印出来的fencoding编码类型
str1 = str.decode('GB2312')
print(str1)


str2 = str.decode(fencoding['encoding'])
print(str2)
