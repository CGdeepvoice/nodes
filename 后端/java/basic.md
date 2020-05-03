## java基础
### 命名规则
   - 类名: 大驼峰， 每个单词首字母大写
   - 方法名: 小驼峰， 首字母小写，后面每个单词首字母大写
   - 变量名: 全部小写
### 常量
在Java程序中固定不变的数据
### 变量
1. 基本数据类型

数据类型|关键字|内存占用|范围
:-: | :-: | :-: | :-:
字节型 | byte | 1个字节| -128~127
短整型 | short | 2个字节 | -2^15 ~ 2^15-1 (-32768 ~ 32767)
整型 | int | 4个字节| -2^31 ~ 2^31-1
长整型 | long | 8个字节|
单精度浮点数| float | 4个字节|
双精度浮点数 | double | 8个字节|
字符型| char | 2个字节|
布尔类型 | boolean| 1个字节|

2. 类型转换
   - 自动转换: 将取值范围小的类型自动提升为取值范围大的类型
   - 强制转换: 将取值范围大的类型强制转换成取值范围小的类型 格式: 数据类型 变量名 = （数据类型） 被转数据值
   - ASCII码表
### 数组
1. 定义
   - int[] arr = new int[3];
   - int[] arr = new int[]{1, 2, 3, 4};
   - int[] arr = {1, 2, 3, 4};
2. java内存划分
  
区域名称 | 作用
:-: | :-:
寄存器| cpu使用
本地方法栈| jvm在使用操作系统功能时候使用
方法区| 存储可以运行的class文件
堆内存| 存储对象或者数组，new来创建的，都存储在堆内存
方法栈|方法运行时使用的内存，比如main方法运行。

![avator](images/内存占用.png)

#### IDEA
1. project -> module -> package -> javaClass
2. psvm  == public static void main(String[] args){} 
3. 5.fori == for (int i = 0; i < 5; i++){}
4. array.fori  for(int i=0; i < array.length; i++){}
5. alt + enter 导入包，自动修正代码
6. Ctrl+Alt+L 格式化代码
7. ctrl+N 自动化生成getter、setter以及constructor 

#### 面向对象
1. 类与对象的内存占用
![avator](images/对象内存图.png)

成员变量有默认值，局部变量没有默认值。
2. JavaBean 编写类的一种标准规范。
   ```java
    public class ClassName{ //成员变量
   //构造方法 //无参构造方法【必须】 //有参构造方法【建议】 //成员方法
   //getXxx()
   //setXxx()
   }
   ```
#### 常用API
1. Scanner 获取输入项
   ```java
   import java.util.Scanner;
   public class TestScanner(){
      public static void main(String[] args){
         Scanner sc = new Scanner(System.in);
         int x = sc.nextInt();

         new Scanner(System.in).nextInt(); // 匿名对象
      }
   }
   ```
2. Random 随机数
   ```java
   import java.util.Random;
   public class TestRandom{
      public static void main(String[] args){
         Random r = new Random(); // 创建一个随机数生成器
         int x = r.nextInt(100); //获取一个0-100的随机数，其中不包括100
      }
   }
   ```
3. ArrayList 大小可变的数组， 存储在内的数据为元素。
   - 构造方法 ArrayList<String> list = new ArrayLiat<>();
   - 添加  public boolean add(E e)
   - 删除  public E remove(int index)
   - 获取  public E get(int index)
   - 元素数量 public int size()
4. String string对象不可变，每次修改都会赋值新的地址
   - 比较 s1.equals(s2);   忽略大小写比较 s1.equalsIgnoreCase(s2);
   - s.length() 获取长度
   - s.concat(s2) 连接
   - s.charAt(1) 获取索引位置的值
   - s.indexOf("ol") 第一次出现的索引位置，找不到为-1
   - s.substring(int beginIndex, int endIndex) 返回子串, 左闭右开
   - s.toCharArray()  转为字符数组
   - s.getBytes()  返回字节数组
   - s.replace(CharSequence target, CharSequence replacement)
   - s.spilit(String regex) 分割字符串，返回字符串数组

