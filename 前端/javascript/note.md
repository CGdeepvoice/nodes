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
   - Promise.all([]).then() promise数组全部执行完成才进行下一步，将数组中的全部结果作为参数传给then。
   - myPromise.then().catch().finally();

3. setTimeout(callback, timeout, parm) 在指定事件后执行， 毫秒为单位, parm传递给callback, clearTimeout,清除超时
4. setInterval()  以固定的时间间隔重复运行一段代码， clearInterval,清除
5. 箭头函数（）=> x 是（）=> {return x;} 的简写
6. async/await
   - 调用async会返回一个promise。它将任何函数转换为promise。
   - await 可以放在任何基于异步声明的函数之前，暂停代码在该行上，直到promise完成，然后返回结果值await只能在异步函数内部工作。


### API
1. 操作文档
   1. 浏览器组成部分
      - window是载入浏览器的标签，在JavaScript中用Window对象来表示，使用这个对象的可用方法，你可以返回窗口的大小等等。
      - navigator web的状态和标识（代理）。在JavaScript中，用Navigator来表示。你可以用这个对象获取一些信息，比如来自用户摄像头的地理信息、用户偏爱的语言、多媒体流等等。
      - document DOM表示载入窗口的实际页面。
   2. 选择元素
      - Document.querySelecotr() 推荐
      - Document.getElementById()
      - Document.getElementsByTagName() 
   3. 创建放置新节点
      
      ```js
      var sect = document.querySelector('section');
      var para = document.createElement('p');
      para.textContent = 'we hope you enjoyed the ride.'
      sect.appendChild(para);
      ```
   4. 移动和删除
      - 移动： sect.appendChild(linkPara), linkPara是唯一引用，这样可以移动到最后。
      - 删除： 从父节点删除该节点 sect.removeChild(linkPara). 从自己删除自己 linkPara.parentNode.removeChild(linkPara).
   5. 操作样式
      - para.style.color = 'red';
      - ```<style>.highlight {color: white} </style>```   para.setAttribute('class', 'highlight');