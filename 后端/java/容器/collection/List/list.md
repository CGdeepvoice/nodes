## List
List接口继承自Collection接口。要理解这个接口要知道List的特点，1. 有序，2. 可重复的，3. 可以索引的， 4. 可以插入删除等动态调整的。
根据他的特点，List接口比Collection接口新增了一些方法：
1. `boolean addAll(int index, Collection<? extends E> c);`在指定的位置插入另一个集合
2. 默认的排序
```java
default void sort(Comparator<? super E> c) {
    // 转为数组，使用数组的排序，再复制回迭代器， 这里的算法就是下面写的算法，归并算法。
    Object[] a = this.toArray();
    Arrays.sort(a, (Comparator) c);
    ListIterator<E> i = this.listIterator();
    for (Object e : a) {
        i.next();
        i.set((E) e);
    }
}
```
3. `E get(int index);`
4. `E set(int index, E element);`
5. `int indexOf(Object o);`查找对象的索引位置
6. `ListIterator<E> listIterator();`提供了列表迭代器，继承自迭代器，新增了hasPrevious， pervious,前一个，可以实现向前遍历
7. `ListIterator<E> listIterator(int index);`从某个位置开始返回一个迭代器。
8. `List<E> subList(int fromIndex, int toIndex);` 返回一个范围内的子列表
9. 提供了静态方法of,用于创建不可变集合中的列表，也就是不可变列表

**ImmutableCollections** 不可变集合，包含了不可变set,不可变map,不可变list。
`Container class for immutable collections. Not part of the public API.Mainly for namespace management and shared infrastructure.` 不可变集合不是公共的API，主要用于名称空间管理和共享基础结构。

![不可变类](images/ImmutableCollections.jpg)

这个使用的比较少还是，本质就是实现了部分方法的collection接口的类。

**AbstractList**
和AbstractCollection差不多，实现了一个骨架，如果需要实现了一个不可变的列表，只要实现get和size方法即可。要实现一个可变的list，要实现set,add，remove方法

新增的方法：
1. `public Iterator<E> iterator() {return new Itr();}`实现了迭代器，Itr在内部实现了，这里有一个`checkForComodification`方法，用来实现fail-fast机制

    如果有两个线程A,B, A负责遍历list, B负责修改list,则A在遍历的过程中会比较expectedModCount = modCount=N，如果不相等就报错。如果B增加或删除一个元素，modCount会变化，A就会报错。

2. `public ListIterator<E> listIterator(final int index) {rangeCheckForAdd(index);return new ListItr(index);}` 另一个迭代器，这个迭代器和上面的差不多，新增了向前遍历，继承自Itr,实现了ListIterator
3. 定义了内部类，`SubList<E>`,继承了AbstractList,可以通过fromIndex和toIndex来控制用户可以操作的范围，从而实现了子列表

4. equals这个方法写的很好，比较全面而且简洁

```java
public boolean equals(Object o) {
    // 1. 判断指针是否指向自己
    if (o == this)
        return true;
    // 2. 相同类型才能比较
    if (!(o instanceof List))
        return false;
    // 3. 比较每个元素的话，需要获取各自的迭代器
    ListIterator<E> e1 = listIterator();
    ListIterator<?> e2 = ((List<?>) o).listIterator();
    while (e1.hasNext() && e2.hasNext()) {
        E o1 = e1.next();
        Object o2 = e2.next();
        // 4. 如果o1是null,则o2也要是null, o1不是null,则比较是否和o2相等，如果不符合条件则两个列表不相等。这个三元表达式很好
        if (!(o1==null ? o2==null : o1.equals(o2)))
            return false;
    }
    return !(e1.hasNext() || e2.hasNext());
}
```
5. hashCode,这里用到了每个元素的哈希码