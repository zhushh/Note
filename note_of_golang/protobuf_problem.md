#### 问题

编译go成功，运行的时候，发现这个失败了：

```
2020/01/14 20:39:41 properties.go:482: proto: duplicate proto type registered: reader_content_comm.CategoryItem
2020/01/14 20:39:41 properties.go:482: proto: duplicate proto type registered: reader_content_comm.AuthorItem
2020/01/14 20:39:41 properties.go:482: proto: duplicate proto type registered: reader_content_comm.TagItem
2020/01/14 20:39:41 properties.go:482: proto: duplicate proto type registered: reader_content_comm.CpItem
2020/01/14 20:39:41 properties.go:482: proto: duplicate proto type registered: reader_content_comm.BookItem
2020/01/14 20:39:41 properties.go:482: proto: duplicate proto type registered: reader_content_comm.ChapItem
2020/01/14 20:39:41 properties.go:482: proto: duplicate proto type registered: reader_content_comm.Condition
2020/01/14 20:39:41 properties.go:482: proto: duplicate proto type registered: reader_content_comm.PageCommon
2020/01/14 20:39:41 properties.go:482: proto: duplicate proto type registered: reader_content_comm.DataLog
2020/01/14 20:39:41 properties.go:482: proto: duplicate proto type registered: reader_content_comm.UserInfo
panic: proto: duplicate enum registered: reader_content_comm.VType
```



#### 分析

查看protobuf源码: `github.com\golang\protobuf@v1.3.2\proto\properties.go`，有这么一段逻辑：

```go
// RegisterEnum is called from the generated code to install the enum descriptor
// maps into the global table to aid parsing text format protocol buffers.
func RegisterEnum(typeName string, unusedNameMap map[int32]string, valueMap map[string]int32) {
	if _, ok := enumValueMaps[typeName]; ok {
		panic("proto: duplicate enum registered: " + typeName)
	}
	enumValueMaps[typeName] = valueMap
}
```

注册枚举类型的时候，会判断是否已经存在这个枚举了，如果注册过，重新注册会直接panic。



原因是因为协议依赖导致的问题：

假设现在有A，B，C三个协议，他们的依赖关系是：A 依赖 C, B 依赖 C，然后在D中import A和B，那么`C.pb.go`的`init`函数会被执行两次，导致出现panic。因为pb编译出来的go文件默认有这个：

```go
func init() {
	proto.RegisterType((*CategoryItem)(nil), "reader_content_comm.CategoryItem")
	proto.RegisterType((*AuthorItem)(nil), "reader_content_comm.AuthorItem")
	proto.RegisterType((*TagItem)(nil), "reader_content_comm.TagItem")
	proto.RegisterType((*CpItem)(nil), "reader_content_comm.CpItem")
	proto.RegisterType((*BookItem)(nil), "reader_content_comm.BookItem")
	proto.RegisterType((*ChapItem)(nil), "reader_content_comm.ChapItem")
	proto.RegisterType((*Condition)(nil), "reader_content_comm.Condition")
	proto.RegisterType((*PageCommon)(nil), "reader_content_comm.PageCommon")
	proto.RegisterType((*DataLog)(nil), "reader_content_comm.DataLog")
	proto.RegisterType((*UserInfo)(nil), "reader_content_comm.UserInfo")
	proto.RegisterEnum("reader_content_comm.VType", VType_name, VType_value)
}
```





#### 参考