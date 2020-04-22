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
2. 获取数据
   1. Ajax
      - 就是使用 XMLHttpRequest 对象与服务器通信。 

      ```js
      httpRequest = new XMLHttpRequest();
      httpRequest.open('POST', 'http://www.example.org/', true);
      httpRequest.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
      httpRequest.send(data);
      httpRequest.onreadystatechange = nameOfTheFunction;
      function nameOfTheFunction(){
         if (httpRequest.readyState === XMLHttpRequest.DONE){
            if (httpRequest.status === 200){
               alert(httpRequest.responseText);
            }
         }
      }
      ```
   2. Fetch
      ```js
      fetch(url, {
         body: JSON.stringify(data),
         cache: 'no-cache',
         credentials: 'same-origin',
         headers: {
            'user-agent': 'Mozilla/4.0 MDN Example',
            'content-type': 'application/json'
         },
         method: 'POST',
         mode: 'cors',
         redirect: 'follow',
         referrer: 'no-referrer',
      }).then(response=>response.json())
      .then(data => console.log(data))
      .catch(error=>console.error(error))
      ```
      - credentials 凭据  
        - 发送跨域源  credentials: 'include'
        - URL与调用脚本位于同一起源， credentials: 'same-origin'
        - 不包含凭据， credentials: 'omit
      - 检测成功 网络故障promise会在reject带上TypeError, 判断response.ok
         ```js
         fetch('flowers.jpg').then(function(response) {
         if(response.ok) {
            return response.blob();
         }
         throw new Error('Network response was not ok.');
         }).then(function(myBlob) { 
            var objectURL = URL.createObjectURL(myBlob); 
            myImage.src = objectURL; 
         }).catch(function(error) {
            console.log('There has been a problem with your fetch operation: ', error.message);
         });
         ```
      - header 
         ```js
         var myHeaders = new Headers();
         myHeaders.append('Content-Type', 'text/plain');

         myHeaders = new Headers({
            'Content-Type': "text/plain",
         });
         ```
      - Response
         - Response.status 状态码
         - Response.statusText 字符串
         - Response.ok

   3. Promise
      - new Promise( function(resolve, reject) {...} /* executor */  );
      - 1 pending: 初始状态，既不是成功，也不是失败状态。 2 fulfilled: 意味着操作成功完成。 3 rejected: 意味着操作失败。
      ![avator](images/promises.png)


### HTTP
1. MIME类型 
   - text/plain text/html text/css text/javascript
   - image/gif image/png
   - multipart/form-data 表单
   - application/json json格式
2. 管理连接（http/1)
   - 短连接  每个http请求都会有一次TCPwo握手。古老而耗时的，现在默认不使用（Connection=close时使用）。
   - 长链接  keep-alive，一个长连接保持一段时间，重复发送一系列的请求，节省了TCP握手的时间。 缺点是在空闲时间也会耗费服务器资源。
   - HTTP流水线 HTTP请求是按顺序发出的。下一个请求只有在当前请求收到应答过后才会被发出。 默认不使用。
3. 安全
   - CSP 内容安全策略 白名单制度 网络服务器返回  Content-Security-Policy  HTTP头部
   - X-Content-Type-Options 响应首部相当于一个提示标志，被服务器用来提示客户端一定要遵循在 Content-Type 首部中对  MIME 类型 的设定，而不能对其进行修改。
4. CORS HTTP访问控制，跨域资源共享,服务器进行配置，nginx或者django进行配置，返回体的头部添加信息 Access-Control-Allow-Origin: xxx;
5. Authentication 认证
6. caching 缓存 Cache-Control
7. Cookies 服务器发送到用户浏览器并保存在本地的一小块数据，它会在浏览器下次向统一服务器再次发送请求时被携带。
   - 创建cookie, 服务器在响应头里添加 ```Set-Cookie: <cookie名>=<cookie值>```
   - 会话期cookie, 浏览器关闭之后会自动删除
   - 持久性cookie， 需要指定 Expires,Max-Age
   - Secure 标记为 Secure 的Cookie只应通过被HTTPS协议加密过的请求发送给服务端。
   - HttpOnly 设置为HttpOnly的cookie不能通过js的Document.cookie获取，只能发送给服务器
   - cookie的作用域， Domain指定了哪些主机可以接受，默认为当前主机。Path制定了哪些路径可以接受cookie
   - SameSite 允许服务器要求某个cookie在跨站请求时不会被发送，从而可以阻止跨站请求伪造攻击（CSRF）。
### 客户端存储
1. cookie cookie的唯一优势是它们得到了非常旧的浏览器的支持，所以如果您的项目需要支持已经过时的浏览器（比如 Internet Explorer 8 或更早的浏览器），cookie可能仍然有用，但是对于大多数项目（很明显不包括本站）来说，您不需要再使用它们了。其实cookie也没什么好说的，document.cookie一把梭就完事了。
2. web Storage 存储简单的 键名/键值 对数据 (限制为字符串、数字等类型) 并在需要的时候检索其值。
   - 数据包含在浏览器的两个类似对象的结构 sessionStorage和localStorage
   ```js
   localStorage.setItem('name', 'xxx');
   localStorage.getItem('name');
   localStorage.removeItem('name');
   ```
   - localStorage数据会持久化，关闭打开依然存在。
3. IndexedDB 可以在浏览器中访问的一个完整的数据库系统