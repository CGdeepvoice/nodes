## TOMCAT
1. TOMCAT是服务器软件，用于接收请求，处理请求和做出相应的。可以部署web项目
2. 安装和启动
    - http://tomcat.apache.org/ 官网下载，解压缩放到Library目录下即可
    - sudo sh bin/startup.sh 启动，默认8080端口
    - sudo sh bin/shutdown.sh 关闭
## servlet: server applet
服务端小程序。
* Servlet就是一个接口，定义了Java类被浏览器访问到（tomcat识别）的规则。
* 自定义类来实现Servlet接口，复写方法。

1. 配置web.xml： url路径

```xml
<servlet>
    <servlet-name>demo1</servlet-name>
    <servlet-class>day1.web.simple</servlet-class>
</servlet>

<servlet-mapping>
    <servlet-name>demo1</servlet-name>
    <url-pattern>/demo1</url-pattern>
</servlet-mapping>
```
2. 声明周期：
    - 创建：init(),只执行一次。单例
    - 提供服务： service()，每次访问都调用
    - 销毁：destroy,只执行一次：
        * Servlet被销毁时执行。服务器关闭时，Servlet被销毁
		* 只有服务器正常关闭时，才会执行destroy方法。
		* destroy方法在Servlet被销毁之前执行，一般用于释放资源
2. Servlet体系结构
   - servlet 接口
   - GenericServlet 抽象类, 实现了servlet接口，对除了service方法外的方法做了默认空实现，只将serverce()方法作为了抽象方法。
   - HttpServlet 抽象类，继承自GenericServlet抽象类，实现了对Http协议的封装，简化了操作。doGet/doPost

## Request:
request和response对象是由服务器进行创建的，我们只是使用。其中request是用来获取请求消息，response对象是来设置响应消息。
### 继承体系 ：
    * ServletRequest  接口
    * HttpServletRequest  继承自ServletRequest的接口
    * org.apache.catalina.connector.RequestFacade 类(tomcat)
### 功能
1. 获取请求消息数据
   1. 获取请求行数据
        * GET /day1/demo1?name=zhangsan HTTP/1.1
        * 方法：
            1. 获取请求方式 get   `String getMethod()`
            2. 获取虚拟目录： /day1   `String getContextPath()`
            3. 获取Servlet路径 /demo1  `String getServletPath()`
            4. 获取get方式请求参数： name=zhangsan `String getQueryString()`
            5. 获取请求URI /day1/demo1  `String getRequestURI() => /day1/demo`  `StringBuffer getRequestURL() => http://localhost/day1/demo1`
    2. 获取请求头数据
        * `String getHeader(String name)` 通过请求头的名称获取请求头的值
        * `Enumeration<String> getHeaderNames()` 获取所有的请求头名称
    3. 获取请求体数据
        * 请求体只有POST方式请求才有请求体
        * 步骤： 先获取流对象，再从流对象中拿数据。 `BufferedReader getReader()` 获取字符输入流 `ServletInputStream getInputStream()`获取字节输入流。
2. 请求转发：一种在服务器内部的资源跳转方式
    1. 步骤：
        * 通过request对象获取请求转发器对象：RequestDispatcher getRequestDispatcher(String path)
        * 使用RequestDispatcher对象来进行转发：forward(ServletRequest request, ServletResponse response) 
    2. 特点：
        *  浏览器地址栏路径不发生变化
		*  只能转发到当前服务器内部资源中。
		*  转发是一次请求
    3. 共享数据：
        * 域对象：一个有作用范围的对象，可以在范围内共享数据
        * request域：代表一次请求的范围，一般用于请求转发的多个资源中共享数据
        * 方法：
       	1. void setAttribute(String name,Object obj):存储数据
       	2. Object getAttitude(String name):通过键获取值
       	3. void removeAttribute(String name):通过键移除键值对
    4. 获取ServletContext: `ServletContext getServletContext()`

