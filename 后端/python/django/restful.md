前后端分离，前端负责数据渲染，后端负责数据转换。通过api来调用。api设计使用restful规范。


## REST 
- Representational 表象层
- State 状态
- Transfer 转移
  
全称应该是 Resource Representational State Transfer 资源在网络中以某种表现形式进行状态转移

**URL定位资源，用HTTP动词（GET,POST,DELETE,PUT）描述操作**

## 如何设计RESTful api
1. 六个原则
   1. C-S架构 数据存储在server端，Client负责渲染。定义好接口格式之后，各自开发互不干扰
   2. 无状态 http请求本身是无状态的，客户端每次请求都带有充分的信息染个服务端识别资源。
   3. 统一的接口 根据请求可以识别出资源、动作和响应信息。
   4. 一致的数据格式 统一用xml或者json
   5. 可缓存
   6. 按需编码、可定制代码  服务端可以发送一些功能让客户端执行。

2. 最佳示例
   1. 版本控制： `developer.github.com/v2`
   2. 参数命名规范  query parameter使用驼峰命名法或者下划线命名，推荐下划线 `http://example.com/api/users/today_login`
   3. rul命名规范  每个url表示一中资源，所以使用名词复数来表示，`http://example.com/api/users/1`，利用http请求实现curd,c--post, r--get, u--put, d--delete
   4. 统一返回数据格式
    ```json
    {
        "code": 200,
        "message": "success",
        "data": {
            "name": 123
        }
    }
    {
        "code": 401,
        "message": "error message",
        "data": null
    }
    ```
    5. http状态码