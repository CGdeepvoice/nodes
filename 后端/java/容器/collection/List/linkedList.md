## LinkedList
linkedList 就是由链表实现的list, linkedList继承自 AbstractSequentialList， AbstractSequentialList继承自AbstractList，这里先看下AbstractSequentialList写了什么

**AbstractSequentialList**
AbstractSequentialList 抽象的 顺序的 列表 表明了这个类是一个抽象类，是一个次序访问的，也就是和RandomAccess不同的机制，不能随机进行访问。
这个抽象类实现的东西并不多

1. 抽象方法listIterator，和方法iterator获取迭代器
2. get方法
```java
public E get(int index) {
    try {
        // 获取Index开始的迭代器，并返回第一个元素
        return listIterator(index).next();
    } catch (NoSuchElementException exc) {
        throw new IndexOutOfBoundsException("Index: "+index);
    }
}
```
3. set方法
```java
public E set(int index, E element) {
    try {
        ListIterator<E> e = listIterator(index);
        E oldVal = e.next();
        // 这里也是使用了迭代器来赋值
        e.set(element);
        return oldVal;
    } catch (NoSuchElementException exc) {
        throw new IndexOutOfBoundsException("Index: "+index);
    }
}
```
4. add,remove, addAll,都是利用了抽象的迭代器来操作的，获取指定位置上的迭代器进行操作

简单来说就是实现类AbstractList中的没有实现的抽象方法实现了，增加了一些操作，而且主要是通过调用ListIterator来进行的。

**LinkedList**重点还是看这个linkedList
它继承了AbstractSequentialList，实现了List,Deque,Cloneable,java.io.Serialiable接口

1. 首先看他的实现方式：
```java
transient int size = 0;
transient Node<E> first;
transient Node<E> last; // 这里可以看到，定义了两个节点作为头尾，每个节点都可以指向前一个或者后一个，从而实现了一个双向链表，所有的操作都是通过链表的指向完成。这里就没有容量的概念了，因为可以无限的增加节点，只需要保持size变量来存储节点个数。
private static class Node<E> {
    E item;
    Node<E> next;
    Node<E> prev;

    Node(Node<E> prev, E element, Node<E> next) {
        this.item = element;
        this.next = next;
        this.prev = prev;
    }
}
```

2. 看下他的重要方法，增删改查
 1. add

```java
public boolean add(E e) {
    // 新增一个值，把它连接到队尾
    linkLast(e);
    return true;
}
public void add(int index, E element) {
    // 在一个index上新增一个值
    checkPositionIndex(index);
    // 如果在最后加，直接连接到队尾
    if (index == size)
        linkLast(element);
    else
        // 否则连接到index所在的节点前面，那么这个节点就成了index位置上的节点了
        // 这里的node(index)是找到在这个位置上的节点
        linkBefore(element, node(index));
}
Node<E> node(int index) {
    // assert isElementIndex(index);
    // 这里是判断index在前半部分还是后半部分
    // 前半部分就正向查找，后半部分就逆向查找，二分法的思想
    if (index < (size >> 1)) {
        Node<E> x = first;
        for (int i = 0; i < index; i++)
            x = x.next;
        return x;
    } else {
        Node<E> x = last;
        for (int i = size - 1; i > index; i--)
            x = x.prev;
        return x;
    }
}
void linkBefore(E e, Node<E> succ) {
    // assert succ != null;
    // 获取以前index位置的节点succ的前一个节点
    final Node<E> pred = succ.prev;
    // 构造一个新节点保存要新增的值， 并设置了他的前驱和后继
    final Node<E> newNode = new Node<>(pred, e, succ);
    // 这里就是链表的插入了，succ的prev指针指向当前节点
    // 前面的节点如果是空，那么要插入的就是first,否则修改pred的next指向当前
    succ.prev = newNode;
    if (pred == null)
        first = newNode;
    else
        pred.next = newNode;
    size++;
    modCount++;
}
void linkLast(E e) {
    // 获取队尾节点
    final Node<E> l = last;
    // 新增元素包装为一个节点，他是最后一个节点，他的前一个节点就是当前的最后一个节点，后一个节点是null
    final Node<E> newNode = new Node<>(l, e, null);
    // 最后一个节点为新增的节点
    last = newNode;
    if (l == null)
        // 这个判断的意思是 如果现在是一个空的链表，那么first就指向这个唯一的节点
        first = newNode;
    else
        // 否则的话，就让以前的最后一个节点指向新增的节点
        l.next = newNode;
    // 存储的个数增加，修改的记录增加
    size++;
    modCount++;
}
```
 2. addAll 把另一个Collection加入到当前的链表中

```java
public boolean addAll(Collection<? extends E> c) {
    // 没有指明在哪里加，就加到队尾
    return addAll(size, c);
}
public boolean addAll(int index, Collection<? extends E> c) {
    // 检查index是否合法，应该在0到size的范围
    checkPositionIndex(index);
    // Collection转为数组， 且不为空
    Object[] a = c.toArray();
    int numNew = a.length;
    if (numNew == 0)
        return false;
    // 这里是找到要插入的位置，如果在队尾，要替换的元素就是Null。找到他的前驱节点，把数据插入到index位置的节点和他的前驱节点之间
    Node<E> pred, succ;
    if (index == size) {
        succ = null;
        pred = last;
    } else {
        succ = node(index);
        pred = succ.prev;
    }
    // 这里就是循环加入到链表中了
    for (Object o : a) {
        @SuppressWarnings("unchecked") E e = (E) o;
        Node<E> newNode = new Node<>(pred, e, null);
        if (pred == null)
            first = newNode;
        else
            pred.next = newNode;
        pred = newNode;
    }

    if (succ == null) {
        last = pred;
    } else {
        pred.next = succ;
        succ.prev = pred;
    }

    size += numNew;
    modCount++;
    return true;
}
```
 3. addFirst，addLast,也是链表操作，不记录了
 4. clear,清理所有的节点
```java
// 这里需要把每个节点的值，指针都置为Null,first、last也置为Null
public void clear() {
    // Clearing all of the links between nodes is "unnecessary", but:
    // - helps a generational GC if the discarded nodes inhabit
    //   more than one generation
    // - is sure to free memory even if there is a reachable Iterator
    for (Node<E> x = first; x != null; ) {
        Node<E> next = x.next;
        x.item = null;
        x.next = null;
        x.prev = null;
        x = next;
    }
    first = last = null;
    size = 0;
    modCount++;
}
```
 5. get， 这里的get调用了node(index)方法，遍历找到index位置的节点的值
 6. getFirst(), getLast() 这里可以直接过去对应指针指向的节点的值
 7. indexOf(Object e) 过去目标对象的索引值

```java
public int indexOf(Object o) {
    int index = 0;
    // 这里也是一样的，通过遍历所有的节点查对比，null的情况单独处理
    if (o == null) {
        for (Node<E> x = first; x != null; x = x.next) {
            if (x.item == null)
                return index;
            index++;
        }
    } else {
        for (Node<E> x = first; x != null; x = x.next) {
            if (o.equals(x.item))
                return index;
            index++;
        }
    }
    return -1;
}
```
 8. remove() 默认删除第一个, remove（index)删除指定位置的节点， remove(Object o)删除指定的元素，使用遍历找到之后进行unlink操作，把它从链表中删除
 9. set(int index, E element), 找到元素并修改节点的值

其实和 ArrayList一样，都能实现对应的操作，只是这里的操作在链表上实现了，ArrayList在列表上实现的。对不同的应用场景，可以选择不同的链表
