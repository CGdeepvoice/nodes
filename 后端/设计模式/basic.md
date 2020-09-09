# 面向对象设计六大原则
1. 单一职责原则

    一个类，应该仅有一个引起他变化的原因。如果一个类承担的责任过多，就等于把这些职责耦合在了一起。一个职责的变化可能会削弱或者抑制这个类完成其他职责的能力。

2. 开放-封闭原则

    对扩展是开放的，对更改是封闭的。即软件实体尽量在不修改原有代码的情况下进行扩展。

3.  里氏代换原则 子类型必须能够替换掉他们的父类型。一个软件系统中使用一个类的地方都可以替换成他的子类，系统仍能够正常工作。 面向接口编程。
   
4. 依赖倒转原则

    高层模块不应该依赖底层模块，都应该依赖抽象。
    抽象不应该依赖细节。细节应该依赖抽象。
    也就是面向接口，函数参数能用接口就用接口

5. 接口隔离原理
   使用多个专门的接口，而不是使用单一的总接口，即客户端不应该依赖那些它不需要的接口。不要在一个接口里放太多的方法，实现类可能不会全部需要，放到多个接口里，实现类可以实现多个接口。

6. 迪米特法则LoD,最少知识法则。
    一个软件实体尽可能少的与其他实体发生相互作用。
    如果两个类不必彼此直接通信，那么这两个类不应发生直接的相互作用。如果其中一个类需要调用另一个类的某一个方法时，可以通过第三者转发这个调用。

# 创建型模式
对类的实例化过程进行抽象，将软件模块中对象的创建和对象的使用分离。为了使软件结构更清晰，外界只需要直到共同的接口，不需要清楚具体的细节，使整个系统的设计更加符合单一职责原理。
## 工厂模式
1. 优点
   * 使代码结构清晰， 有效的封装变化。
   * 对调用者屏蔽具体的产品类。调用者只关系产品的接口即可。
   * 降低耦合度。
2. 适用场景
   * 作为创建型模式，复杂对象适合适用，简单对象只需要new就可以完成创建的对象不适用
   * 作为解耦模式，加入调用者自己组装产品需要增加依赖关系时，可以考虑工厂模式。
   * 系统需要较好的扩展性时，需要考虑工厂模式

### 简单工厂
提供一个创建对象实例的功能，而无需关心其具体实现。
例如创建一个计算器。
```java
// 首先创建操作的基类，并继承为加减乘除
public abstract class Operation{
    private double value1 = 0;
    private double value2 = 0;
    protected abstract double getResult();
}
// 如果只定义了这些操作，客户端每次调用需要创建不同操作符
// 所以创建简单工厂
public class OperationFactory{
    public static Operation createOperation(String operation){
        Operation oper = null;
        switch(operation){
            case "add":
                oper = new OperationAdd();
                break;
            ...
            default:
                throw new UnsupportedOperationException("不支持");
        }
        return oper;
    }
}
// 现在客户端只需要调用简单工厂就可以获取操作实例
// 这里有一个缺点，如果需要扩展操作符，还需要加case情况，不符合对改变封闭，对新增开放的原则
```
### 工厂模式
定义一个创建对象的接口，但是让实现这个接口的类来决定实例化哪个类。工厂模式让类的实例化推迟到子类进行。

```java
// 首先创建一个接口，用来实例化对象
public interface IFactory{
    Operation CreateOperation();
}
// 继承接口实现各个操作工厂
public class AddFactory implements IFactory{
    public Operation CreateOperation(){
        return new OperationAdd();
    }
}
// 客户端可以自己调用
IFactory subFactory = new SubFactory();
Operation operationSub = subFactory.CreateOperation();
```
优点是符合开闭原则。
使用场景还是很多的，例如日志记录器，数据库访问。无论产品是什么，只要用工厂来创建对象，使用产品的接口进行调用即可。
缺点：每次新增产品，需要增加具体实现类和对象实现工厂。类的个数太多了。
### 抽象工厂
为创建一组相关或相互依赖的对象提供一个接口 ，无需指定具体类。

与工厂模式的区别是，这里的产品是抽象的，工厂也是抽象的。工厂模式返回的是实例类型，抽象工厂要返回接口类型。

> 以车来做例子，车有卡车、客车、轿车之分。如果用普通工厂，那么就需要搞出一个生产卡车的工厂，一个生产客车的工厂和一个生产轿车的工厂。这很简单，里面只有一个方法，就是createVehicle即可。如果用抽象工厂，那么就需要搞出来一个纯粹的车类，也就是Vehicle类。然后再搞出来一个零件工厂类，里面可以生产轮胎、生产车架、生产发动机等。不同的工厂子类生产不同的轮胎、车架和发动机。这时候把Vehicle和零件工厂类一结合即可。可以看到，普通工厂生产出来的就是一个整车；而抽象工厂生产出来的是一堆零件，然后和车类一结合，才算是整车。

