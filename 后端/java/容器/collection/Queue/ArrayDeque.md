## ArrayDeque
ArrayDeque就是利用数组实现的双向队列。要实现双向队列，最先想到是链表，双向链表即可实现了。Linkedlist其实就是双线链表，所以把LinkedList当成Deque来用也没啥问题
数组来实现双向插入和删除，看下源码怎么做到的

ArrayDeque 继承了AbstractCollection抽象容器，实现了Deque双向队列接口，所以只要添加一些增删改查的操作就行了。

既然是数组实现，内部肯定要定义一个对象数组来保存数据 `transient Object[] elements;`.这里使用的容量就直接用了elements.length。
```java
// 可以看到默认的构造函数，会初始化数组为17个大小，但是他的注释写的是可以容纳16个元素，应该有一个位置用来存放特殊值或者作为缓冲

/**
* Constructs an empty array deque with an initial capacity
* sufficient to hold 16 elements.
*/
public ArrayDeque() {
    elements = new Object[16 + 1];
}
public ArrayDeque(int numElements) {
    // 这里也是，numElements是元素的数量，如果小于1个就创建1个，如果在1和0x7fffffff之间就创建n+1个
    elements =
        new Object[(numElements < 1) ? 1 :
                    (numElements == Integer.MAX_VALUE) ? Integer.MAX_VALUE :
                    numElements + 1];
}
```
**存疑**
这里的16+1和n+1有点奇怪，旧版本的jdk就直接创建了n个,查文档也没找到原因和提问，挺奇怪的。先继续往下看
**解答**
找到了，原来就在声明数组的地方，上面的注释写了
```java
/**
* The array in which the elements of the deque are stored.
* All array cells not holding deque elements are always null.
* The array always has at least one null slot (at tail).
* 这里意思是，这个数组用来存储双向队列的数据，所有的元素都不能为空，数组总是最少持有一个空的插槽，在尾部，所以才会多创建一个。
*/
transient Object[] elements;

/**
* The index of the element at the head of the deque (which is the
* element that would be removed by remove() or pop()); or an
* arbitrary number 0 <= head < elements.length equal to tail if
* the deque is empty.
* 这里用整数索引值来表示首项，双向队列的第一个值得索引，每次remove，pop会删除的那个值.arrayList也有删除，但是有参数的，是删除某个位置上的值或者某个值，队列才会删除队首的值。栈会删除队尾的值。因为插值在队尾
*/
transient int head;

/**
* The index at which the next element would be added to the tail
* of the deque (via addLast(E), add(E), or push(E));
* elements[tail] is always null.
* 这就说的很清楚了，下一个元素要添加的位置，不论调用addLast,add,push，elements[tail]总是null,多创建的那个。
* 但是这两个值得初始化不是在构造时，而是每次具体插入删除才会变化
*/
transient int tail;
```

**常用方法**照旧看下增删查，这里没有修改操作
1. 新增：
```java
public boolean add(E e) {
    // 这里就说明了不能新增Null,不然会报错
    addLast(e);
    return true;
}
public void addLast(E e) {
    if (e == null)
        throw new NullPointerException();
    final Object[] es = elements;
    // 如果调用了构造函数就直接添加元素，tail还没赋值，就会由jvm自动赋予初始值，int类型就是0，这里的0是对的
    // 默认的构造函数可以容纳16个值，直接调用没问题的
    es[tail] = e;
    // tail会增加1，
    if (head == (tail = inc(tail, es.length)))
        grow(1);
}
static final int inc(int i, int modulus) {
    // 这里也挺有意思，0 <= tail < length,因为是索引，最大就是length-1了。
    // 如果超过这个范围了，那么就返回head,就行扩容
    if (++i >= modulus) i = 0;
    return i;
}
private void grow(int needed) {
    // add一个元素，这里的needed也就是1
    // overflow-conscious code
    final int oldCapacity = elements.length;
    int newCapacity;
    // 如果容量很小，每次涨50%， 否则每次加两个。如果队列里的值很多，一次一次的add太浪费资源了。
    // jump只是涨幅的值，新的容量要通过newCapacity函数来获取
    // Double capacity if small; else grow by 50%
    int jump = (oldCapacity < 64) ? (oldCapacity + 2) : (oldCapacity >> 1);
    if (jump < needed
        || (newCapacity = (oldCapacity + jump)) - MAX_ARRAY_SIZE > 0)
        newCapacity = newCapacity(needed, jump);
    // 实际进行扩容
    final Object[] es = elements = Arrays.copyOf(elements, newCapacity);
    // 消除歧义的，如果tail<head,或者head==tail es[head]!= null,证明内存存储已经不对了，可能是多线程导致的
    // Exceptionally, here tail == head needs to be disambiguated
    if (tail < head || (tail == head && es[head] != null)) {
        // wrap around; slide first leg forward to end of array
        int newSpace = newCapacity - oldCapacity;
        System.arraycopy(es, head,
                            es, head + newSpace,
                            oldCapacity - head);
        for (int i = head, to = (head += newSpace); i < to; i++)
            es[i] = null;
    }
}
/** Capacity calculation for edge conditions, especially overflow. */
private int newCapacity(int needed, int jump) {
    // 来获取新的容量， 这里他用了简写的方式，声明了两个变量，只对第一个赋值了
    final int oldCapacity = elements.length, minCapacity;
    // 如果容量超了，只能用Integer.MAX_VALUE这么大的容量了
    if ((minCapacity = oldCapacity + needed) - MAX_ARRAY_SIZE > 0) {
        if (minCapacity < 0)
            throw new IllegalStateException("Sorry, deque too big");
        return Integer.MAX_VALUE;
    }
    // 上面的判断语句中已经对minCapacity赋值了。如果实际需要的比涨幅要大，就增加需要的这些
    if (needed > jump)
        return minCapacity;
    // 否则新容量就是旧的加涨幅的
    return (oldCapacity + jump - MAX_ARRAY_SIZE < 0)
        ? oldCapacity + jump
        : MAX_ARRAY_SIZE;
}
```
这就是新增一个值了，主要的操作就是维护指针tail和保证容量足够，不够就扩容
offer其实就是调用的add.
还有addFirst，和addLast差不多。但是addFirst是维护head索引，对head进行dec操作，如果head==tail进行扩容。
**由此可知**，它并不是简单的使用数组，head可以指向tail后面的，只要一直调用addFirst，head指针就会从队尾往前走。

