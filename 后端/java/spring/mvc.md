ssm: spring+springMVC+mybatis
mvc: model+view+controller
mvc是一种架构模式，作用是降低视图和业务逻辑间的双向耦合

# 记录
## 导入依赖
```xml
<dependency>
    <groupId>org.springframework</groupId>
    <artifactId>spring-webmvc</artifactId>
    <version>5.1.9.RELEASE</version>
</dependency>
<dependency>
    <groupId>javax.servlet</groupId>
    <artifactId>servlet-api</artifactId>
    <version>2.5</version>
</dependency>
<dependency>
    <groupId>javax.servlet.jsp</groupId>
    <artifactId>jsp-api</artifactId>
    <version>2.2</version>
</dependency>
<dependency>
    <groupId>javax.servlet</groupId>
    <artifactId>jstl</artifactId>
    <version>1.2</version>
</dependency>
```
1. 创建maven项目，右键 AddFrameworksSupport,添加web支持，会自动创建web目录并添加WEB-INF文件夹和web.xml配置文件
2. 配置web.xml，需要声明一个servlet, 并配置servlet-mapping，设置路由情况，由哪个servlet接收处理

```xml
<servlet>
    <servlet-name>springmvc</servlet-name>
    <!-- 这个是固定的，需要这个中心控制器来调度，由spring框架实现的servlet -->
    <servlet-class>org.springframework.web.servlet.DispatcherServlet</servlet-class>

    <init-param>
        <param-name>contextConfigLocation</param-name>
        <!-- 加载子项目的配置文件,也就是子路由的处理情况，是spring配置文件 -->
        <param-value>classpath:springmcv-servlet.xml</param-value>
    </init-param>
    <load-on-startup>1</load-on-startup>
</servlet>
<servlet-mapping>
    <servlet-name>springmvc</servlet-name>
    <url-pattern>/</url-pattern>
</servlet-mapping>
```
3. 配置spring配置文件 这里可以使用IDEA的右键添加xml-> springxml
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!-- 添加支持，这里写了支持aop,mvc -->
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xmlns:context="http://www.springframework.org/schema/context"
       xmlns:mvc="http://www.springframework.org/schema/mvc"
       xsi:schemaLocation="http://www.springframework.org/schema/beans
       http://www.springframework.org/schema/beans/spring-beans.xsd
       http://www.springframework.org/schema/context
       https://www.springframework.org/schema/context/spring-context.xsd
       http://www.springframework.org/schema/mvc
       https://www.springframework.org/schema/mvc/spring-mvc.xsd">
</beans>
```
4. 添加具体配置，根据选择类型不同配置也不同，


编写controller时有几种方式：


1. 继承Controller,重写handleRequest方法，并返回ModelAndView，
 ```java
 import org.springframework.web.servlet.ModelAndView;
 import org.springframework.web.servlet.mvc.Controller;

 import javax.servlet.http.HttpServletRequest;
 import javax.servlet.http.HttpServletResponse;
 public class ControllerTest1 implements Controller {
     @Override
     public ModelAndView handleRequest(HttpServletRequest httpServletRequest, HttpServletResponse httpServletResponse) throws Exception {
         ModelAndView mv = new ModelAndView();
         mv.addObject("msg", "Test 1 controller");
         mv.setViewName("test");
         return mv;
     }
 }
 ```

编写test.jsp文件，配置spring
```xml
<bean class="org.springframework.web.servlet.view.InternalResourceViewResolver" id="InternalResourceViewResolver"> 
<!-- 视图解析器，可以接收到ModelAndView -->
    <property name="suffix" value=".jsp"/>
    <property name="prefix" value="/WEB-INF/jsp/"/>
    <!-- view会在这个目录下查找，后缀是jsp的文件 -->
</bean>
<!-- 注册controller, 使用的路由就是 /t1 -->
<bean name="/t1" class="com.chen.controller.ControllerTest1"/>
```
2. 使用注解`@Controller`
```xml
<!-- 自动扫描指定包，所有的注解类让Ioc容器管理 -->
<context:component-scan base-package="com.chen.controller">
```
```java
@Controller
public class ControllerTest2 {
    @RequestMapping("/t2")
    public String index(Model model){
        model.addAttribute("msg", "ControllerTest2");
        return "test";
    }
}
```
获取路径上的传参
```java
@Controller
public class RestFulController {
    @RequestMapping("/commit/{p1}/{p2}")
    public String index(value = "/commit/{p1}/{p2}", method = {RequestMethod.GET}){
        int result = p1 + p2;
        model.addAttribute("msg", "result: " + result);
        return "test";
    }
}
```

**转发和重定向**
1. 使用servletAPI进行转发和重定向，HttpServletRequest.sendRedirect()进行重定向，HttpServletRequest.getRequestDispatcher.forward()进行转发

```java
@Controller
public class ResultGo {
    @RequestMapping("/result/t1")
    public void test1(HttpServletRequest req, HttpServletResponse rsp) throws IOException{
        rsp.getWriter().println("Hello, Spring by servlet api"); // 直接返回一个字符串，显示页面上
    }
    @RequestMapping("/result/t2")
    public void test2(HttpServletRequest req, HttpServletResponse rsp) throws IOException{
        rsp.sendRedirect("/index.jsp"); // 重定向到index.jsp，url会变化
    }
    @RequestMapping("/result/t3")
    public void test3(HttpServletRequest req, HttpServletResponse rsp) throws Exception {
        req.setAttribute("msg", "/result/t3");
        req.getRequestDispatcher("/WEB-INF/jsp/test.jsp").forward(req, rsp); // 转发到test.jsp带参数。 这个路径不会变化
    }
}
```
2. ModelAndView
```java
public class ControllerTest1 implements Controller {