```java
// 1. 抽象产品
public interface Keyboard{
    void input();
}
public interface Mouse{
    void click();
}
// 2. 具体产品
public class MacKeyboard implements Keyboard{
    @Override
    public void input(){
        System.out.println("MAC 键盘");
    }
}
public class MacMouse implements Mouse{
    @Override
    public void click(){
        System.out.println("MAC 鼠标");
    }
}
public class WinKeyboard implements Keyboard{
    @Override
    public void input(){
        System.out.println("Win 键盘");
    }
}
public class WinMouse implements Mouse{
    @Override
    public void click(){
        System.out.println("Win 鼠标");
    }
}
// 3. 抽象工厂
public interface Hardware{
    Keyboard createKeyBoard();
    Mouse createMouse();
}
// 4. 具体工厂类
public class MacFactory implements Hardware{
    @Override
    public Keyboard createKeyBoard{
        return new MacKeyboard();
    }
    @Override
    public Mouse createMouse{
        return new MacMouse();
    }
}
public class WinFactory implements Hardware{
    @Override
    public Keyboard createKeyBoard{
        return new WinKeyboard();
    }
    @Override
    public Mouse createMouse{
        return new WinMouse();
    }
}
// 5.client
public class Client{
    public static void main(String[] args){
        Hardware factory1 = new MacFactory();
        Keyboard keyboard = factory.createKeyBoard();
        keyboard.input()

        Hardware factory2 = new WinFactory();
        Mouse mouse = factory.createMouse();
        mouse.click();
    }
}
```

## 生成器模式builder
将一个复杂的对象的构建和他的表示分离，是的同样的构建过程可以创建不同的表示。

使用场景：当一个类的构造参数个数超过4个，而且这些参数有些是可选的参数，可以考虑使用builder模式。

```java
public class Computer {
    private final String cpu;//必须
    private final String ram;//必须
    private final int usbCount;//可选
    private final String keyboard;//可选
    private final String display;//可选

    private Computer(Builder builder){
        this.cpu=builder.cpu;
        this.ram=builder.ram;
        this.usbCount=builder.usbCount;
        this.keyboard=builder.keyboard;
        this.display=builder.display;
    }
    public static class Builder{
        private String cpu;//必须
        private String ram;//必须
        private int usbCount;//可选
        private String keyboard;//可选
        private String display;//可选

        public Builder(String cup,String ram){
            this.cpu=cup;
            this.ram=ram;
        }

        public Builder setUsbCount(int usbCount) {
            this.usbCount = usbCount;
            return this;
        }
        public Builder setKeyboard(String keyboard) {
            this.keyboard = keyboard;
            return this;
        }
        public Builder setDisplay(String display) {
            this.display = display;
            return this;
        }        
        public Computer build(){
            return new Computer(this);
        }
    }
}
// client
Computer computer=new Computer.Builder("因特尔","三星")
                .setDisplay("三星24寸")
                .setKeyboard("罗技")
                .setUsbCount(2)
                .build();
```
## 原型模式
用原型实例来指定创建对象的种类，并且通过拷贝这些原型创建新的对象。
即实现Cloneable.clone
## 单例模式
保证一个类仅有一个实例，并提供一个访问它的全局访问点。
保证在一个进程中，某个类有且仅有一个实例。
实现方式：
通过private构造方法，确保外部无法进行实例化。通过private static变量持有唯一实例，保证全局唯一。通过public static方法返回唯一实例。

# 结构型模式
通过组合各种对象一遍获得更好的更灵活的结构。
## 适配器模式
将一个类的接口转换成客户希望的另一个接口，使原来由于接口不兼容而不能一起工作的那些类可以一起工作。

```java
public BAdapter implements B{
    private A a;
    public BAdapter(A a){
        this.a = a;
    }
    public void b(){
        a.a();
    }
}
```
## 桥接
将抽象部分与它的实现部分分离，使他们都可以独立的变化。
用来处理多维度的变化

## 组合
将对象组合成树形结构以表示“部分-整体”的层次结构，使得用户对单个对象和组合对象的使用具有一致性。
适用于层级结构。
## 装饰器
动态的给一个对象添加一些额外的职责。
通过装饰器模式可以在运行期动态的独立的增加核心功能或者是附加功能。

## 外观Facade
为子系统中的一组接口提供一个一致的界面。Facade模式定义了一个高层接口，这个接口是的这一子系统更加容易使用。
也就是将多个功能合并到一个函数中，形成一个流程。

## 享元 flyweight
运用共享技术有效的支持大量细粒度的对象,主要用于缓存
核心思想很简单：如果一个对象实例一经创建就不可变，那么反复创建相同的实例就没有必要，直接向调用方返回一个共享的实例就行，这样即节省内存，又可以减少创建对象的过程，提高运行速度。

## 代理模式 Proxy
为其他对象提供一种代理以控制对这个对象的访问
```java
public AProxy implements A {
    private A a;
    public Aproxy(A a){
        this.a = a;
    }
    public void a(){
        // 添加处理
        this.a.a()
        // 添加处理
    }
}
```
可以添加权限检查。

# 行为型模式
主要涉及算法和对象间的职责分配。通过使用对象组合，行为型模式可以描述一组对象应该如何写作完成一个整体任务。