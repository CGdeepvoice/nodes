## ArrayList
ArrayList, 顾名思义就是用数组实现的列表，它继承了AbstractList,并且实现了几个接口，包括List接口，RandomAccess随机访问接口，Cloneable接口等
既然是由数组实现，内部的数据必然要存放在一个数组里，然后所有的操作都是指向这个数组的。
`transient Object[] elementData;` 可以看到所有数据放在这里，transient表示不被序列化
```java
private static final int DEFAULT_CAPACITY = 10; // 默认的容量是10，初始化如果是默认的arrayList，是一个空数组，第一次扩容时最小是10
transient Object[] elementData; 
private int size; // size是实际的存储数量，容量是可以存储的数量 0 <= size <= cap
protected transient int modCount = 0; // 修改次数，多线程时候会比较这个值，cas
```

**扩容**， ArrayList区别于Array,最大的特征就是可以扩容，看下扩容机制：
```java
public void ensureCapacity(int minCapacity) {
    // 扩容到minCapacity，这个值要比以前大才算扩容，而且不能低于最小的容量10，空数组也不用扩容
    if (minCapacity > elementData.length
        && !(elementData == DEFAULTCAPACITY_EMPTY_ELEMENTDATA
                && minCapacity <= DEFAULT_CAPACITY)) {
        modCount++;
        // 主要就是调用grow函数来增加容量
        grow(minCapacity);
    }
}
private Object[] grow(int minCapacity) {
    int oldCapacity = elementData.length;
    if (oldCapacity > 0 || elementData != DEFAULTCAPACITY_EMPTY_ELEMENTDATA) {
        // 使用工具类的静态方法来获取新容量，这里的意思是最少涨0.5， 计算出minimum growth和preferred growth中较大者，再加上原来的容量
        int newCapacity = ArraysSupport.newLength(oldCapacity,
                minCapacity - oldCapacity, /* minimum growth */
                oldCapacity >> 1           /* preferred growth */);
        // 调用工具类的复制方法来进行扩容，其中包含了复制原有数据的过程
        return elementData = Arrays.copyOf(elementData, newCapacity);
    } else {
        // 最小的容量是10
        return elementData = new Object[Math.max(DEFAULT_CAPACITY, minCapacity)];
    }
}
```
既然能扩容，能不能缩小数组呢，也是可以的,trimToSize可以把数组缩小为size大小，但是这个方法要在列表不变的时候再调用，不然刚缩小了又要扩容，消耗很大
```java
public void trimToSize() {
    modCount++;
    if (size < elementData.length) {
        elementData = (size == 0)
            ? EMPTY_ELEMENTDATA
            : Arrays.copyOf(elementData, size);
    }
}
```

**重要方法**
1. indexOfRange, 对数组遍历，找到要找的对象，会区分null的情况，null用等号，其他调用equals
2. `public E get(int index){Objects.checkIndex(index, size);return elementData(index);}`这里索引index可以直接使用下标访问数组即可
3. `public E set(int index, E element)`也就是`elementData[index] = element;`
4. add方法
```java
public boolean add(E e) {
    modCount++;
    add(e, elementData, size);
    return true;
}
private void add(E e, Object[] elementData, int s) {
    // 比较实际存储的数量和容量，如果已经满了就扩容，调用前面的grow函数，这里的grow会调用grow(size+1)
    if (s == elementData.length)
        elementData = grow();
    elementData[s] = e;
    size = s + 1;
}

public void add(int index, E element) {
    // 在index位置上添加元素element
    rangeCheckForAdd(index);
    modCount++;
    final int s;
    Object[] elementData;
    // 如果满了就扩容，这里size<= elementData.length， 如果等于就是满了，不可能比length大
    if ((s = size) == (elementData = this.elementData).length)
        elementData = grow();
    // index开始所有的值向后移动一位
    System.arraycopy(elementData, index,
                        elementData, index + 1,
                        s - index);
    // index的位置上加入element，这里体现出了数组的劣势，中间插值需要移动很多值，O(N)的复杂度
    elementData[index] = element;
    size = s + 1;
}
```

5. 删除
```java
public E remove(int index) {
    Objects.checkIndex(index, size);
    final Object[] es = elementData;

    @SuppressWarnings("unchecked") E oldValue = (E) es[index];
    // 这里调用了快速删除
    fastRemove(es, index);

    return oldValue;
}
public boolean remove(Object o) {
    // 删除一个元素
    final Object[] es = elementData;
    final int size = this.size;
    int i = 0;
    //这里需要先找到这个元素, 这个found是label语法，用来退出循环的，像goto语法。这里就是找到退出，能获得坐标i
    found: {
        if (o == null) {
            for (; i < size; i++)
                if (es[i] == null)
                    break found;
        } else {
            for (; i < size; i++)
                if (o.equals(es[i]))
                    break found;
        }
        return false;
    }
    fastRemove(es, i);
    return true;
}
private void fastRemove(Object[] es, int i) {
    modCount++;
    final int newSize;
    // 如果删除的不是最后一位，需要把i后面的值全部向前移动一位
    if ((newSize = size - 1) > i)
        System.arraycopy(es, i + 1, es, i, newSize - i);
    // 如果是最后一位，直接赋值为null
    es[size = newSize] = null;
}
```
6. 相等
```java
public boolean equals(Object o) {
    if (o == this) {
        return true;
    }
    if (!(o instanceof List)) {
        return false;
    }
    final int expectedModCount = modCount;
    // 如果要比较的对象也是ArrayList,调用equalsArrayList，否则比较范围的值
    boolean equal = (o.getClass() == ArrayList.class)
        ? equalsArrayList((ArrayList<?>) o)
        : equalsRange((List<?>) o, 0, size);
    checkForComodification(expectedModCount);
    return equal;
}
boolean equalsRange(List<?> other, int from, int to) {
    final Object[] es = elementData;
    if (to > es.length) {
        throw new ConcurrentModificationException();
    }
    var oit = other.iterator();
    for (; from < to; from++) {
        // 本身是一个数组，就不用迭代器了，直接遍历，目标对象调用迭代器
        if (!oit.hasNext() || !Objects.equals(es[from], oit.next())) {
            return false;
        }
    }
    // 如果目标对象的值多余本身，也是不相等的
    return !oit.hasNext();
}

private boolean equalsArrayList(ArrayList<?> other) {
    final int otherModCount = other.modCount;
    final int s = size;
    boolean equal;
    if (equal = (s == other.size)) {
        //都是arrayList可以比较size,因为都有这个属性
        final Object[] otherEs = other.elementData;
        final Object[] es = elementData;
        if (s > es.length || s > otherEs.length) {
            // 这里是多线程，如果比较过程中被修改抛出异常
            throw new ConcurrentModificationException();
        }
        for (int i = 0; i < s; i++) {
            // 这里就简单了，比较数组，一个for循环就可以了
            if (!Objects.equals(es[i], otherEs[i])) {
                equal = false;
                break;
            }
        }
    }
    other.checkForComodification(otherModCount);
    return equal;
}
```
还有一些其他的比如addAll,removeRange等，都差不多这里不写了
ArrayList也实现了自己的迭代器，Itr和ListItr，区别就是后者能向前遍历，这里的实现就是使用了elementData这个数组。subList和AbstractList没区别，都是控制用户可见范围，只是这里的操作是对自己的elementData数组。

**其他接口方法**
forEach,调用for循环来调用action.accept参数的方法