   public ModelAndView handleRequest(HttpServletRequest httpServletRequest, HttpServletResponse httpServletResponse) throws Exception {
       //返回一个模型视图对象
       ModelAndView mv = new ModelAndView();
       mv.addObject("msg","ControllerTest1");
       mv.setViewName("test");
       //这里是转发， url不会变化
       return mv;
  }
}
```
3. SpringMVC

```java
@Controller
public class ResultSpringMVC {
    // 不用视图解析器，
    @RequestMapping("/rsm/t1")
    public String test1(){
        // 转发
        return "/index.jsp";
    }
    @RequestMapping("/rsm/t2")
    public String test2(){
        // 转发
        return "forward:/index.jsp";
    }
    @RequestMapping("/rsm/t3")
    public String test3(){
        // 重定向
        return "redirect:/index.jsp";
    }
}
```
```java
@Controller
public class ResultSpringMVC2 {
    // 使用视图解析器
   @RequestMapping("/rsm2/t1")
   public String test1(){
       //转发
       return "test";
  }

   @RequestMapping("/rsm2/t2")
   public String test2(){
       //重定向
       return "redirect:/index.jsp";
  }
}
```
**提交数据**
1. 直接在函数的参数列表处声明，参数名与url上参数名一直即可接收
2. 如果不一致，可以使用`@RequestParam()`进行映射
3. 直接使用对象接收，提交的参数名与对象的字段名相同即可
**返回数据**
1. 通过ModelAndView, 使用addObject, setViewName(继承Controller)
2. 通过ModelMap, 使用addAttribute(使用注解)，返回viewName字符串即可
3. 通过model,使用addAttribute(),用法同modelMap

**乱码**
在web.xml中添加过滤器
```xml
<filter>
   <filter-name>encoding</filter-name>
   <filter-class>org.springframework.web.filter.CharacterEncodingFilter</filter-class>
   <init-param>
       <param-name>encoding</param-name>
       <param-value>utf-8</param-value>
   </init-param>
</filter>
<filter-mapping>
   <filter-name>encoding</filter-name>
   <url-pattern>/*</url-pattern>
</filter-mapping>
```

## json
1. 使用jackson
   ```xml
    <dependency>
        <groupId>com.fasterxml.jackson.core</groupId>
        <artifactId>jackson-databind</artifactId>
        <version>2.12.0-rc1</version>
    </dependency>
   ```
   ```java
   @Controller
    public class UserController {
        @RequestMapping(value = "/json1", produces = "application/json;charset=utf-8")
        @ResponseBody
        public String json1() throws JsonProcessingException {
            ObjectMapper mapper = new ObjectMapper();
            User user = new User("取为啊是", 1, "男");
            return mapper.writeValueAsString(user);
        }
    }
   ```
   ```xml
   <!-- 统一设置为utf-8为jackson -->
   <mvc:annotation-driven>
        <mvc:message-converters register-defaults="true">
            <bean class="org.springframework.http.converter.StringHttpMessageConverter">
                <constructor-arg value="UTF-8"/>
            </bean>
            <bean class="org.springframework.http.converter.json.MappingJackson2HttpMessageConverter">
                <property name="objectMapper">
                    <bean class="org.springframework.http.converter.json.Jackson2ObjectMapperFactoryBean">
                        <property name="failOnEmptyBeans" value="false"/>
                    </bean>
                </property>
            </bean>
        </mvc:message-converters>
    </mvc:annotation-driven>
   ```
   格式化时间
   ```java
    @RequestMapping("/json2")
    @ResponseBody
    public String json2() throws JsonProcessingException {
        ObjectMapper mapper = new ObjectMapper();
        mapper.configure(SerializationFeature.WRITE_DATE_KEYS_AS_TIMESTAMPS, false);
        SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
        mapper.setDateFormat(sdf);
        return mapper.writeValueAsString(new Date());
    }
   ```
2. 使用fastJson
