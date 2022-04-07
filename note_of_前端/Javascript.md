#### Vue引入Json-viewer美化显示插件

https://www.npmjs.com/package/vue-json-viewer



#### 数组处理

```js
var arr = [1, 2, 3, 4, 5]

var newArr = arr.slice(1);	// newArr: [2, 3, 4, 5]
var newArr = arr.slice(0, 3);	// newArr: [1, 2, 3]

var joinStr = arr.join('-');	// joinStr: '1-2-3-4-5'
var rarr = arr.reverse();	// rarr: [5, 4, 3, 2, 1]

var array = [5, 2, 1, 4, 3];
var sarr = array.sort();		// sarr: [1, 2, 3, 4, 5]
var sarr = array.sort(function(a, b){ reutrn b - a}) // sarr: [5, 4, 3, 2, 1]
```



#### 读取文件

```js
function GetContent(filename) {
    var content = ''
    if (window.FileReader) {
        var reader = new FileReader();
        reader.onloadend = function(evt) {
            if (evt.target.readyState == FileReader.DONE) {
                content = evt.target.result
                console.log(evt.target.result)
            }
        }
    }
    return content
}
```



#### Object转Json

```js
function toJson(obj) {
    return JSON.stringify(obj);
}

function toJsonPetty(obj) {
    return JSON.stringify(obj, null, 2);
}

var myObj = {
    "name": 'nick',
    "age": 20,
    "company": 'tencent'
}
var formatStr = toJson(myObj)
var pettyStr = toJsonPetty(myObj)

console.log(formatStr)
console.log(pettyStr)
```

https://www.cnblogs.com/anychem/archive/2012/04/02/2429785.html



#### 参考

https://developer.mozilla.org/zh-CN/docs/Web/JavaScript