2. 查找
先分析查找吧，因为删除和修改都需要用到查找。element,elementAt,peek等方法。
```java
public E element() {
    return getFirst();
}
public E peek() {
    return peekFirst();
}
public E peekFirst() {
    return elementAt(elements, head);
}

public E peekLast() {
    final Object[] es;
    return elementAt(es = elements, dec(tail, es.length));
}
static final <E> E elementAt(Object[] es, int i) {
    return (E) es[i];
}
public E getFirst() {
    E e = elementAt(elements, head);
    if (e == null)
        throw new NoSuchElementException();
    return e;
}
```
数组对索引的查找还是简单,而且没有对某个值得查找，只是对队首和队尾的处理


3. 删除

remove方法调用removeFirst, 在调用pollFirst。如果删除失败就报错。可以联系到Queue 会报错的是add和remove, poll不会报错，只会删除失败，所以需要这样调用，删除失败时再次抛出异常NoSuchElementException

```java
public E pollFirst() {
    // 删除队首，就是将该位置置为null,head指针自增
    final Object[] es;
    final int h;
    E e = elementAt(es = elements, h = head);
    if (e != null) {
        es[h] = null;
        head = inc(h, es.length);
    }
    return e;
}
public boolean remove(Object o) {
    // 删除指定的值
    return removeFirstOccurrence(o);
}
public boolean removeFirstOccurrence(Object o) {
    // 先遍历检查值存不存在
    if (o != null) {
        final Object[] es = elements;
        // 这里遍历一个元素，用了两层for循环。这里用两层for是因为head的值不一定比tail小，可能会在队首插值。
        for (int i = head, end = tail, to = (i <= end) ? end : es.length;
                ; i = 0, to = end) {
            for (; i < to; i++)
                if (o.equals(es[i])) {
                    delete(i);
                    return true;
                }
            if (to == end) break;
        }
    }
    return false;
}
boolean delete(int i) {
    // 删除index=i上的元素，并且将后面的前移不能置为null
    final Object[] es = elements;
    final int capacity = es.length;
    final int h, t;
    // 这里还挺麻烦的，画图就简单点，还是修改数组，用后面或者前面的移动，还需要考虑有没有跨过0
    // number of elements before to-be-deleted elt
    final int front = sub(i, h = head, capacity);
    // number of elements after to-be-deleted elt
    final int back = sub(t = tail, i, capacity) - 1;
    if (front < back) {
        // move front elements forwards
        if (h <= i) {
            System.arraycopy(es, h, es, h + 1, front);
        } else { // Wrap around
            System.arraycopy(es, 0, es, 1, i);
            es[0] = es[capacity - 1];
            System.arraycopy(es, h, es, h + 1, front - (i + 1));
        }
        es[h] = null;
        head = inc(h, capacity);
        return false;
    } else {
        // move back elements backwards
        tail = dec(t, capacity);
        if (i <= tail) {
            System.arraycopy(es, i + 1, es, i, back);
        } else { // Wrap around
            System.arraycopy(es, i + 1, es, i, capacity - (i + 1));
            es[capacity - 1] = es[0];
            System.arraycopy(es, 1, es, 0, t - 1);
        }
        es[tail] = null;
        return true;
    }
}
static final int sub(int i, int j, int modulus) {
    if ((i -= j) < 0) i += modulus;
    return i;
}
```

看了下以前版本的jdk的分析，还需要进行移位操作来计算新的容量。新版本没见到这种操作了，差别还挺大的，不过修改源码并不影响实际的功能。源代码看起来也越来越简单了应该。

数据量比较大且经常需要增加删除的话，还是用linkedList吧，这个每次都扩容太浪费资源和时间了。可以用链表来模拟队列和栈的操作。
再一次感叹，mac+idea还是挺好用的。看源码还是写代码都很舒服。