5. static 用来修饰的成员变量和成员方法，被修饰的成员是属于类的，而不是单单是属 于某个对象的。也就是说，既然属于类，就可以不靠创建对象来调用了。
   1. 类变量 static int numberId; 所有对象共享同一个类变量的值，这个值保存在类的空间中，不在对象里
   2. 静态方法 格式： ```修饰词 static 返回值类型 方法名 （参数列表）{}```,调用直接从类调用。
   3. 静态代码块  定义在成员位置，使用static修饰的代码块{ }。随着类的加载而执行且执行一次，优先于main方法和构造方法的执行。
   
   ```java
   public class Game{
      public static int num;
      public static ArrayList<String>  list;
      static{
         number = 2;
         list = new ArrayList<String>();
         list.add("222");
      }
   }
   ```

   ![avator](images/静态原理图解.jpg)

#### 继承
1. 继承
   1. 格式 extends
   2. 成员方法: 
      - 不重名没有影响
      - 重名 方法重写，使用@override,使用super. 来调用父类的方法
   3. 构造方法
      - super() 调用父类
   4. super & this
      - super: 代表父类的存储空间标识， super() 表示父类的构造方法
      - this: 代表当前的对象的引用， this() 表示本类的构造方法
   5. 特点：只支持单继承， 不支持多继承，顶层的父类是Object类
2. 抽象类
   1. 没有方法主体的方法称为抽象方法，包含抽象方法的类是抽象类
   2. 格式 ```修饰词 abstract 返回值类型 方法名(参数列表)```
   3. 抽象类的子类必须重写父类所有的抽象方法，否则，该子类也要声明为抽象类

#### 接口
1. 引用类型(数组，类和接口)， 方法的集合。 不能创建对象，可以被实现implements,实现的子类必须实现接口中所有的抽象方法，否则它必须是一个抽象类
2. 格式 
   ```java
   public interface 接口名称{
      // 抽象方法
      // 默认方法
      // 静态方法 
      // 私有方法
   }
   ```
   - 抽象方法 public abstract void method(); 没有方法体
   - 默认方法 public default void method(){}; 供子类调用或者子类重写
   - 静态方法 public static void method(){}; 供接口直接调用
   - 私有方法 private void method(){}; 供接口中的默认方法调用
   - 私有静态方法 private static void method(){}; 供接口中的静态方法和默认方法调用

#### 多态
1. 同一行为，具有多个不同表现形式
2. 格式 父类类型 变量名 = new 子类对象; 变量名.方法名();
   使用多态方式调用方法时， 首先检查父类是否有，如果没有则编译错误。如果有执行子类重写的方法
3. 引用类型转换
   1. 向上转型： 多态本身是子类类型向父类类型向上转换的过程，这个过程是默认的。
   ```java
   Animal a = new Cat();
   ```
   2. 向下转型： 父类类型向子类类型向下转换的过程，这个过程是强制的。
   ```java
   Cat c = (Cat) a;
   ```
4. instanceof 类型校验， 
   ```java
   // 变量名 instanceof 数据类型
   if (a instanceof Cat){
      Cat c = (Cat)a;
   } else {
      Dog d = (Dog)a;
   }
   ```
#### final 权限 内部类 引用类型
1. final 不可改变
   1. 类: 被修饰的类，不能被继承
   2. 方法: 被修饰的方法，不能被重写
   3. 变量: 被修饰的变量，不能被重新赋值
2. 权限修饰符
   1. public(全部可见) protected(子类可见) default(空)(包内可见) private(本类可见)
   2. 常用方式:
      - 成员变量使用private
      - 构造方法使用public
      - 成员方法使用Public
3. 内部类 定义在类内部的类，则称为内部类
   1. 成员内部类。定义在类中方法外。
      ```java
      class 外部类{
         class 内部类{}
      }
      // 内部类可以直接访问外部类的成员，包括私有成员
      // 外部类想要访问内部类的成员，必须建立内部类的对象
      // 格式: 外部类名.内部类名 对象名 = new 外部类型().new 内部类型()
      ```
   2. 匿名内部类: 内部类的简化写法。本质是一个带具体实现的父类或者父接口的匿名的子类对象
   ```java
   new 父类名或者接口名() {
      // 方法重写
      @Override
      public void method(){}
   }
   ```
4. 引用类型用法总结
   1. class 作为成员变量
   2. interface 作为成员变量
   3. interface作为方法参数和返回值类型
   4. 