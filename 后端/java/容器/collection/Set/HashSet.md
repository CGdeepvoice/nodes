## HashSet
先来看一个最简单也比较常见的set,利用hash来实现的set

继承自AbstractSet,实现了set方法
他的内部是利用了一个HashMap来存储的。有点奇怪了，Map内部也用到了Set接口，我还是先去看Map接口。

HashSet内部定义了一个私有属性`private transient HashMap<E,Object> map;`,直接利用了HashMap

**construct构造器**
```java
public HashSet() {
    map = new HashMap<>();
}
public HashSet(Collection<? extends E> c) {
    // 这里是将其他容器转换为set
    map = new HashMap<>(Math.max((int) (c.size()/.75f) + 1, 16));
    addAll(c);
}
public HashSet(int initialCapacity) {
    map = new HashMap<>(initialCapacity);
}
```
这里就是用了HashMap,对hashMap的封装
**add操作**
```java
public boolean add(E e) {
    // 使用map就很简单了，直接put就行了，因为只有key,没有value,就用了一个空对象
    return map.put(e, PRESENT)==null;
}
```

**remove**
```java
public boolean remove(Object o) {
    return map.remove(o)==PRESENT;
}
```

**contains**
```java
public boolean contains(Object o) {
    return map.containsKey(o);
}
```
这里就没什么好看的了，都是用了hashMap