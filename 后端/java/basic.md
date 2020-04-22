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