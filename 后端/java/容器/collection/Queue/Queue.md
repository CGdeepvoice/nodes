## Queue
队列，先进先出，主要作用就是放入元素取出元素，用来排队。与之对应的是栈，先进后出。这里先看下Queue接口如何写的。

Queue接口继承了Collection接口，Collection继承了Iterable，所以queue是可以foreach遍历的，也是可以存取数据的。

**主要方法**
1. boolean add(E e); 新增一个元素
2. boolean offer(E e); 也是新增一个元素，注释写的是如果容量满了，add新增一个元素会报错, offer会返回一个False, 具体实现还是要看子类怎么写
3. E remove(); 删除队首的元素，如果队列为空则抛出异常
4. E poll(); 将队首的元素删除，队列为空则返回Null
5. E element(); 获取队首的元素但是不删除，队列为空则抛出异常
6. peek 获取队首元素，但是不移除，队列为空则返回Null

可以看到这里实现了两套增删查，一套会报出异常，一套不会。
看下他的抽象实现类
**AbstractQueue**
这里对add,remove,element,使用offer,poll,peek做了实现。主要就是如果操作不成功就抛出异常。新增了几个方法
1. add
```java
public boolean add(E e) {
    // 如果调用offere插入失败，就报错容量满了
    if (offer(e))
        return true;
    else
        throw new IllegalStateException("Queue full");
}
```
2. remove,element和add是相同的，调用的是pool和peek
3. clear

```java
public void clear() {
    // 这里有点意思，一直poll()，知道取光所有数据
    while (poll() != null)
        ;
}
```
4. addAll() 添加全部的collection到队列里
```java
public boolean addAll(Collection<? extends E> c) {
    if (c == null)
        throw new NullPointerException();
    if (c == this)
        throw new IllegalArgumentException();
    boolean modified = false;
    // 调用目标的foreach来加入到队列中，如果容量满了就报错了
    for (E e : c)
        if (add(e))
            modified = true;
    return modified;
}
```