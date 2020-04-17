## js
### 基础
1. string, 
   - length
   - string[0]
   - string.indexOf('substring')
   - string.slice()
   - toLowerCase(), toUpperCase()
   - replace()
   - split() 分割成数组
2. 数组
   - join() 拼接字符串
   - push() pop() 对数组尾部进行操作
   - unshift() shift() 对数组头部进行操作
3. 事件
   - 捕获和冒泡, 当一个事件发生在具有父元素的元素上,现代浏览器运行两个不同的阶段 - 捕获阶段和冒泡阶段。 在现代浏览器中，默认情况下，所有事件处理程序都在冒泡阶段进行注册
        1. 捕获： 从顶向下运行， 从Html检查到最后，哪个触发了就运行哪个
        2. 冒泡，从底向上， 先运行最低层的，在检查父元素，直到Html
        3. 阻止冒泡，event.stopPropagation()
   - 事件委托，字节点的事件委托给父节点， 比如，li的事件委托给ul
4. 对象
   - 原型

  ```javascript
  function Person(){};  // 构造函数
  Person.prototype      // 属性，指向Object
  var person1 = new Person();

  person1.__proto__     // 继承原型链， 每次继承不会复制属性，是通过原型链来查找属性和方法

  ```
    - json   json字符串转对象  myObj = JSON.parse(myStr)  对象转字符串 myStr = JSON.stringify(myObj)
### 异步
1. 老派 callbacks
2. 新派 promise
   - 创建promise时，它既不是成功也不是失败状态。这个状态叫作pending（待定）。
   - 当promise返回时，称为 resolved（已解决）.
   - 一个成功resolved的promise称为fullfilled（实现）。它返回一个值，可以通过将.then()块链接到promise链的末尾来访问该值。 .then()块中的执行程序函数将包含promise的返回值。
   - 一个不成功resolved的promise被称为rejected（拒绝）了。它返回一个原因（reason），一条错误消息，说明为什么拒绝promise。可以通过将.catch()块链接到promise链的末尾来访问此原因。

3. setTimeout(callback, timeout, parm) 在指定事件后执行， 毫秒为单位, parm传递给callback, clearTimeout,清除超时
4. setInterval()  以固定的时间间隔重复运行一段代码， clearInterval,清除
   