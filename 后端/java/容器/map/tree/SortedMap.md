## SortedMap
SortedMap接口继承了Map接口,顾名思义 这是一个可以有顺序的map,顺序肯定是按照key的值来比较，所以key要是可以比较的类型。而且不能使用hash来实现，想一想数据结构，不是hash肯定就是树了。

```java
// 返回排序数据所用的Comparator
Comparator<? super K> comparator();

// 返回在[fromKey, toKey)之间的数据
SortedMap<K,V> subMap(K fromKey, K toKey);

// 返回从第一个元素到toKey之间的数据
SortedMap<K,V> headMap(K toKey);

// 返回从fromKey到末尾之间的数据
SortedMap<K,V> tailMap(K fromKey);

//返回第一个数据的key
K firstKey();

//返回最后一个数据的key
K lastKey();
```