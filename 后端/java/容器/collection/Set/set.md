## Set
set 组，继承了collection接口，是一个没有重复对象的容器。

**主要方法**
1. boolean contains(Object o); 检查是否包含某个值
2. boolean add(E e); 增加一个值,这里有返回值布尔类型，就是说可能添加成功或者失败
3. boolean remove(Object o); 
4. Iterator<E> iterator(); collection都是可以遍历的

这里也定义了of静态方法，在不可变集合中的静态类，ImmutableCollections中的Set12和SetN,


**AbstractSet**
和list一样，他也有一个抽象类实现了部分方法，方便实现类来继承和实现

这里只是简单地实现了equals,调用了containsAll， containsAll内部是for each然后另一个set是否contains每个元素。
它主要利用了contains这个方法来实现的其他方法，当然循环也会用for-each或者iterator内部的迭代器。