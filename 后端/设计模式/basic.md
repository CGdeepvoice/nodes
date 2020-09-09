1. 单一职责原则

    一个类，应该仅有一个引起他变化的原因。如果一个类承担的责任过多，就等于把这些职责耦合在了一起。一个职责的变化可能会削弱或者抑制这个类完成其他职责的能力。

2. 开放-封闭原则

    对扩展是开放的，对更改是封闭的。

3. 依赖倒转原则

    高层模块不应该依赖底层模块，都应该依赖抽象。
    抽象不应该依赖细节。细节应该依赖抽象。

    **里氏代换原则** 子类型必须能够替换掉他们的父类型。一个软件实体如果使用的是一个父类的话，那么一定适用于其子类，而且不会察觉出父类对象和子类对象的区别。

4. 迪米特法则LoD,最少知识法则。

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